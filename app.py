import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtTest import *
from graph import DictGraph
import numpy as np
# https://www.thomaspietrzak.com/teaching/IHM/pyqt2.pdf

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    
class Node():
    radius = 10
    factor_root = 0.8
    def __init__(self, rect, i, root, level=0):
        self.rect = rect
        self.i = i
        self.moved = False
        self.level = level
        
    def __hash__(self):
        return self.i
    
    def __str__(self):
        return str(self.i)
    
    def __repr__(self):
        return str(self.i)
    
    def get_center(self):
        x, y, w, h = self.rect
        x_center, y_center = x + w//2, y + h//2
        return (x_center, y_center)
    
    def set_X(self, x):
        self.rect[0] = x
    
    def set_Y(self, y):
        self.rect[1] = y
    
    def get_X(self):
        return self.rect[0]
    
    def get_Y(self):
        return self.rect[1]
        
    def draw(self, painter):
        if self.level == 0:
            painter.setBrush(Qt.GlobalColor.green)
        elif self.level == 1:
            painter.setBrush(Qt.GlobalColor.cyan)
        elif self.level == 2:
            painter.setBrush(Qt.GlobalColor.yellow)
        painter.drawEllipse(*self.rect)
        
    def draw_root(self, painter):
        center = self.get_center()
        painter.drawEllipse(QPointF(*center), Node.factor_root * Node.radius, 
                                              Node.factor_root * Node.radius)
    
class PainterWidget(QWidget):
    arrow_length = 1.7
    def __init__(self, button_link, button_drag):
        super().__init__()
        button_link.clicked.connect(self.active_draw_line)
        button_drag.clicked.connect(self.active_move_rect)
        
        self.button_link = button_link
        self.button_drag = button_drag
        
        self.active_draw_line()

        self.pos = None
        self.draw_node = False
        self.moved = None
        self.source = None
        self.graph = {}
        self.roots = []
        self.setMouseTracking(True)
        
        theta = np.radians(10)
        cos, sin = np.cos(theta), np.sin(theta)
        self.rotation_right = np.array(((cos, -sin), (sin, cos)))
        self.rotation_left = np.array(((cos, sin), (-sin, cos)))
        
    def draw_arrow(self, painter, x, y, xn, yn, offset=False):
        painter.drawLine(x, y, xn, yn)
        vec = np.array((x - xn, y - yn))
        vec_u = vec/np.linalg.norm(vec) if np.linalg.norm(vec) != 0 else vec
        point_source = np.array((xn, yn))
        if offset : point_source = point_source + vec_u * Node.radius
        # https://stackoverflow.com/questions/52868835/im-getting-a-typeerror-for-a-b-but-not-b-a-numpy
        vec_u_right = vec_u@self.rotation_right
        point_right = np.array((xn, yn)) + vec_u_right * self.arrow_length * Node.radius
        vec_u_left = vec_u@self.rotation_left
        point_left = np.array((xn, yn)) + vec_u_left * self.arrow_length * Node.radius
        painter.drawLine(QPointF(*point_source), QPointF(*point_left))
        painter.drawLine(QPointF(*point_source), QPointF(*point_right))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        if self.source and self.pos :
            x_center, y_center = self.source.get_center()
            self.draw_arrow(painter, x_center, y_center, self.pos.x(), self.pos.y())
        if self.draw_node and self.pos :
            x, y = self.pos.x() - Node.radius, self.pos.y() - Node.radius
            index = len(self.graph)
            for (i, nd) in enumerate(sorted(self.graph, key=lambda nd: nd.i)):
                if i!=nd.i : 
                    index = i
                    break
            node = Node([x, y, 2 * Node.radius, 2 * Node.radius], index, False)
            self.graph[node] = []
            self.draw_node = False
        graph = {node : neighbours for (node, neighbours) in self.graph.items()}
        if self.moved and self.pos :
            x, y = self.pos.x() - Node.radius, self.pos.y() - Node.radius
            rect = [x, y, 2 * Node.radius, 2 * Node.radius]
            painter.drawEllipse(*rect)
            temp = Node(rect, self.moved.i, self.moved.level)
            graph[temp] = graph[self.moved]
            graph.pop(self.moved, None)
            graph = {node : [n if n != self.moved else temp for n in neighbours] 
                     for (node, neighbours) in graph.items()}
        for (node, neighbours) in graph.items():
            for n in neighbours :
                x, y = node.get_center()
                xn, yn = n.get_center()
                self.draw_arrow(painter, x, y, xn, yn, offset=True)
        for node in graph :
            node.draw(painter)
            if node in self.roots :
                node.draw_root(painter)
            painter.drawText(QRect(*node.rect), 
                             Qt.AlignmentFlag.AlignCenter, str(node.i))
        painter.end()

    def mousePressEvent(self, event):
        if self.source and event.button() == Qt.MouseButton.RightButton :
            self.source = None
            self.update()
            return
        remove = None
        for node in self.graph :
            x, y, w, h = node.rect
            ellipse = QRegion(x, y, w, h, QRegion.RegionType.Ellipse)
            if ellipse.contains(self.pos):
                if event.button() == Qt.MouseButton.LeftButton :
                    if self.draw_line :
                        if self.source and self.source != node :
                            if node not in self.graph[self.source] : 
                                self.graph[self.source].append(node)
                            self.source = None
                        else :
                            self.source = node
                        self.update()
                        return
                    elif self.move_node :
                        QApplication.setOverrideCursor(Qt.CursorShape.OpenHandCursor)
                        self.moved = node
                        self.update()
                        return
                elif event.button() == Qt.MouseButton.RightButton :    
                    remove = node
                    break
                elif event.button() == Qt.MouseButton.MiddleButton :
                    if node in self.roots :
                        self.roots.remove(node)
                    else :
                        self.roots.append(node)
                    self.update()
                    return
        if remove :
            if remove is self.roots :
                self.roots.remove(remove)
            self.graph.pop(remove, None)
            self.graph = {node : [n for n in neighbours if n != remove] 
                          for (node, neighbours) in self.graph.items()}
            self.update()
            return
        if not self.source and event.button() == Qt.MouseButton.LeftButton :  
            self.draw_node = True
            self.update()
            
    def mouseReleaseEvent(self, event):
        if self.moved :
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            x, y = self.pos.x() - Node.radius, self.pos.y() - Node.radius
            self.moved.set_X(x)
            self.moved.set_Y(y)
            self.moved = None
            self.update()
            
    def mouseMoveEvent(self, event):
        self.pos = event.pos()
        if self.source or self.moved :
            self.update()
    
    def active_draw_line(self):
        self.moved = None
        self.draw_line = True
        self.move_node = False
        self.button_link.setDisabled(True)
        self.button_drag.setDisabled(False)
        
    def active_move_rect(self):
        self.source = None
        self.move_node = True
        self.draw_line = False
        self.button_drag.setDisabled(True)
        self.button_link.setDisabled(False)

class Worker(QObject):
    finished = pyqtSignal()
    
    @staticmethod
    def on_discovery(source, n, painter_widget):
        n.level += 1
        painter_widget.update()
        QTest.qWait(600)
        
    @staticmethod
    def on_known(source, n, painter_widget):
        n.level += 1
        painter_widget.update()
        QTest.qWait(600)
        
    def run(self, painter_widget):
        graph = painter_widget.graph
        roots = painter_widget.roots
        dict_graph = DictGraph(roots, graph)
        try : 
            dict_graph.bfs(painter_widget, on_discovery=Worker.on_discovery, 
                                           on_known=Worker.on_known)
        except KeyError:
            pass
        while True:
            try :
                for node in graph:
                    node.level = 0
                    painter_widget.update()
                    QTest.qWait(100)
                break    
            except RuntimeError:
                pass
        self.finished.emit()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        
        vbox = QVBoxLayout()
        button_link = QPushButton("link")
        
        button_link.setSizePolicy(QSizePolicy.Policy.Fixed, 
                                  QSizePolicy.Policy.Fixed)
        vbox.addWidget(button_link)
        button_drag = QPushButton("drag and drop")
        button_drag.setSizePolicy(QSizePolicy.Policy.Fixed, 
                                  QSizePolicy.Policy.Fixed)
        vbox.addWidget(button_drag)
        self.button_run = QPushButton("run")
        self.button_run.setSizePolicy(QSizePolicy.Policy.Fixed, 
                                 QSizePolicy.Policy.Fixed)
        vbox.addWidget(self.button_run)
        
        self.button_run.clicked.connect(self.run)
        label = QLabel("link : pour lier les noeuds entre eux avec le clic gauche\n"
                      "drag and drop : pour deplacer les noeuds avec un drag and drop\n"
                      "molette : marquer le noeud comme root\n"
                      "molette sur un noeud root : l'enleve des roots\n"
                      "clic droit sur un noeud : supprimer un noeud\n")
        vbox.addWidget(label)
        hbox = QHBoxLayout()
        vbox.addStretch()
        hbox.addLayout(vbox, 1)
        self.painter_widget = PainterWidget(button_link, button_drag)
        hbox.addWidget(self.painter_widget, 3)
        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)
        
    def run(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda :self.worker.run(self.painter_widget))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        
        self.button_run.setEnabled(False)
        self.thread.finished.connect(lambda: self.button_run.setEnabled(True))
        
if __name__ == "__main__" :
    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    app.exec()
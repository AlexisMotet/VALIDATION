# Projet Validation - ENSTA Bretagne
*MOTET Alexi - HOARAU William - BERTELOOT Emile*

### Description
Notre projet de validation réalisé lors de notre 3ème année à l'ENSTA Bretagne 
dans la filière CSN a pour but de réaliser un simulateur de programmation par contrainte.

Pour réaliser celà nous avons travaillé par étape :

#### Model & Graph
Nous avons dans un premier temps chercher à modéliser un graph de POO. Pour celà, nous avons créé la classe *DictGraph* qui contient le nom du nœud racine *self.roots* et *self.d* représentant les transitions au sein du graph modélisé grace à un dictionnaire.

Par exemple ``DictGraph([3], {3: [1, 2], 1: [3, 1], 2: [3]})`` représente ici :

<p align="center"> <img src="img_1.png">

Nous avons ensuite chercher à parcourir notre graph dans ``TransitionRelation``, pour celà nous parcourons notre graphe en largeur dans ``bfs`` en marquant les nœuds les uns à la suite des autres lors de chaque visite.

#### Des exmples : nbits & hanoi

Dans ``nbits`` nous avons cherché à modéliser à partir d'un graphe tout les mots binaires de nbits et les transitions de celui-ci en ne changenat qu'un bit à la fois.

Dans ``hanoi`` nous avons cherché à résoudre le problème de la tour de hanoi en avec un nombre de disques variable et de tours variables.
<p align="center"> <img src="img_2.png">

Pour celà nous modélisons le tout par un graph en se fixant des conditions sur la transition entre 2 configuration, un disque ne peut pas plus grand ne peut pas être au-dessus d'un disque plus petit.

#### Avoir une Trace

#### Semantic  : Alice & Bob

#### Composition : Se déplacer dans 2 graphes avec les mêmes variables

#### BONUS - Interface Graphique & Test Unitaire

Nous avons créer une interface graphique permettant à l'utlisateur de créer son propre graph et de montrer son parcours par un parcours en largeur (*Breadth-First Search* - bfs).

Pour celà il faut :

* Clicker sur *Link*
* Puis n'importe où dans la fenêtre blanche pour y ajouter un nœud
* Clicker de nœud en nœud pour y ajouter des liens
* Réaliser un click molette sur un nœud afin qu'il soit le départ de notre parcours de graph

Nous pouvons enfin, clicker sur *run* pour pour voir le parcours du graph de manière graphique.
<p align="center"> <img src="img.png">
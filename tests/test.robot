*** Settings ***
Documentation   Test case pour vérifier le fonctionnement de
...             l'outil de test robot framework
...

*** Variables ***
${a}    1
${b}    2

*** Keywords ***
Afficher les valeurs de a et b
    Log    a = ${a}
    Log    b = ${b}


*** Test Cases ***
Test de la classe AandB
    [Documentation]   Test de robot framework
    [Tags]   test1
    Afficher les valeurs de a et b


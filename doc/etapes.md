retirer le type de produits et mettre juste une liste de produits avec de la pagination

# Cahier des charges

## Description du parcours utilisateur

L'utilisateur est sur le terminal. Ce dernier lui affiche les choix suivants :

1 - Quel aliment souhaitez-vous remplacer ? 

2 - Retrouver mes aliments substitués.

L'utilisateur sélectionne 1. Le programme pose les questions suivantes à l'utilisateur et ce dernier sélectionne les réponses :

* Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
* Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
* Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
* L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.
 

## Fonctionnalités

* Recherche d'aliments dans la base Open Food Facts.
* L'utilisateur interagit avec le programme dans le terminal, mais si vous souhaitez développer une interface graphique vous pouvez,
* Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question,
* La recherche doit s'effectuer sur une base MySql.

# Etapes

## 1 - Organiser son travail

*Ecrire des user stories pour faire des taches et sous taches*

[user_stories.md](user_stories.md)

*creer un tableau agile et mettre des deadlines*

https://trello.com/b/NFvfd67Q/ocdapythonpr5

*Ecrire la documentation pour faire du DDD*

[documentation.md](documentation.md)

## 2 - Construire la base de données

*Ecrire le modèle physique de données*

catégories:
* petit dejeuner
    * pate a tartiner
    * sandwich
    * fromage
    * biscuits
    * compotes
    * pizza
    * choucroute
    * ravioli
    * creme chocolat
    * yaourt aux fruits

* les données de OFF
* les données sauvegardées par l'utilisateur

database.png


*Avoir un script pour la création de la base*

*Ecrire un script qui récupère les données de OFF pour les mettre dans notre base*

## 3 - Construire le programme

*Lister les fonctionnalitées,faire un diagramme de classe*

## 4 - Intéragir avec la base de données

*Ecrire les requetes*

*Ecrire la structure du programme*

# difficultés rencontrées

structure du main pour la logique de sequencage des fenetres

faire les différents raises pour les erreurs de la DB
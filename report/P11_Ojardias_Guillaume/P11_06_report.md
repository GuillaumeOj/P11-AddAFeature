---
title: Projet 11 - Améliorez un projet existant en Python
subtitle: Parcours OpenClassrooms - Développeur d'application Python
author:
  - 'Étudiant : Guillaume OJARDIAS'
  - 'Mentor : Erwan KERIBIN'
  - 'Mentor évaluateur : Ranga GONNAGE'
geometry: margin=2cm
---
\renewcommand{\contentsname}{Sommaire}
\tableofcontents

\pagebreak
# I. Présentation

Ce projet reprend l'application réalisée lors des projets 8 et 10.

L'objectif de ce projet 11, est d'ajouter une fonctionnalité majeure à un projet existant et de corriger un bug introduit par un tiers au sein de la base de code.

## I.1. Liens du projets

- Le code source du projet est disponible sur la plate-forme GitHub à cette adresse : _[https://github.com/GuillaumeOj/P11-AddAFeature](https://github.com/GuillaumeOj/P11-AddAFeature)_.
- Le site est visible en ligne à cette adresse : _[https://projet-11.ojardias.io/](https://projet-11.ojardias.io/)_.
- Le tableau Notion du projet est accessible ici : _[https://www.notion.so/guillaumeoj/](https://www.notion.so/guillaumeoj/c79895c9cf514fe0ae1ff4d535d42308?v=0d9c86e1912149bcbbc329277ca46819)_.

# II. Démarche de création

Mes objectifs personnels sur ce projet étaient :

- d'être le plus efficace possible avec le peu de temps que j'avais à ma disposition par semaine;
- d'éviter de m'égarer en modifiant des parties importantes de mon code ou en ajoutant des fonctionnalités autre que celle fixée au préalable avec mon mentor.

Finalement, les deux fonctionnalités principales ajoutées lors de ce projet sont :

- l'envoir par e-mail d'une fiche produit;
- l'ajout de _[tox](https://tox.readthedocs.io/en/latest/)_ pour la gestion des environnements de tests.

J'ai utilisé Notion pour la réalisation d'un tableau des tâches de ce projet. Ce tableau m'a permis de mettre en évidence :

- les tâches nécessaire au transfert du projet 10 vers le projet 11 (nouveau dépôt GitHub, nouveau nom de domaine, nouvelle configuration serveur, etc.);
- les tâches pour la mise en place de tox;
- les tâches pour la création de la nouvelle fonctionnalité;

## II.1. Mise en place de _Tox_

Je souhaitais mettre en place _Tox_ car il est utilisé pour les projets de mon stage. C'était donc l'occasion pour moi de mieux comprendre son utilité et comment le configurer.

J'ai créé plusieurs environnements :

- `py39` : lance les tests unitaires et fontcionnels;
- `pep8` : vérifie avec les outils `black`, `isort` et `flake8` la conformité du code;
- `coverage` : vérifie la couverture de test de la base de code;
- `start` : permet de démarrer le serveur d'application en local;
- `prod` : exécute différentes tâches nécessaires à la mise en production de l'application;
- `init-db` : initialise la base de données lors de la première mise en service de l'application.

## II.2. Envoi d'une fiche produit par e-mail

Pour la mise en place de la nouvelle fonctionnalité, j'ai découpé mon travail en trois parties :

- mise en place de la vue nécessaire sur la partie back-end de l'application;
- création du template du mail en utilisant le framework MJML;
- réalisation du front-end en ajoutant le bouton d'envoi de la fiche du produit.

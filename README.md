# DSIA_5101_A
E5 DSIA
DANG Méline et VAN ROOIJ Théo


# Comment lancer le projet ? 
Pour lancer notre projet il vous suffit de :
- lancer Docker ;
- aller dans votre Terminal et vous placer dans le dossier de notre projet ;
- lancer un "docker-compose up -d" depuis le Terminal ;
- ouvrir un navigateur, et rendez-vous sur la page "http://localhost:8050/".


# Pourquoi ce projet, et comment fonctionne-t-il ?
Notre projet vise à réaliser une plateforme de vie scolaire pour les écoles.
Il est possible d'accéder à quatre pages principales depuis notre barre de navigation :
- la page d'accueil, là où nous expliquons d'accueil brièvement le but de notre projet ;
- la page élèves, c'est ici que se regroupe tous les élèves comtenus dans notre database ;
- la page professeurs, c'est ici que se regroupe tous les professeurs de notre database ;
- la page matières/unités, nous y retrouvons toutes les matières enseignées par les professeurs, et suivies par les élèves de notre database.


## Page Elèves
La page élèves regroupe tous les élèves de la database en plusieurs colonnes détaillant : 
- noms ;
- prénoms ;
- dates de naissance ;
- niveaux scolaires ;
- classes ;
- matières auxquelles ils sont inscrits.
Nous pouvons ajouter directement des élèves en cliquant sur le bouton "Ajouter un élève" en haut à droite de notre page. Depuis la page de création, nous pouvons rentrer les détails mentionnés au-dessus, et sélectionner les matières auxquelles l'élève est inscrit (il faut au préalable ajouter des matières dans la page Matières/Unités).
Pour inscrire les élèves à plusieurs matières, il faut maintenir la touche CTRL et sélectionner les matières voulues, ou bien SHIFT pour en sélectionner plusieurs de suite.
Nous pouvons gérer les élèves à partir de cette page, c'est-à-dire : voir la page détaillée des élèves, modifier leurs informations si besoin, ou bien même supprimer des élèves depuis la colonne "Actions", respectivement par les boutons "Détails", "Modifier" et "Supprimer".

### Page d'un élève spécifique
Il est possible de cliquer sur le bouton "Détails" de la Page Elèves, ou bien sur le nom ou prénom d'un élève en particulier (directement depuis la table de la Page Elèves), pour accéder à sa page élève spécifique dans laquelle nous pouvons voir :
- nom et prénom de l'élève ;
- niveau scolaire et classe de l'élève ;
- date de naissance de l'élève ;
- tous les cours où est inscrit l'élève, il est possible de modifier la note de l'élève de chaque matière en particulier, d'accéder à la page détaillée de la matière, ou de le désinscrire d'une unité depuis cette page en cliquant respectivement sur les boutons symbole de Edit de la note (le petit dessin avec une feuille et un crayon), "Détails" et "Désinscrire".
Nous pouvons aussi modifier directement les informations de l'élève en cliquant sur le bouton "Modifier l'élève" en haut à droite de notre page.


## Page Professeurs
La page élèves regroupe tous les professeurs de la database en plusieurs colonnes détaillant : 
- noms ;
- prénoms ;
- dates de naissance ;
- matières qu'ils enseignent.
Nous pouvons ajouter directement des professeurs en cliquant sur le bouton "Ajouter un professeur" en haut à droite de notre page. Depuis la page de création, nous pouvons rentrer les détails mentionnés au-dessus, et sélectionner les matières qu'enseigne le professeur (il faut au préalable ajouter des matières dans la page Matières/Unités).
Pour associer les professeurs à plusieurs matières, il faut maintenir la touche CTRL et sélectionner les matières voulues, ou bien SHIFT pour en sélectionner plusieurs de suite.
Nous pouvons gérer les professeurs à partir de cette page, c'est-à-dire : voir la page détaillée des professeurs, modifier leurs informations si besoin, ou bien même supprimer des professeurs depuis la colonne "Actions", respectivement par les boutons "Détails", "Modifier" et "Supprimer".

### Page d'un professeur spécifique
Il est possible de cliquer sur le bouton "Détails" de la Page Professeurs, ou bien sur le nom ou prénom d'un professeur en particulier (directement depuis la table de la Page Professeurs), pour accéder à sa page professeur spécifique dans laquelle nous pouvons voir :
- nom et prénom du professeur ;
- niveau scolaire et classe du professeur;
- date de naissance du professeur ;
- tous les cours qu'enseigne le/la professeur, il est possible d'accéder à la page détaillée de la matière, ou de le désassocier d'une unité depuis cette page en cliquant respectivement sur les boutons "Détails" et "Désinscrire".
Nous pouvons aussi modifier directement le/la professeur en cliquant sur le bouton "Modifier le/la professeur" en haut à droite de notre page.


## Page Matières/Unités
La page Matières/Unités regroupe toutes les matières de la database en plusieurs colonnes détaillant : 
- code de la matière/unité ;
- nom de la matière/unité.
Nous pouvons ajouter directement des matières en cliquant sur le bouton "Ajouter une matière/unité" en haut à gauche de notre page. Depuis la page de création, nous pouvons rentrer les détails mentionnés au-dessus.
Nous pouvons gérer les matières à partir de cette page, c'est-à-dire : voir la page détaillée des matières, modifier leurs informations si besoin, ou bien même supprimer des matières depuis la colonne "Actions", respectivement par les boutons "Détails", "Modifier" et "Supprimer".

 ### Page d'une matière/unité spécifique
Il est possible de cliquer sur le bouton "Détails" de la Page Matières/Unités, ou bien sur le nom ou prénom d'une matière/unité en particulier (directement depuis la table de la Page Matières/Unités), pour accéder à sa page unité spécifique dans laquelle nous pouvons voir :
- code et nom de l'unité ;
- tous les professeurs associés au cours, il est possible d'accéder à la page détaillée du professeur ou bien de le désassocier du cours en utilisant respectivement les boutons "Détails" et "Désinscrire" ;
- tous les élèves inscrits au cours ainsi que leur note générale dans cette unité, il est possible de modifier la note, de voir la page détaillée de l'élève ou de le désinscrire du cours respectivement par les boutons symbole de Edit de la note (le petit dessin avec une feuille et un crayon), "Détails" et "Désinscrire".
Nous pouvons aussi modifier directement la matière/unité en cliquant sur le bouton "Modifier l'unité" en haut à droite de notre page.



# Explications des routers


## student

create_student : permet de créer un élève en utilisant les réponses soumises au form student pour avoir les données nécessaires à sa création. Les matières que nous pouvons assigner à l'élève sont recherchées à partir de celles stockées dans les matières de la database. Ajoute le nouvel élève à la database. Si l'élève est déjà repertorié dans la database, nous retournons une erreur 409.

get_all_students : permet de récuperer tous les élèves présents dans la database.

get_student_by_id : permet de récuperer un élève grâce à son ID unique. Si l'ID donné n'est pas repertorié dans la database, nous retournons une erreur 404.

update_student_by_id : permet de modifier un élève grâce à son ID unique et en ouvrant le form conçu pour récuperer les informations d'un élève.

delete_student_by_id : permet de supprimer un élève grâce à son ID unique.

delete_all_students : permet de supprimer tous les élèves de la database.


## teacher

create_teacher : permet de créer un professeur en utilisant les réponses soumises au form teacher pour avoir les données nécessaires à sa création. Les matières que nous pouvons assigner au professeur sont recherchées à partir de celles stockées dans les matières de la database. Ajoute le nouvel professeur à la database. Si le professeur est déjà repertorié dans la database, nous retournons une erreur 409.

get_all_teachers : permet de récuperer tous les professeurs présents dans la database.

get_teacher_by_id : permet de récuperer un professeur grâce à son ID unique. Si l'ID donné n'est pas repertorié dans la database, nous retournons une erreur 404.

update_teacher_by_id : permet de modifier un professeur grâce à son ID unique et en ouvrant le form conçu pour récuperer les informations d'un professeur.

delete_teacher_by_id : permet de supprimer un professeur grâce à son ID unique.

delete_all_teachers : permet de supprimer tous les professeurs de la database.


## subject

create_subject : permet de créer une matière en utilisant les réponses soumises au form subject pour avoir les données nécessaires à sa création. Si la matière est déjà repertoriée dans la database, nous retournons une erreur 409.

get_all_subjects : permet de récuperer toutes les matières présents dans la database.

get_subject_by_id : permet de récuperer une matière grâce à son ID unique. Si l'ID donné n'est pas repertorié dans la database, nous retournons une erreur 404.

update_subject : permet de modifier un élève grâce à son ID unique et en ouvrant le form conçu pour récuperer les informations d'un élève.

delete_subject : permet de supprimer un élève grâce à son ID unique.

delete_all_subjects : permet de supprimer toutes les matières de la database.
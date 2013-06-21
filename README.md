# HEIG-VD (FEE) notes planner

Ce script permet de récupérer ses notes de modules directement depuis l'intranet FEE de la HEIG-VD puis de les enregistrer dans un fichier Excel.

Il est ensuite possible de modifier les valeurs afin de prévoir facilement ses notes finales de modules.

Pour l'utiliser, il faut installer les modules Python suivants (avec pip ou easy_install) :

```shell
pip install requests
pip install XlsxWriter
pip install beautifulsoup4
```

Il suffit ensuite d'appeler le script en lui passant en paramètre votre nom d'utilisateur et mot de passe pour l'intranet :

```shell
python getNotes.py prenom.nom motdepasse
```

Il générera alors un fichier `Notes.xlsx` dans le dossier en cours.
# HEIG-VD (FEE) notes planner

Ce script permet de récupérer ses notes de modules directement depuis l'intranet FEE de la HEIG-VD puis de les enregistrer dans un fichier Excel.

Le fichier est généré avec les formules qui permettent de calculer les moyennes finales. Il est donc facile d'ajouter ou modifier des valeurs afin de prévoir ses notes finales de modules.

Pour l'utiliser, il faut tout d'abord installer les dépendances :

```shell
python setup.py install
```

Il suffit ensuite d'appeler le script en lui passant en paramètre votre nom d'utilisateur et mot de passe pour l'intranet :

```shell
python getNotes.py prenom.nom motdepasse
```

Il générera alors un fichier `Notes.xlsx` dans le dossier en cours.

Licence
======================
(The MIT License)

Copyright (C) 2013 Leeroy Brun, www.leeroy.me

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/leeroybrun/heigvd-notes/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

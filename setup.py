from setuptools import setup, find_packages
setup(
    name = "HEIGVD_Notes",
    version = "0.1",
    packages = find_packages(),

    install_requires = ['requests', 'XlsxWriter', 'beautifulsoup4'],

    # metadata for upload to PyPI
    author = "Leeroy Brun",
    author_email = "leeroy.brun@gmail.com",
    description = "Ce script permet de récupérer ses notes de modules directement depuis l'intranet FEE de la HEIG-VD puis de les enregistrer dans un fichier Excel.",
    license = "MIT",
    keywords = "heig-vd xlsx notes",
    url = "https://github.com/leeroybrun/heigvd-notes", 
)
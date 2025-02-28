import PyInstaller.__main__
import os

# Chemin vers l'icône (optionnel)
# icon_path = os.path.abspath("icon.ico")

PyInstaller.__main__.run([
    'app.py',  # Script principal
    '--name=PlayStore-Reviews-Analyzer',  # Nom de l'exécutable
    '--onefile',  # Créer un seul fichier exe
    '--noconsole',  # Ne pas afficher la console
    '--clean',  # Nettoyer avant la compilation
    # f'--icon={icon_path}',  # Ajouter une icône (optionnel)
    '--disable-windowed-traceback',
    '--uac-admin',  # Demander les droits admin explicitement
    '--version-file=version_info.txt',
    '--add-data=utils.py;.',  # Inclure les fichiers nécessaires
    '--collect-all=customtkinter',  # Collecter tous les fichiers de customtkinter
    '--collect-all=google_play_scraper',  # Collecter tous les fichiers de google_play_scraper
    '--collect-all=fpdf2',  # Collecter tous les fichiers de fpdf2
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
]) 
# Test de l'importation des élèves

Ce fichier contient les instructions pour tester la fonctionnalité d'importation.

## Prérequis

Pour importer des fichiers Excel (.xlsx, .xls), vous devez installer la bibliothèque `openpyxl` :

```bash
pip install openpyxl
```

Pour les fichiers CSV (.csv), aucune bibliothèque supplémentaire n'est requise.

## Tests à effectuer

1. **Test avec CSV**
   - Utilisez le fichier `students_import_example.csv` fourni
   - Cliquez sur "Charger depuis un fichier"
   - Sélectionnez le fichier CSV
   - Vérifiez que les statistiques s'affichent correctement (6 élèves, 3 garçons, 3 filles)
   - Sélectionnez une classe
   - Cliquez sur "Importer"
   - Vérifiez que les élèves ont été importés

2. **Test avec Excel**
   - Créez un fichier Excel avec le même format que le CSV d'exemple
   - Répétez les mêmes étapes que pour le CSV

3. **Test de validation**
   - Essayez d'importer un fichier avec un format incorrect
   - Vérifiez que des messages d'erreur appropriés s'affichent

## Installation de openpyxl

Si vous voulez supporter les fichiers Excel, installez openpyxl :

```bash
# Windows
pip install openpyxl

# Ou dans un environnement virtuel
.venv\Scripts\activate
pip install openpyxl
```

## Structure du projet

La fonctionnalité d'importation est implémentée dans :

- `screens/students/students_screen.py` - Interface utilisateur et logique
- `screens/students/students_services.py` - Services d'importation
- `data/api/fake_client.py` - API pour l'importation en base de données

## Format des fichiers

Consultez `IMPORT_FORMAT.md` pour tous les détails sur le format des fichiers d'importation.

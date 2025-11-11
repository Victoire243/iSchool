# Fonctionnalité d'Importation des Élèves - Documentation Technique

## Vue d'ensemble

Cette fonctionnalité permet d'importer plusieurs élèves simultanément via des fichiers CSV ou Excel dans l'application iSchool.

## Nouvelles Fonctionnalités Implémentées

### 1. Dialogue d'Importation

- Interface utilisateur intuitive pour sélectionner et prévisualiser les fichiers
- Affichage des statistiques en temps réel (total, garçons, filles)
- Sélection de la classe de destination
- Style cohérent avec l'interface existante

### 2. Parsers de Fichiers

- **Parser CSV** : Lit les fichiers CSV avec encodage UTF-8
- **Parser Excel** : Lit les fichiers .xlsx et .xls (nécessite openpyxl)
- Validation automatique des données
- Gestion des erreurs gracieuse

### 3. API d'Importation

- Nouvelle méthode `import_students()` dans le FakeApiClient
- Insertion batch des élèves dans la base de données
- Création automatique des inscriptions (enrollments)
- Support des transactions pour garantir la cohérence

## Fichiers Modifiés

### 1. `src/screens/students/students_screen.py`

**Modifications :**

- Ajout de `_build_import_dialog()` : Construction du dialogue d'importation
- Ajout de `_pick_import_file()` : Sélection de fichier avec FilePicker
- Ajout de `_parse_import_file()` : Orchestration du parsing
- Ajout de `_parse_csv_file()` : Parsing des fichiers CSV
- Ajout de `_parse_excel_file()` : Parsing des fichiers Excel
- Ajout de `_open_import_dialog()` : Ouverture du dialogue
- Ajout de `_close_import_dialog()` : Fermeture du dialogue
- Ajout de `_confirm_import()` : Exécution de l'importation
- Ajout de `_create_detail_stat()` : Création des cartes de statistiques
- Ajout de `_populate_import_classroom_dropdown()` : Remplissage du dropdown
- Ajout de `_show_error_snackbar()` et `_show_success_snackbar()` : Messages utilisateur
- Mise à jour du bouton "Charger depuis un fichier" pour ouvrir le dialogue

### 2. `src/screens/students/students_services.py`

**Modifications :**

- Ajout de `import_students()` : Service d'importation

### 3. `src/data/api/fake_client.py`

**Modifications :**

- Ajout de `create_student()` : Création d'un seul élève
- Ajout de `import_students()` : Importation multiple avec inscriptions
- Ajout de `update_student()` : Mise à jour d'un élève existant

### 4. `src/langs/fr.json` et `src/langs/en.json`

**Ajouts :**

- Traductions pour toutes les nouvelles fonctionnalités
- Messages d'erreur et de succès
- Labels des champs du dialogue

## Nouveaux Fichiers Créés

1. **`IMPORT_FORMAT.md`** : Documentation complète du format des fichiers d'importation
2. **`IMPORT_TEST.md`** : Instructions de test de la fonctionnalité
3. **`students_import_example.csv`** : Fichier d'exemple pour l'importation

## Format des Fichiers d'Importation

### Structure CSV

```csv
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
Jean,Kabongo,Mukendi,M,15-03-2010,Avenue Lubumbashi 123,+243 123 456 789
```

### Structure Excel

| first_name | last_name | surname | gender | date_of_birth | address | parent_contact |
|------------|-----------|---------|--------|---------------|---------|----------------|
| Jean       | Kabongo   | Mukendi | M      | 15-03-2010    | ...     | ...            |

### Colonnes Requises

1. `first_name` : Prénom
2. `last_name` : Nom de famille
3. `surname` : Post-nom
4. `gender` : Sexe (M = Masculin, F = Féminin)
5. `date_of_birth` : Date de naissance (format JJ-MM-AAAA)
6. `address` : Adresse (optionnel)
7. `parent_contact` : Contact du parent (optionnel)

## Workflow d'Importation

```
1. Utilisateur clique sur "Charger depuis un fichier"
   ↓
2. Dialogue d'importation s'ouvre
   ↓
3. Utilisateur clique sur "Parcourir"
   ↓
4. FilePicker s'ouvre (filtré : CSV, XLSX, XLS)
   ↓
5. Utilisateur sélectionne un fichier
   ↓
6. Parsing automatique du fichier
   ↓
7. Affichage des statistiques
   - Total d'enregistrements
   - Nombre de garçons
   - Nombre de filles
   ↓
8. Utilisateur sélectionne la classe
   ↓
9. Utilisateur clique sur "Importer"
   ↓
10. Importation en base de données
    - Insertion des élèves
    - Création des inscriptions
   ↓
11. Message de confirmation
   ↓
12. Rechargement automatique des données
```

## Validation des Données

### Pendant le Parsing

- Vérification du format de fichier (.csv, .xlsx, .xls)
- Vérification de la présence des colonnes requises
- Conversion et normalisation des données

### Pendant l'Importation

- Vérification de la sélection de classe
- Vérification de l'année scolaire active
- Gestion des erreurs ligne par ligne

### Gestion des Erreurs

- Les lignes invalides sont ignorées
- L'importation continue pour les lignes valides
- Un compteur affiche le nombre d'élèves importés avec succès

## Statistiques Affichées

Le dialogue affiche trois statistiques clés :

1. **Total d'enregistrements** : Nombre total d'élèves dans le fichier
2. **Nombre de garçons** : Élèves avec gender = "M"
3. **Nombre de filles** : Élèves avec gender = "F"

## Dépendances

### Obligatoires (déjà présentes)

- `flet` : Framework UI
- `asyncio` : Opérations asynchrones
- `csv` : Parsing CSV (bibliothèque standard Python)

### Optionnelles

- `openpyxl` : Pour le support des fichiers Excel (.xlsx, .xls)

  ```bash
  pip install openpyxl
  ```

## Architecture et Modularité

L'implémentation respecte l'architecture existante :

- **Séparation des préoccupations** : UI, Services, API
- **Réutilisation des composants** : Utilisation des styles existants
- **Cohérence visuelle** : Design similaire aux dialogues existants
- **Gestion des erreurs** : Messages utilisateur appropriés
- **Asynchronisme** : Opérations non-bloquantes

## Tests Recommandés

1. **Test de format CSV**
   - Fichier valide avec tous les champs
   - Fichier avec colonnes manquantes
   - Fichier avec données invalides

2. **Test de format Excel**
   - Fichier .xlsx valide
   - Fichier .xls valide
   - Fichier avec mauvaise structure

3. **Test de validation**
   - Sexe invalide (autre que M ou F)
   - Date de naissance dans un mauvais format
   - Fichier vide

4. **Test d'importation**
   - Importation réussie
   - Importation partielle (certaines lignes invalides)
   - Vérification de la création des inscriptions

## Messages Utilisateur

### Messages de Succès

- "[X] élèves importés avec succès"

### Messages d'Erreur

- "Format de fichier invalide. Seuls les fichiers CSV et Excel sont acceptés."
- "Erreur lors de l'importation"
- "La classe est obligatoire pour l'importation"
- "openpyxl library not installed. Please install it to import Excel files."

## Améliorations Futures Possibles

1. **Validation avancée**
   - Vérification des doublons
   - Validation du format des contacts
   - Validation des adresses

2. **Rapport d'importation détaillé**
   - Liste des élèves importés
   - Liste des erreurs avec numéros de ligne
   - Export du rapport en PDF

3. **Support de plus de formats**
   - Import depuis Google Sheets
   - Import depuis fichiers JSON
   - Import depuis API externe

4. **Prévisualisation**
   - Affichage d'un tableau avec les données à importer
   - Possibilité de modifier avant l'importation
   - Validation interactive

5. **Templates**
   - Téléchargement de template vide
   - Templates préremplis pour tests
   - Export du format actuel

## Conformité aux Instructions

✅ **Respect de la structure du projet** : Tous les nouveaux composants suivent l'architecture existante
✅ **Modularité** : Fonctions séparées et réutilisables
✅ **Design cohérent** : Utilisation des styles et composants existants
✅ **Documentation** : Format des fichiers clairement documenté
✅ **Statistiques détaillées** : Affichage du nombre total, garçons, filles
✅ **Gestion de la classe** : Sélection obligatoire de la classe de destination
✅ **Messages utilisateur** : Snackbars pour erreurs et succès
✅ **Fonctionnalités enrichies** : Parsing CSV et Excel, validation, gestion d'erreurs

## Support et Documentation

- **Format d'importation** : Voir `IMPORT_FORMAT.md`
- **Tests** : Voir `IMPORT_TEST.md`
- **Exemple de fichier** : `students_import_example.csv`

## Auteur et Maintenance

Cette fonctionnalité a été implémentée en respectant :

- Les standards de code du projet
- L'architecture existante
- Les principes de modularité
- Les bonnes pratiques de développement

# 📚 Fonctionnalité d'Importation d'Élèves

## 🎯 Vue d'ensemble

Cette fonctionnalité permet d'**importer plusieurs élèves simultanément** via des fichiers **CSV** ou **Excel** dans l'application iSchool. Elle offre une interface intuitive avec aperçu des statistiques avant l'importation.

---

## ✨ Fonctionnalités Principales

### 🔹 Interface Utilisateur

- Dialogue modal élégant avec design cohérent
- Sélecteur de fichiers intégré (FilePicker)
- Aperçu des statistiques en temps réel
- Messages de confirmation et d'erreur clairs

### 🔹 Statistiques Affichées

Après sélection du fichier, affichage automatique de :

- 📊 **Nombre total d'élèves** dans le fichier
- 👦 **Nombre de garçons** (sexe = M)
- 👧 **Nombre de filles** (sexe = F)

### 🔹 Formats Supportés

- **CSV** (`.csv`) - Comma Separated Values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel

### 🔹 Validation et Gestion des Erreurs

- Parsing automatique du fichier
- Validation ligne par ligne
- Gestion gracieuse des lignes invalides
- Messages d'erreur explicites

---

## 📋 Format des Fichiers

### En-têtes Requis (Première Ligne)

```
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
```

### Description des Colonnes

| Colonne          | Description           | Format/Valeurs              | Requis |
|------------------|-----------------------|-----------------------------|--------|
| `first_name`     | Prénom                | Texte                       | ✅     |
| `last_name`      | Nom de famille        | Texte                       | ✅     |
| `surname`        | Post-nom              | Texte                       | ✅     |
| `gender`         | Sexe                  | **M** (garçon) ou **F** (fille) | ✅ |
| `date_of_birth`  | Date de naissance     | **JJ-MM-AAAA** (ex: 15-03-2010) | ✅ |
| `address`        | Adresse               | Texte                       | ❌     |
| `parent_contact` | Contact parent/tuteur | Texte                       | ❌     |

### ⚠️ Points Importants

- **Sexe** : Uniquement **M** (masculin) ou **F** (féminin) en MAJUSCULES
- **Date** : Format strict **JJ-MM-AAAA** avec tirets (ex: `15-03-2010`)
- **Ordre** : Les colonnes doivent être dans l'ordre indiqué ci-dessus
- **Encodage CSV** : UTF-8 avec séparateur virgule (`,`)

---

## 🚀 Utilisation

### Étapes d'Importation

1. **Accéder à la page** : Ouvrez "Gestion des élèves"
2. **Ouvrir le dialogue** : Cliquez sur "Charger depuis un fichier" (bouton orange)
3. **Sélectionner le fichier** : Cliquez sur "Parcourir" et choisissez votre fichier
4. **Vérifier l'aperçu** : Les statistiques s'affichent automatiquement
5. **Choisir la classe** : Sélectionnez la classe de destination (obligatoire)
6. **Importer** : Cliquez sur "Importer" et attendez la confirmation
7. **Vérification** : La page se recharge avec les nouveaux élèves

---

## 📁 Fichiers de Documentation

### Pour les Utilisateurs

1. **`GUIDE_SIMPLE_IMPORT.md`** 📖
   - Guide simple en français
   - Instructions étape par étape
   - Exemples concrets
   - **🔥 RECOMMANDÉ POUR DÉBUTER**

2. **`UPLOAD_INSTRUCTIONS.md`** 📝
   - Instructions complètes et détaillées
   - Règles de formatage
   - Erreurs courantes à éviter
   - Conseils pratiques

3. **`students_import_example.csv`** 💾
   - Fichier d'exemple avec 6 élèves
   - Format exact à respecter
   - Prêt à utiliser pour tests

### Pour les Développeurs

4. **`IMPORT_FORMAT.md`** 🔧
   - Spécifications techniques du format
   - Structure détaillée
   - Validation des données

5. **`IMPORT_FEATURE_DOCUMENTATION.md`** 💻
   - Documentation technique complète
   - Architecture de la fonctionnalité
   - Fichiers modifiés et créés
   - API et services

6. **`IMPORT_TEST.md`** 🧪
   - Instructions de test
   - Scénarios de test
   - Installation des dépendances

7. **`SUMMARY.md`** 📊
   - Résumé complet de la fonctionnalité
   - Caractéristiques principales
   - Architecture technique

---

## 📄 Exemple de Fichier CSV

Un fichier d'exemple complet est fourni : **`students_import_example.csv`**

Contenu :

```csv
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
Jean,Kabongo,Mukendi,M,15-03-2010,Avenue Lubumbashi 123,+243 123 456 789
Marie,Tshimanga,Kalala,F,20-05-2011,Boulevard Lumumba 45,+243 987 654 321
Pierre,Mwamba,Kasongo,M,10-08-2009,Rue de la Paix 78,+243 111 222 333
Sophie,Nsimba,Luamba,F,05-12-2010,Avenue Kasa-Vubu 90,+243 444 555 666
Paul,Mutombo,Kabila,M,25-07-2010,Avenue des Martyrs 12,+243 777 888 999
Grace,Kimpembe,Nzita,F,18-09-2011,Rue de la Victoire 34,+243 222 333 444
```

---

## 🔧 Installation des Dépendances

### Pour CSV (Déjà Disponible)

Aucune installation nécessaire, bibliothèque standard Python.

### Pour Excel (Optionnel)

```bash
pip install openpyxl
```

Ou dans un environnement virtuel :

```bash
.venv\Scripts\activate
pip install openpyxl
```

---

## 🎨 Captures d'Écran du Workflow

### 1. Bouton d'Importation

Dans la page "Gestion des élèves", cliquez sur **"Charger depuis un fichier"** (bouton orange).

### 2. Dialogue d'Importation

Un dialogue s'ouvre avec :

- Sélecteur de fichier ("Parcourir")
- Zone d'affichage du nom du fichier
- Section des statistiques (masquée initialement)
- Dropdown pour sélectionner la classe
- Boutons "Annuler" et "Importer"

### 3. Aperçu des Statistiques

Après sélection du fichier, affichage de 3 cartes :

- 📊 Total d'enregistrements (couleur bleue)
- 👦 Nombre de garçons (couleur bleue)
- 👧 Nombre de filles (couleur rose)

### 4. Confirmation

Message de succès : "[X] élèves importés avec succès"

---

## ✅ Checklist Avant Importation

Avant d'importer, vérifiez que :

- [ ] Le fichier est au format CSV, XLSX ou XLS
- [ ] La première ligne contient les en-têtes
- [ ] Les colonnes sont dans le bon ordre
- [ ] Le sexe est `M` ou `F` (majuscules)
- [ ] Les dates sont au format `JJ-MM-AAAA`
- [ ] Pour CSV : encodage UTF-8, séparateur virgule
- [ ] Une classe est sélectionnée dans le dialogue

---

## 🐛 Dépannage

### Problème : "Format de fichier invalide"

**Solution** : Vérifiez que votre fichier est bien `.csv`, `.xlsx` ou `.xls`

### Problème : Certains élèves ne sont pas importés

**Solution** : Vérifiez le format des dates et le sexe (M ou F uniquement)

### Problème : "La classe est obligatoire"

**Solution** : Sélectionnez une classe dans le dropdown avant de cliquer sur "Importer"

### Problème : Erreur avec fichier Excel

**Solution** : Installez openpyxl : `pip install openpyxl`

---

## 📚 Quelle Documentation Lire ?

### 🆕 Vous débutez ?

➡️ Lisez **`GUIDE_SIMPLE_IMPORT.md`** - Guide simple avec instructions pas-à-pas

### 📝 Vous préparez votre fichier ?

➡️ Lisez **`UPLOAD_INSTRUCTIONS.md`** - Instructions détaillées avec exemples

### 👨‍💻 Vous êtes développeur ?

➡️ Lisez **`IMPORT_FEATURE_DOCUMENTATION.md`** - Documentation technique complète

### 🧪 Vous voulez tester ?

➡️ Lisez **`IMPORT_TEST.md`** - Guide de test avec scénarios

### 📊 Vous voulez un aperçu rapide ?

➡️ Lisez **`SUMMARY.md`** - Résumé de toutes les fonctionnalités

---

## 💡 Conseils Pratiques

### 1. Commencez Petit

- Testez d'abord avec le fichier d'exemple
- Puis testez avec 2-3 élèves
- Enfin importez votre fichier complet

### 2. Utilisez le Fichier d'Exemple

- Copiez `students_import_example.csv`
- Remplacez les données par les vôtres
- Gardez la même structure

### 3. Vérifiez Avant d'Importer

- Dates au bon format
- Sexe correct (M ou F)
- Pas de colonnes manquantes

### 4. Gardez une Copie

- Sauvegardez toujours votre fichier source
- En cas d'erreur, vous pourrez corriger et réessayer

---

## 🏗️ Architecture Technique

### Fichiers Modifiés

1. `src/screens/students/students_screen.py` - Interface utilisateur
2. `src/screens/students/students_services.py` - Services métier
3. `src/data/api/fake_client.py` - API et base de données
4. `src/langs/fr.json` et `src/langs/en.json` - Traductions

### Nouvelles Méthodes

- `_build_import_dialog()` - Construction du dialogue
- `_parse_csv_file()` - Parsing CSV
- `_parse_excel_file()` - Parsing Excel
- `import_students()` - Importation en BDD

### Workflow Technique

```
Interface (Dialogue) 
    ↓ 
Parsing (CSV/Excel) 
    ↓ 
Validation (Format) 
    ↓ 
Service (import_students) 
    ↓ 
API (fake_client) 
    ↓ 
Base de Données (SQLite)
```

---

## 🎉 Résultat

Une fonctionnalité complète, robuste et intuitive pour importer facilement plusieurs élèves avec :

- ✅ Interface élégante et cohérente
- ✅ Statistiques détaillées (total, garçons, filles)
- ✅ Support CSV et Excel
- ✅ Validation automatique
- ✅ Gestion des erreurs
- ✅ Documentation complète
- ✅ Respect de l'architecture du projet

---

## 📞 Support

Pour toute question ou problème :

1. Consultez d'abord **`GUIDE_SIMPLE_IMPORT.md`**
2. Vérifiez les erreurs courantes dans **`UPLOAD_INSTRUCTIONS.md`**
3. Testez avec le fichier d'exemple fourni

---

**🚀 Vous êtes prêt à importer vos élèves !**

Bonne utilisation de cette nouvelle fonctionnalité !

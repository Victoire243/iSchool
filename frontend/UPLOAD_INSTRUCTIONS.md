# 📝 INSTRUCTIONS : Format des Fichiers à Uploader

## 🎯 Formats Acceptés

L'application accepte deux types de fichiers :

- **CSV** (`.csv`) - Comma Separated Values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel

---

## 📋 Structure OBLIGATOIRE du Fichier

### En-têtes de Colonnes (Première Ligne)

Votre fichier **DOIT** contenir ces colonnes **EXACTEMENT** dans cet ordre :

```
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
```

### Description des Colonnes

| N° | Nom de Colonne    | Description                      | Format/Valeurs         | Obligatoire |
|----|-------------------|----------------------------------|------------------------|-------------|
| 1  | `first_name`      | Prénom de l'élève               | Texte libre            | ✅ OUI      |
| 2  | `last_name`       | Nom de famille                  | Texte libre            | ✅ OUI      |
| 3  | `surname`         | Post-nom                        | Texte libre            | ✅ OUI      |
| 4  | `gender`          | Sexe                            | **M** ou **F** uniquement | ✅ OUI   |
| 5  | `date_of_birth`   | Date de naissance               | **JJ-MM-AAAA**         | ✅ OUI      |
| 6  | `address`         | Adresse de résidence            | Texte libre            | ❌ Non      |
| 7  | `parent_contact`  | Contact du parent/tuteur        | Texte libre            | ❌ Non      |

---

## ⚠️ RÈGLES IMPORTANTES À RESPECTER

### 1. Colonne `gender` (Sexe)

- **M** = Masculin (Garçon)
- **F** = Féminin (Fille)
- ⛔ Pas d'autres valeurs acceptées
- ⛔ Sensible à la casse (utilisez des MAJUSCULES)

### 2. Colonne `date_of_birth` (Date de Naissance)

- **Format stricte : JJ-MM-AAAA**
- Exemples valides :
  - ✅ `15-03-2010` (15 mars 2010)
  - ✅ `01-01-2012` (1er janvier 2012)
  - ✅ `25-12-2009` (25 décembre 2009)
- Exemples invalides :
  - ❌ `15/03/2010` (mauvais séparateur)
  - ❌ `2010-03-15` (mauvais ordre)
  - ❌ `15-3-2010` (jour/mois à 2 chiffres requis)

### 3. Ordre des Colonnes

- ⚠️ L'ordre des colonnes **DOIT** être respecté
- ⚠️ Même si vous utilisez Excel, respectez l'ordre

### 4. Encodage (pour CSV)

- Utilisez **UTF-8** pour éviter les problèmes d'accents
- Séparateur : **virgule** (`,`)

---

## 📄 Exemple de Fichier CSV Valide

```csv
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
Jean,Kabongo,Mukendi,M,15-03-2010,Avenue Lubumbashi 123,+243 123 456 789
Marie,Tshimanga,Kalala,F,20-05-2011,Boulevard Lumumba 45,+243 987 654 321
Pierre,Mwamba,Kasongo,M,10-08-2009,Rue de la Paix 78,+243 111 222 333
Sophie,Nsimba,Luamba,F,05-12-2010,Avenue Kasa-Vubu 90,+243 444 555 666
```

---

## 📊 Exemple de Fichier Excel Valide

Dans Excel, créez un tableau comme ceci :

| A (first_name) | B (last_name) | C (surname) | D (gender) | E (date_of_birth) | F (address)           | G (parent_contact)  |
|----------------|---------------|-------------|------------|-------------------|-----------------------|---------------------|
| Jean           | Kabongo       | Mukendi     | M          | 15-03-2010        | Avenue Lubumbashi 123 | +243 123 456 789    |
| Marie          | Tshimanga     | Kalala      | F          | 20-05-2011        | Boulevard Lumumba 45  | +243 987 654 321    |
| Pierre         | Mwamba        | Kasongo     | M          | 10-08-2009        | Rue de la Paix 78     | +243 111 222 333    |

---

## ✅ Comment Créer un Fichier Valide

### Option 1 : Utiliser Excel

1. Ouvrez Microsoft Excel
2. Créez les en-têtes dans la première ligne (A1 à G1)
3. Remplissez vos données ligne par ligne
4. Enregistrez en `.xlsx` ou exportez en `.csv`

### Option 2 : Utiliser Google Sheets

1. Créez une nouvelle feuille Google Sheets
2. Ajoutez les en-têtes dans la première ligne
3. Remplissez vos données
4. Téléchargez en format CSV ou Excel

### Option 3 : Utiliser un Éditeur de Texte (pour CSV)

1. Ouvrez Notepad++ ou un éditeur de texte
2. Copiez le format exemple ci-dessus
3. Remplacez les données par les vôtres
4. Enregistrez avec l'extension `.csv` et encodage UTF-8

---

## 🔍 Vérification Avant Import

Avant d'importer, vérifiez que :

- [ ] La première ligne contient les en-têtes
- [ ] Les colonnes sont dans le bon ordre
- [ ] Le sexe est bien `M` ou `F` (majuscules)
- [ ] Les dates sont au format `JJ-MM-AAAA`
- [ ] Le fichier est bien `.csv`, `.xlsx` ou `.xls`
- [ ] Pour CSV : encodage UTF-8, séparateur virgule

---

## 🧪 Test avec le Fichier Exemple

Un fichier d'exemple **`students_import_example.csv`** est fourni dans le dossier `frontend/`.

Vous pouvez l'utiliser pour :

1. Voir le format exact attendu
2. Tester la fonctionnalité d'importation
3. Créer votre propre fichier en vous basant dessus

---

## ❌ Erreurs Courantes à Éviter

### 1. Sexe Invalide

```csv
Jean,Kabongo,Mukendi,Masculin,15-03-2010,...  ❌ INCORRECT
Jean,Kabongo,Mukendi,M,15-03-2010,...         ✅ CORRECT
```

### 2. Date Mal Formatée

```csv
Jean,Kabongo,Mukendi,M,15/03/2010,...         ❌ INCORRECT
Jean,Kabongo,Mukendi,M,15-03-2010,...         ✅ CORRECT
```

### 3. Colonnes Manquantes

```csv
first_name,last_name,gender,date_of_birth     ❌ INCORRECT (surname manquant)
first_name,last_name,surname,gender,...       ✅ CORRECT
```

### 4. Ordre Incorrect

```csv
last_name,first_name,surname,...              ❌ INCORRECT
first_name,last_name,surname,...              ✅ CORRECT
```

---

## 💡 Conseils Pratiques

### 1. Commencez Petit

- Testez d'abord avec 2-3 élèves
- Vérifiez que tout fonctionne
- Puis importez votre fichier complet

### 2. Gardez une Copie

- Conservez toujours une sauvegarde de votre fichier source
- En cas d'erreur, vous pourrez corriger et réessayer

### 3. Utilisez le Fichier Exemple

- Copiez `students_import_example.csv`
- Modifiez-le avec vos données
- Cela garantit le bon format

### 4. Vérifiez les Données

- Pas de doublons
- Dates cohérentes
- Sexe correct

---

## 📱 Ce Qui Se Passe Lors de l'Import

1. **Sélection du fichier**
   - Vous choisissez votre fichier CSV ou Excel

2. **Analyse automatique**
   - L'application lit et analyse le fichier
   - Affiche les statistiques (total, garçons, filles)

3. **Sélection de la classe**
   - Vous choisissez dans quelle classe inscrire les élèves

4. **Importation**
   - Les élèves sont ajoutés à la base de données
   - Les inscriptions sont créées automatiquement

5. **Confirmation**
   - Message de succès avec le nombre d'élèves importés
   - La liste se met à jour automatiquement

---

## 📞 En Cas de Problème

Si l'import échoue, vérifiez dans cet ordre :

1. ✅ Format de fichier (CSV, XLSX, XLS)
2. ✅ Première ligne = en-têtes
3. ✅ Ordre des colonnes
4. ✅ Valeurs du sexe (M ou F)
5. ✅ Format des dates (JJ-MM-AAAA)
6. ✅ Encodage UTF-8 (pour CSV)
7. ✅ Séparateur virgule (pour CSV)

---

## 📚 Documentation Complémentaire

- **Format détaillé** : `IMPORT_FORMAT.md`
- **Documentation technique** : `IMPORT_FEATURE_DOCUMENTATION.md`
- **Guide de test** : `IMPORT_TEST.md`
- **Résumé** : `SUMMARY.md`

---

**🎉 Vous êtes prêt à importer vos élèves !**

Suivez ces instructions et votre importation se déroulera sans problème.

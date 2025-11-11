# 🎓 Importation d'Élèves - Guide Simple

## 📄 Quel format de fichier utiliser ?

Vous pouvez utiliser :

- **Fichier CSV** (`.csv`)
- **Fichier Excel** (`.xlsx` ou `.xls`)

Un fichier d'exemple `students_import_example.csv` est fourni dans le dossier.

---

## 📋 Comment structurer votre fichier ?

### En-têtes (Première ligne) - OBLIGATOIRE

Votre fichier DOIT commencer par cette ligne exactement :

```
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
```

### Que mettre dans chaque colonne ?

1. **first_name** → Prénom de l'élève (ex: Jean)
2. **last_name** → Nom de famille (ex: Kabongo)
3. **surname** → Post-nom (ex: Mukendi)
4. **gender** → **M** pour garçon, **F** pour fille (MAJUSCULES !)
5. **date_of_birth** → Date au format **JJ-MM-AAAA** (ex: 15-03-2010)
6. **address** → Adresse (optionnel)
7. **parent_contact** → Téléphone des parents (optionnel)

---

## ⚠️ IMPORTANT : Points à ne pas oublier

### 1. Le sexe (gender)

- ✅ Écrivez **M** pour un garçon
- ✅ Écrivez **F** pour une fille
- ❌ N'écrivez PAS "Masculin", "Garçon", "Féminin", "Fille"

### 2. La date de naissance (date_of_birth)

- ✅ Format correct : **15-03-2010** (jour-mois-année avec des tirets)
- ❌ Format incorrect : 15/03/2010, 2010-03-15, 15-3-2010

### 3. L'ordre des colonnes

Respectez exactement l'ordre ci-dessus !

---

## 📝 Exemple de fichier CSV correct

```csv
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
Jean,Kabongo,Mukendi,M,15-03-2010,Avenue Lubumbashi 123,+243 123 456 789
Marie,Tshimanga,Kalala,F,20-05-2011,Boulevard Lumumba 45,+243 987 654 321
Pierre,Mwamba,Kasongo,M,10-08-2009,Rue de la Paix 78,+243 111 222 333
```

---

## 📊 Exemple de fichier Excel correct

Dans Excel, créez un tableau comme ceci :

| first_name | last_name | surname | gender | date_of_birth | address               | parent_contact      |
|------------|-----------|---------|--------|---------------|-----------------------|---------------------|
| Jean       | Kabongo   | Mukendi | M      | 15-03-2010    | Avenue Lubumbashi 123 | +243 123 456 789    |
| Marie      | Tshimanga | Kalala  | F      | 20-05-2011    | Boulevard Lumumba 45  | +243 987 654 321    |

---

## 🚀 Comment faire l'importation ?

### Étape 1 : Préparer votre fichier

- Utilisez Excel ou un éditeur de texte
- Respectez le format ci-dessus
- Vérifiez bien le sexe (M ou F) et les dates

### Étape 2 : Ouvrir la page des élèves

- Dans l'application, allez sur "Gestion des élèves"

### Étape 3 : Cliquer sur "Charger depuis un fichier"

- C'est le bouton orange en haut

### Étape 4 : Sélectionner votre fichier

- Cliquez sur "Parcourir"
- Choisissez votre fichier CSV ou Excel

### Étape 5 : Vérifier l'aperçu

L'application vous montre automatiquement :

- 📊 Le nombre total d'élèves
- 👦 Le nombre de garçons
- 👧 Le nombre de filles

### Étape 6 : Choisir la classe

- Dans le menu déroulant, sélectionnez la classe
- C'est obligatoire !

### Étape 7 : Importer

- Cliquez sur "Importer"
- Attendez le message de confirmation

### Étape 8 : Vérifier

- La page se recharge automatiquement
- Vos élèves apparaissent dans la liste

---

## ✅ Checklist avant d'importer

Avant de cliquer sur "Importer", vérifiez :

- [ ] Mon fichier a bien la première ligne avec les en-têtes
- [ ] Les colonnes sont dans le bon ordre
- [ ] J'ai utilisé **M** ou **F** pour le sexe (en majuscules)
- [ ] Mes dates sont au format **JJ-MM-AAAA** avec des tirets
- [ ] Mon fichier est en `.csv`, `.xlsx` ou `.xls`
- [ ] J'ai bien sélectionné une classe

---

## 🎯 Conseils pratiques

### Pour débuter

1. Utilisez d'abord le fichier d'exemple `students_import_example.csv`
2. Testez l'importation avec 2-3 élèves
3. Si ça marche, préparez votre fichier complet

### Pour créer votre fichier

1. Copiez le fichier d'exemple
2. Remplacez les données par les vôtres
3. Gardez le même format

### Si Excel est disponible

1. Ouvrez Excel
2. Créez votre tableau avec les en-têtes
3. Remplissez ligne par ligne
4. Enregistrez en `.xlsx`

---

## ❌ Erreurs fréquentes

### Erreur 1 : Sexe mal écrit

```
❌ Masculin → Utilisez M
❌ Garçon → Utilisez M
❌ m → Utilisez M (majuscule)
✅ M → CORRECT
```

### Erreur 2 : Date mal formatée

```
❌ 15/03/2010 → Utilisez 15-03-2010
❌ 2010-03-15 → Utilisez 15-03-2010
❌ 15-3-2010 → Utilisez 15-03-2010
✅ 15-03-2010 → CORRECT
```

### Erreur 3 : Colonnes manquantes

Toutes les colonnes doivent être présentes, même si certaines sont vides.

---

## 💡 Ce qui se passe pendant l'importation

1. ✅ L'application lit votre fichier
2. ✅ Elle compte les garçons et les filles
3. ✅ Elle vous montre les statistiques
4. ✅ Vous choisissez la classe
5. ✅ Les élèves sont ajoutés à la base de données
6. ✅ Les inscriptions sont créées automatiquement
7. ✅ Un message vous confirme le nombre d'élèves importés

---

## 📱 Besoin d'aide ?

### Pour créer votre fichier

1. Consultez `UPLOAD_INSTRUCTIONS.md` (instructions détaillées)
2. Utilisez le fichier d'exemple fourni
3. Respectez exactement le format

### Si l'import ne fonctionne pas

Vérifiez dans cet ordre :

1. Format du fichier (CSV ou Excel)
2. Première ligne = en-têtes
3. Sexe = M ou F (majuscules)
4. Dates = JJ-MM-AAAA (avec tirets)
5. Classe sélectionnée

---

## 📚 Documentation complète

Si vous avez besoin de plus d'informations, consultez :

- **`UPLOAD_INSTRUCTIONS.md`** : Instructions très détaillées
- **`IMPORT_FORMAT.md`** : Format technique complet
- **`SUMMARY.md`** : Résumé de la fonctionnalité
- **`students_import_example.csv`** : Fichier d'exemple à copier

---

## 🎉 Vous êtes prêt

Suivez ces instructions simples et votre importation réussira du premier coup !

**Astuce** : Commencez toujours par tester avec 2-3 élèves avant d'importer votre fichier complet.

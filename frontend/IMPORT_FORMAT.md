# Format des fichiers d'importation des élèves

Ce document décrit le format à respecter pour les fichiers CSV et Excel lors de l'importation des élèves dans l'application iSchool.

## Formats de fichiers acceptés

- **CSV** (`.csv`) - Comma Separated Values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel

## Structure du fichier

### Colonnes requises (en-têtes)

Le fichier doit contenir les colonnes suivantes dans l'ordre suivant (la première ligne doit être l'en-tête) :

| Nom de colonne    | Description                           | Format / Valeurs acceptées | Obligatoire |
|-------------------|---------------------------------------|----------------------------|-------------|
| `first_name`      | Prénom de l'élève                     | Texte                      | Oui         |
| `last_name`       | Nom de famille                        | Texte                      | Oui         |
| `surname`         | Post-nom                              | Texte                      | Oui         |
| `gender`          | Sexe de l'élève                       | `M` (garçon) ou `F` (fille)| Oui         |
| `date_of_birth`   | Date de naissance                     | `JJ-MM-AAAA` (ex: 15-03-2010) | Oui      |
| `address`         | Adresse de résidence                  | Texte                      | Non         |
| `parent_contact`  | Contact du parent/tuteur              | Texte                      | Non         |

### Remarques importantes

1. **Ordre des colonnes** : L'ordre des colonnes doit être respecté comme indiqué ci-dessus
2. **Sexe** : Utilisez **M** pour les garçons (masculin) et **F** pour les filles (féminin)
3. **Date de naissance** : Format stricte `JJ-MM-AAAA` (jour-mois-année). Exemple : `15-03-2010`
4. **Encodage** : Pour les fichiers CSV, utilisez l'encodage UTF-8 pour éviter les problèmes d'accents
5. **Séparateur CSV** : Utilisez la virgule (`,`) comme séparateur

## Exemple de fichier CSV

```csv
first_name,last_name,surname,gender,date_of_birth,address,parent_contact
Jean,Kabongo,Mukendi,M,15-03-2010,Avenue Lubumbashi 123,+243 123 456 789
Marie,Tshimanga,Kalala,F,20-05-2011,Boulevard Lumumba 45,+243 987 654 321
Pierre,Mwamba,Kasongo,M,10-08-2009,Rue de la Paix 78,+243 111 222 333
Sophie,Nsimba,Luamba,F,05-12-2010,Avenue Kasa-Vubu 90,+243 444 555 666
```

## Exemple de fichier Excel

Créez une feuille Excel avec les mêmes colonnes en en-tête :

| first_name | last_name | surname | gender | date_of_birth | address              | parent_contact      |
|------------|-----------|---------|--------|---------------|----------------------|---------------------|
| Jean       | Kabongo   | Mukendi | M      | 15-03-2010    | Avenue Lubumbashi 123| +243 123 456 789   |
| Marie      | Tshimanga | Kalala  | F      | 20-05-2011    | Boulevard Lumumba 45 | +243 987 654 321   |
| Pierre     | Mwamba    | Kasongo | M      | 10-08-2009    | Rue de la Paix 78    | +243 111 222 333   |
| Sophie     | Nsimba    | Luamba  | F      | 05-12-2010    | Avenue Kasa-Vubu 90  | +243 444 555 666   |

## Processus d'importation

1. **Préparer le fichier** : Créez votre fichier CSV ou Excel en respectant le format ci-dessus
2. **Ouvrir le dialogue** : Cliquez sur le bouton "Charger depuis un fichier" dans l'écran de gestion des élèves
3. **Sélectionner le fichier** : Cliquez sur "Parcourir" et sélectionnez votre fichier
4. **Vérifier les détails** : L'application affichera automatiquement :
   - Le nombre total d'élèves
   - Le nombre de garçons
   - Le nombre de filles
5. **Choisir la classe** : Sélectionnez la classe dans laquelle les élèves seront inscrits
6. **Importer** : Cliquez sur "Importer" pour valider l'importation

## Validation des données

L'application effectue les validations suivantes :

- ✅ Vérification du format de fichier (CSV ou Excel uniquement)
- ✅ Vérification de la présence des colonnes requises
- ✅ Vérification du format de la date de naissance
- ✅ Vérification de la valeur du sexe (M ou F)
- ✅ Création automatique de l'inscription dans la classe sélectionnée

## Gestion des erreurs

- Si une ligne contient des données invalides, elle sera ignorée et l'importation continuera pour les autres lignes
- Un message de confirmation indiquera le nombre d'élèves importés avec succès
- En cas d'erreur, un message détaillé sera affiché

## Conseils

1. **Testez avec un petit fichier** : Commencez par importer 2-3 élèves pour vous assurer que le format est correct
2. **Vérifiez les doublons** : L'application ne vérifie pas automatiquement les doublons, assurez-vous de ne pas importer le même élève plusieurs fois
3. **Sauvegardez vos données** : Gardez une copie de votre fichier source
4. **Utilisez Excel pour la préparation** : Excel facilite la gestion des données et peut être exporté en CSV

## Support

En cas de problème avec l'importation, vérifiez :

- Le format de votre fichier
- L'encodage (UTF-8 pour CSV)
- La présence de toutes les colonnes requises
- Le format des dates
- Les valeurs du sexe (M ou F uniquement)

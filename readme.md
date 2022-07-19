[![MIT licensed](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![Gitter](https://badges.gitter.im/Elounda_Market/community.svg)](https://gitter.im/Elounda_Market/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/johnkommas/Elounda_Market)](SCORE)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/johnkommas/Elounda_Market)](CODE_SIZE)
[![GitHub forks](https://img.shields.io/github/forks/johnkommas/Elounda_Market?style=social)](FORKS)
[![GitHub issues](https://img.shields.io/github/issues/johnkommas/Elounda_Market)](ISSUES)
[![GitHub last commit](https://img.shields.io/github/last-commit/johnkommas/Elounda_Market)](COMMIT)
[![GitHub language count](https://img.shields.io/github/languages/count/johnkommas/Elounda_Market)](LANGUAGES)
[![GitHub top language](https://img.shields.io/github/languages/top/johnkommas/Elounda_Market)](lang)

# Barcode Form Print Generator 

---
### SQL Ανάγνωση Κωδικών ειδών.
###### Eφαρμογή D-Net Mobile 
- Απογραφή ΑΠ-ΜΟΒ <b>ΧΧΧΧ</b>

###### Το ερώτημα στη βάση δεδομένων επιστρέφει:
- Barcode
- Περιγραφή
- Μονάδα Μέτρησης
- Τιμή Πώλησης Καταστήματος

###### Πίνακες Entersoft Database
- <b>IMP_MobileDocumentLines </b>
- IMP_MobileDocumentHeaders 
- ESFIItem 
    
    

### Δημιουργία Αρχείων `{barcode}.svg` στον Φάκελο `svg` <br>
- Τα αρχεία αποθηκεύονται στην μορφή `<κωδικός>.svg`
- Ο φάκελος που φιλοξενεί τα αρχεία ονομάζεται `svg`
```python
def app(codes, folder='svg'):
    # codes are the barcodes of items 
    # folder is predifined
    ...
```

### Διαγραφή Αρχείων μέσα στον Φάκελο `svg`
- Όλα τα αρχεία που βρίσκονται μέσα στο φάκελο 'svg' διαγράφονται.
```python
def delete_all_files_inside_folder(folder=f'{path}/svg'):
    # folder is predifined
    ...
```

### Contributors

- Ioannis E. Kommas


#### Thank you to everyone who has contributed to the Pipedream codebase. We appreciate you!

<a >
  <img src="https://github.com/johnkommas/CodeCademy_Projects/blob/master/img/dart_images/b.png?raw=true" />
</a>



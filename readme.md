
[![MIT licensed](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/johnkommas/BarcodeReader.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/johnkommas/BarcodeReader/context:python)[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/johnkommas/BarcodeReader)](CODE_SIZE)
[![GitHub forks](https://img.shields.io/github/forks/johnkommas/BarcodeReader?style=social)](FORKS)
[![GitHub issues](https://img.shields.io/github/issues/johnkommas/BarcodeReader)](ISSUES)
[![GitHub last commit](https://img.shields.io/github/last-commit/johnkommas/BarcodeReader)](COMMIT)
[![GitHub language count](https://img.shields.io/github/languages/count/johnkommas/BarcodeReader)](LANGUAGES)
[![GitHub top language](https://img.shields.io/github/languages/top/johnkommas/BarcodeReader)](lang)
[![Join the chat at https://gitter.im/johnkommas/Welcome](https://badges.gitter.im/johnkommas/Welcome.svg)](https://gitter.im/johnkommas/Welcome?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
---

# Barcode Form Print Generator 


### SQL Ανάγνωση Κωδικών ειδών.
###### Eφαρμογή D-Net Mobile 
- Απογραφή ΑΠ-ΜΟΒ <b>ΧΧΧΧ</b>

###### Το ερώτημα στη βάση δεδομένων επιστρέφει:
- Barcode (DISTINCT)
- Περιγραφή
- Ποσότητα (SUM)
- Κατηγορία
- Μονάδα Μέτρησης
- Τιμή Πώλησης Καταστήματος
- Τιμή 1
- Τιμή 2

###### Πίνακες Entersoft Database
- <b>IMP_MobileDocumentLines </b>
- IMP_MobileDocumentHeaders 
- ESFIItem 
- ESFIZItemCategory
- ESMMItemMU

###### Φίλτρα
- Έτος == Τρέχον Έτος (const)
- Αριθμός Παραστατικού: (modal view on Slack)
- Τύπος Παραστατικού: (modal view Slack)

###### Ταξινόμηση
- Κατηγορία (1st)
- Περιγραφή (2d)

```python
def data_query(input_param, type_of_forma):
    return f"""
    SELECT ...
    """
```

```python
def get_info_from_database(mobile_document_header_code, order_type):
    # mobile_document_header_code => the number
    # order_type => the type
    ...
```    

---

### Δημιουργία Αρχείων `{barcode}.svg` στον Φάκελο `svg` <br>
- Τα αρχεία αποθηκεύονται στην μορφή `<κωδικός>.svg`
- Ο φάκελος που φιλοξενεί τα αρχεία ονομάζεται `svg`
```python
def app(codes, folder='svg'):
    # codes are the barcodes of items 
    # folder is predifined
    ...
```

---

### Διαγραφή Αρχείων μέσα στον Φάκελο `svg`
- Όλα τα αρχεία που βρίσκονται μέσα στο φάκελο 'svg' και 'merged_images' διαγράφονται.
```python
def delete_all_files_inside_folder(folder):
    # folder is predifined
    ...
```

---

### SLACK GETTER
- Επιστρέφει πληροφορίες χρήστη κατά τη διεπαφή.
- με χρήση `event` (κυρίως σε View Channel)
```python
def get_user_details(event, client):
    user_id = event["user"]
    ...
```
- με χρήση `body` (κυρίως σε Button Triggers)
```python
def get_modal_user_details(body, client):
    user_id = body['user'].get('id')
    ...
```

---

### SLACK HOME PAGE
- Δέχεται Βασικές Πληροφορίες του Χρήστη
  - Link
  - Title
  - Status
  - Image
- Ελέγχει τα δικαιώματα 
```python
if user_info['user'].get('is_admin')
```
- Επιστρέφει αποτελέσματα βάσει τύπο χρήστη

---

### SLACK MODAL
- Επιστρέφει το modal view που ενεργοποιείτε όταν πατηθέι το κουμπί.
```python
def modal_view():
    return ...
```
### Contributors

- Ioannis E. Kommas


#### Thank you to everyone who has contributed. We appreciate you!

<a >
  <img src="https://github.com/johnkommas/CodeCademy_Projects/blob/master/img/dart_images/b.png?raw=true" />
</a>



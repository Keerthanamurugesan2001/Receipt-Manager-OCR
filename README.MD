# Receipt Manager OCR    
A solution for receipt management that leverages OCR/AI technology to extract and store receipt details.

## SetUP

### Clone the repo

`git clone https://github.com/Keerthanamurugesan2001/Receipt-Manager-OCR.git`

## Install all the requirements.txt

`pip install -r requirement.txt`

API Specifications
The solution should expose a set of REST APIs for receipt management. You may use any web framework and implement the APIs with or without an ORM.

1. **/upload (POST)**

Uploads a receipt file (PDF format only).
Stores metadata in the receipt_file table.

2. **/validate (POST)**

Validates whether the uploaded file is a valid PDF.
Updates is_valid and invalid_reason fields in the receipt_file table.

3. **/process (POST)**

Extracts receipt details using OCR/AI.
Stores extracted information in the receipt table.
Marks is_processed as True in the receipt_file table.

4. **/receipts (GET)**

Lists all receipts stored in the database.

5. **/receipts/{id} (GET)**

Retrieves details of a specific receipt by its ID.

6. **/**

Swagger api documentation


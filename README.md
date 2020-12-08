# InvoiceOCR

## Overview

- This project is to extract the necessary information from the invoice pdf with the non-searchable document using Google 
Vision API and develop the user-friendly UI using Flask as a backend and mysql as a database.

## Structure

- src

    The main source code for the information extraction, database management, image processing
    
- static

    The javascript & css source code for UI
    
- templates

    The html source code for UI
    
- utils

    * The credential key for Google Vision
    * The model for various types of invoices
    * The source code for Google Vision API & file management

- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings

    Several settings for server & database
    
## Installation

- Environment

    Ubuntu 18.04, Python 3.6
    
- Dependency Installation

    Please navigate to this project directory and run the following command in the terminal
    
    ```
        pip3 install -r requirements.txt
    ```

## Execution
  
- Please run the following commands.

    ```
        python3 app.py
    ```

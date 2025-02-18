EASY DELIVERY API 
-------------------------

This module provides an API connexion between ODOO and EASY-DELIVERY.COM.
It is used to retrieve informations for creating and printing a PDF or ZPL labels.

CONFIGURATION
-------------------------

- The API configuraiton menu is located at Inventory/Configuration/Easy Delivery API Configuration
- Configure the URL and the auth token
- Only ONE active configuration accepted at a time

USAGE
-------------------------
- The button "Easy Delivery Retrieve Label" is available on the form view of the deliveries
- Clic on the button to launch the API request
- Create a PDF or ZPL labels depending on the request's response
# RIDIV

Project Configuration
Install required dependencies by running the following commands:


    pip install django-restframework

Set up the Django project and apps by running the necessary migrations. Navigate to the project directory containing the manage.py file and execute the following command:

    python manage.py makemigrations
    python manage.py migrate
Once the migrations have been applied successfully, start the Django development server:

shell
Copy code


    python manage.py runserver
The server should now be running at http://localhost:8000.

There are 2 URLS:


    BaseURL/invoices/

It server the create and list API for model invoices. Hitting this api with POST method and all information in payload will create an object for invoice model as well as an object for invoice_detail models associated with it. And hitting this API with GET mthod will list all invoices and all objects of invoice detail associated with it 


    BaseURL/invoices/{int:pk}/

It serves the Retrieve Update and Destroy API for both models in the, hitting this api with GET method will retrieve the particular invoice and invoice_detail attached to it. Hitting this with PATCH method will update all fields mentioned in payload irrespective of it is field of invoice or invoice_details. Hitting it with DELETE method will destroy the invoice and invoice_details attached to it.
    

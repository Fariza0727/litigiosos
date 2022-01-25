*********************** Our APP ***********************

we used django 3.1.6, python 3.8.5,  bootstrap 4.5.3, jquery 3.5.1 in our app.
also we used debug mode in local environment, so we can find issue easily and fix it.


1.  you have to install python or anaconda on your pc or server.


2.  Instalar dependencias con pip. (Si estas usando entorno virtual recuerda activarlo)
    pip install -r requirements/local.txt

3.  Realizar las migraciones
    python manage.py makemigrations
    python manage.py makemigrations cities_light
    python manage.py makemigrations authentication
    python manage.py makemigrations website

    python manage.py migrate
    python manage.py loaddata paymentintegration/authentication/data/users.json
    python manage.py loaddata paymentintegration/authentication/data/sites.json
    python manage.py loaddata paymentintegration/authentication/data/socialaccount.json
    python manage.py loaddata paymentintegration/authentication/data/cities_light_country.json
    python manage.py loaddata paymentintegration/authentication/data/cities_light_region.json
    python manage.py loaddata paymentintegration/authentication/data/cities_light_city.json

    python manage.py cities_light --force-all
    <!-- python manage.py makemigrations administrate -->
    

4.  python manage.py runserver

    


5.  email: admin@admin.com
    password: admin!@#
    username: admin
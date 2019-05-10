release: python manage.py migrate
release: python manage.py init_food_db --category chips --category glace --category pizza --category chocolat --nb_products 500
web: gunicorn PurBeurre.wsgi

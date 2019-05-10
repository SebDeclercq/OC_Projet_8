release: python manage.py migrate
release: python manage.py init_food_db --category "chips,glace,pizza,chocolat" --nb_products 500
web: gunicorn PurBeurre.wsgi

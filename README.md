# edirTIC31_main_courante
Dépôt de l'EDIR-TIC de la DDUS31 lié au dévelopemment de la main courante

# Utilisation de django

Il vous faut Python >= 3.4, pip, et éventuellement virtualenv, voire virtualenvwrapper ou virtualfish. Il peut vous falloir également bower.

```bash
git clone https://github.com/edirTIC31/edirTIC31_main_courante
cd edirTIC31_main_courante
git submodule init
git submodule update
cd django
pip install -U -r requirements.dev.txt  # installation des dépendances
./manage.py migrate  # création du schéma de la base de données
./manage.py createsuperuser  # création d’un superuser
./manage.py runserver
```

Ensuite, vous pouvez aller sur http://localhost:8000/, vous logger et créer un évènement.

## API REST

cf ``docs/maincourante/api.rst``.

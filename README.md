# Immortal Fighters
Rewrite of old immortalfighters.net website with Django and modern technologies.

### Description

Immortal Fighters is a role-playing site using DrD system.
It provide functionality to manage character, quests, guilds, market, forums and other character or player focused modules.

Implementation of DrD mechanics is based on rulebooks: Dračí doupě - Altar, ver.: 1.6e

### How to setup

IF project uses Django and PostgreSQL as database. Whole project is configured to run in pipenv.

1. Install Python (version >= 3.6)
2. Install pipenv
  ```
  pip install pipenv
  ```
3. Install docker (for tests).
4. Install PostgreSQL:
   1. Setting up PostgreSQL for tests:
    ```
    docker run
    -p 5433:5432
    --env POSTGRES_USER=postgres
    --env POSTGRES_PASSWORD=postgres
    --env POSTGRES_DB=postgres
    --name postgres
    postgres:10.5 
    ```
    
   2. How to setup PostgreSQL on Ubuntu: https://help.ubuntu.com/lts/serverguide/postgresql.html
   https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
5. Clone project:
  ```
  git clone https://github.com/Sanquira/immortalfighters.git
  ```
6. Initialize pipenv:
  ```
  cd immortalfighters
  pipenv install
  ```
7. When running manage.py:

  Set env variable: `DJANGO_SETTINGS_MODULE`
  * Development:
  `immortalfighters.settings.development`
  * Production:
  `immortalfighters.settings.production`
  * Tests:
  `immortalfighters.settings.tests`
  
  Ex.:
  `DJANGO_SETTINGS_MODULE=immortalfighters.settings.production pipenv run python manage.py collectstatic`
  
8. When deploying on production run these:
  ```bash
  export DJANGO_SETTINGS_MODULE=immortalfighters.settings.production
  pipenv run python manage.py migrate
  pipenv run python manage.py compilescss
  pipenv run python manage.py collectstatic
  service daphne restart
  service nginx restart
  ```

(You should have script for this on production server, at least we do)

### Q&A
**Q:** Why we do not have statistics in right menu?
> A: Middleware

**W:** Why we do not have login form in right menu?
> A: We use bootstrap forms. Also login has redirect feature.

## 1.Introduce
**This is an Api server for Photo sharing social network like Instagram built with Django REST Framework and deployed to Heroku.** 

**I made this app to practice Django Framework.**

Link App: https://django-instagram-api.herokuapp.com/  
Link Postman API:
## 2.Features
***Current***  
1. **Authentication**
- Authenticate with JWT 
- Social Oauth With Facebook and Google
2. **Posts**  
- Create, Retrieve, List, Update, Delete
- Like, Comment

***Incoming***
- Follow User

## 3.Some packages used
- https://github.com/davesque/django-rest-framework-simplejwt
- https://github.com/RealmTeam/django-rest-framework-social-oauth2
- https://github.com/joke2k/django-environ
- https://github.com/django-extensions/django-extensions
- https://github.com/jschneier/django-storages
- https://github.com/rsinger86/drf-access-policy
- https://github.com/jazzband/django-debug-toolbar

## 4. Installation
1. Install python packages 
  `pip install -r requirements.txt`
2. Setup  
    `python manage.py reset_app`  
   `python manage.py collectstatic`
3. Run app  
- `python manage.py runserver` or  
- config var in `.example-env` and run
   `ENV_PATH=instagram/.example-env python manage.py runserver`


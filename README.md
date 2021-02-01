## URL Shortener ✨
Simple and powerful URL shortener written in Python using Django 3.1.5.

### Features:
- URL Shortening
- Admin interface
- Error Handling
- Cool looking Design 🔥 (Bootstrap)

### URL Shortening Features:
- Protected routes
- Expiration date (7 days)
- Maximum number of views (20 views)
- View the statistics for each short URLs.

## How to run?

1. Clone repo & cd into it
2. ```pipenv install``` - installs required packages
3. Configure .env file (if needed).
4. ```manage.py makemigrations``` create migrations and then migrate by ```manage.py migrate```.
5. ```manage.py createsuperuser``` to create an admin user.
6. ```manage.py runserver ip:port``` run server.

## Routes

1. `/admin/` - admin interface.
2. `/<short_url>/` - shorten URL.
3. `/info/<short_url>/` - shorten URL statistics and information.

## Photos 💈

* Main interface
<img src="https://i.gyazo.com/3ab9e0e84007b411c18ffd1a5265642c.png" alt="photo1"/>

* After generating a new URL
<img src="https://i.gyazo.com/c9130107d83ffafc19527186b778e270.png" alt="photo2"/>

* Information about short URL
<img src="https://i.gyazo.com/82bcde164bc2308d407597763f824ac9.png" alt="photo3"/>

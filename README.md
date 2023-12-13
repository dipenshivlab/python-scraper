## Installation
```bash
pip3 install -r requirements.txt
```

## Add to installed apps:
``` bash
INSTALLED_APPS = [
    # General use templates & template tags (should appear first)
'adminlte3',
    # Optional: Django admin theme (must be before django.contrib.admin)
'adminlte3_theme',

...

]
```

## For Virtual Env follow this link

https://stackoverflow.com/questions/55142774/how-to-activate-virtual-environment-in-django



## Run Code

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```


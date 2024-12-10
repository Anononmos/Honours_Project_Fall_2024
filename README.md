# Honours_Project_Fall_2024

# Credits

Author:         Ainan Kashif\
Supervisor:     Prof. Darryl Hill

## Outline

This project is accessible on the website http://ainan.pythonanywhere.com. There, you can upload and watch the videos you uploaded. To share an uploaded video, copy and paste its URL. The website will expire 

There is also an administrator webpage whose login is accessible through the http://ainan.pythonanywhere.com/admin endpoint. 

## To setup the Code onto your Local Device:

1. Set up and activate a Python virtual environment to install the required libraries.

2. Run "pip install -r requirements.txt" followed by "python manage.py migrate"

3. Create a local .env file in the topmost /honours_project directory:

```
DJANGO_SECRET_KEY="Any long, random string."
DJANGO_DEBUG=True   # Set for development mode

EXPIRY=10       # In minutes. Dictates when uploaded videos become inaccessible after upload.
TIME_LIMIT=60   # In seconds. Maximum duration of video file uploads.
SIZE_LIMIT=50   # In MB. Maximum file size of video file uploads.
```

4. In the settings.py file:

    1. Comment the ```ALLOWED_HOSTS``` variable. Add a new line setting ```ALLOWED_HOSTS = []```.
    2. Comment the ```CSRF_TRUSTED_ORIGINS``` variable.
    3. Comment the whitenoise middleware in the ```MIDDLEWARE``` variable.
    4. Comment the ```STORAGES``` variable.

## To Run the Development Server: 

Run the following command:

```python manage.py runserver```

## To Run the Unit Tests:

Run the following command:

```python manage.py test clip_sharing_app.tests```

## To Run a Unit Test File within the /tests Folder:

Run the following commmand:

```python manage.py test clip_sharing_app.tests.test_views```

## To Run a Unit Test Class:

```python manage.py test clip_sharing_app.tests.test_views.UploadPageTest```

## To Run a Single Unit Test:

```python manage.py test clip_sharing_app.tests.test_views.WatchPageTest.test_no_id```

## To Delete Expired Entries on the Database:

```python manage.py delete_expired```

## To Access the Administrator Site and the PythonAnywhere Account

The login information is included in the Honours_Admin.txt file in the Design-documents folder.
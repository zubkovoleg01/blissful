Blissful social network.

This is a django web application for publishing posts and subscriptions to authors of interest.

________________________________________________________________________________________________________________________________________________________


● Registration and authentication:

Users can register and authenticate in the system.

● User profiles:

Users have their own profiles with the ability to edit.

● Communities:

Users can view community posts and create them.

● Communication:

Users can subscribe to each other.

● Content:

Users can post, edit or delete them posts.

● Pagination:

All content using a pagionation.

________________________________________________________________________________________________________________________________________________________

Deployment Instructions

● Installing dependencies:

pip install -r requirements.txt

● Creating migrations and applying:

python manage.py makemigrations python manage.py migrate

● Creating a superuser (for the administrative panel):

python manage.py createsuperuser

● Starting the server:

python manage.py runserver

● Administrative panel:

Go to http://localhost:8000/admin and log in using the superuser credentials.

● Adding Posts or Community:

In the admin panel, you can add and edit information about posts or community.




from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import myapp.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    # path("", myapp.views.index, name="index"),
    path("db/", myapp.views.db, name="db"),
    path("admin/", admin.site.urls),
    # path("", myapp.views.index, name="index"),

    path("", include('myapp.urls')),
]


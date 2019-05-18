from django.urls import path, include
from .views import templistview, templistview2, templistview3, tempdetailtview, tempcreatetview, tempupdatetview
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", views.index, name="index"),
    path("webmail/<wmlarg>/", views.webmail, name="webmail"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.uprofile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='index.html'), name="logout"),
    path("start/", views.start, name="start"),
    path("startspam/", views.startspam, name="startspam"),
    # path("stop/", views.stop, name="stop"),
    path("on/", views.on, name="on"),
    path("off/", views.off, name="off"),
    path("templates/", templistview.as_view(), name="templist"),
    path("templates2/", templistview2.as_view(), name="templist2"),
    path("templates3/", templistview3.as_view(), name="templist3"),
    path("templates/<int:pk>/", tempdetailtview.as_view(), name="tempdetail"),
    path("templates/new", tempcreatetview.as_view(), name="tempcreate"),
    path("templates/<int:pk>/update", tempupdatetview.as_view(), name="tempupdate"),
    path("maillist/", views.maillist, name="maillist"),
    path("maillistget/", views.maillistget, name="maillistget"),
    path("blacklist/", views.blacklist, name="blacklist"),
    path("blocking/<adddelarg>/<mailarg>/", views.blocking, name="blocking"),
    path("sentlist/", views.sentlist, name="sentlist"),
    path("failedlist/", views.failedlist, name="failedlist"),
    path("waitinglist/", views.waitinglist, name="waitinglist"),
    
]
 # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
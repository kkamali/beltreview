from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'register$', views.register, name = "register"),
    url(r'login$', views.login, name = "login"),
    url(r'books/add$', views.add, name = "new"),
    url(r'books/create$', views.create, name = "create"),
    url(r'books/(?P<book_id>\w+)/$', views.display, name = "display"),
    url(r'delete$', views.delete, name = "delete"),
    url(r'destroy/(?P<review_id>\w+)/$', views.destroy, name = "destroy"),
    url(r'add_review$', views.add_review, name = "add_review"),
    url(r'users/(?P<user_id>\w+)/$', views.display_user, name = "display_user"),
    url(r'logout$', views.logout, name = "logout"),
    url(r'home$', views.home, name = "home")
]

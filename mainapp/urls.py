from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig


app_name = MainappConfig.name


urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('courses_list/', views.CoursesListView.as_view(), name='courses_list'),
    path('doc_site/', views.DocSiteView.as_view(), name='doc_site'),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('search/', views.google_redirect_view, name='search'),
]

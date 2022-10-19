from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig


app_name = MainappConfig.name


urlpatterns = [
    path('contacts/', views.ContactsView.as_view()),
    path('courses_list/', views.CoursesListView.as_view()),
    path('doc_site/', views.DocSiteView.as_view()),
    path('', views.IndexView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('news/', views.NewsView.as_view()),
]


from django.urls import path,include
from . import views
urlpatterns = [

     path('', views.home, name='home'),
     path('register/', views.register_page, name='register-page'),
     path('login/', views.login_page, name='login-page'),
     path("logout/",views.logout_page,name="logout-page"),

     path('add-password/', views.add_new_password, name="add-password"),
     path('manage-passwords/', views.manage_passwords, name="manage-passwords"),
     path('edit-password/<str:pk>/', views.edit_password, name="edit-password"),
     # path for generating random password
    path('generate-password/',views.generate_password, name='generate-password'),
]

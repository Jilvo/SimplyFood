"""Simplyshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipe_list import views as recipe_list_views
from manage_user import views as manage_user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("pdf",recipe_list_views.weasyprint, name="pdf"),
    path("", recipe_list_views.home_function, name="index"),
    path("tab",recipe_list_views.recipe_table, name= "tab"),
    path("404", manage_user_views.page_not_found_view,name="404"),
    path("500", manage_user_views.page_internal_error,name="500"),
    path("legal_mention", recipe_list_views.legal_mention, name='legal_mention'),
    path("login", manage_user_views.connexion, name="login"),
    path("login_page",manage_user_views.page_signin,name="login_page"),
    path("logout", manage_user_views.logout_view, name="logout"),
    path("signup", manage_user_views.register, name="signup"),
    path("history", recipe_list_views.see_history, name="history"),
    path("recipe", recipe_list_views.find_ingredients, name="recipe"),
    path("name_recipe", recipe_list_views.find_name_recipe, name="name_recipe"),
    
]

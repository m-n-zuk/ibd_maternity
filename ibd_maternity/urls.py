"""ibd_maternity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from ibd_website import views as wv
from ibd_visits import views as vv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', wv.MainView.as_view()),
    path('register/', wv.RegisterView.as_view()),
    path('register_details/<str:role>/<int:id>/', wv.RegisterDetailsView.as_view()),
    path('login/', wv.LoginView.as_view()),
    path('logout/', wv.LogoutView.as_view()),
    path('user/', wv.UserView.as_view()),
    path('community/', wv.CommunityView.as_view()),
    path('doctors/', wv.DoctorsView.as_view()),

    path('add_visit/', vv.AddVisitView.as_view()),
    # path('book_visit/<int:id_doc>/<int:id_pat>', vv.BookVisitView.as_view()),
    # path('visits/<int:id>', vv.VisitsView.as_view()),

]

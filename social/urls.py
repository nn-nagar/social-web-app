# """dj2django URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path

from social import views
from django.views.generic import RedirectView

from social.views import ContactView, AboutView, HomeView

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('about/', AboutView.as_view()),
    path('contact/', ContactView.as_view()),
    # path('mylist/',MyList.as_view()),
    # path('question/create/', QuestionCreate.as_view(success_url="/college/home/")),
    # path('notice/<int:pk>', NoticeDetailView.as_view()),
    # path('notice/', NoticeListView.as_view()),
    # path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(success_url="/college/home/")),
    path('', RedirectView.as_view(url='home/')),

]

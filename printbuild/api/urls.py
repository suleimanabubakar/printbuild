from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('spares',SpareView.as_view()),
    path('update/<transno>',SpareUpdate.as_view()),
    path('spares/<transno>',SpareEach.as_view()),
    path('printTest/',PrintView)
]
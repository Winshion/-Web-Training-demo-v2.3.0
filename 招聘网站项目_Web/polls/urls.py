from os import name
from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_main_page),
    path('wordcloud/', views.show_wordcloud),
    path('form/', views.show_form),
    path('cpny_wc/', views.show_cpny_wordcloud),
    path('barplot/', views.show_barplot),
    path('bubble/', views.show_bubble),
    path('boxplot/', views.show_boxplot),
    path('intro/', views.show_intro),
    path('test/', views.test),
    path('search/', views.search_button),
    path('craw/', views.craw),
]

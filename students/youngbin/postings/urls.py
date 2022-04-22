from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.PostingView.as_view()),
]

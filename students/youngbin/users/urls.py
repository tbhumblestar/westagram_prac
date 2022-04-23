from django.urls import path,include
from . import views
        
urlpatterns = [
    path('/signup',views.SignUpView.as_view()),
    path('/signin',views.SignInView.as_view()),
    path('/like',views.LikeView.as_view()),
]
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.PostingView.as_view()),
    path('/<int:posting_id>/comment',views.CommentView.as_view()),
    path('/<int:posting_id>/like',views.LikeView.as_view()),
]

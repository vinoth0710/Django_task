from django.urls import path
from Quora import views

app_name = "Quora"

urlpatterns = [
    # URL pattern for user registration
    path('Register/', views.registration, name='register'),

    # URL pattern for user login
    path('', views.user_login, name='login'),

    # URL pattern for user logout
    path('user_logout/', views.user_logout, name='user_logout'),

    # URL pattern for the user dashboard
    path('Dashboard/', views.user_dashboard, name='user_dashboard'),

    # URL pattern for saving question details
    path('save_question_details/', views.save_question_details, name='save_question_details'),

    # URL pattern for getting answers
    path('get_answers/', views.get_answers, name='get_answers'),

    # URL pattern for adding an answer
    path('add_answer/', views.add_answer, name='add_answer'),

    # URL pattern for liking or unliking an answer
    path('like-unlike-answer/<int:answer_id>/', views.like_unlike_answer, name='like_unlike_answer'),
]

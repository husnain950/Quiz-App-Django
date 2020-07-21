from django.urls import include, path

from QuizApp import views

urlpatterns = [
    path('result_details/<int:quiz_pk>/student/<int:student_pk>/', views.result_details, name='result_details'),
    path('', views.home, name='home'),
    path('signout', views.logout_view, name='signout'),
    path('signup', views.signup, name='signup'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('add/', views.add_quiz, name='add_quiz'),
    path('quiz/<int:quiz_pk>/', views.quiz_details, name='quiz_details'),
    path('quiz/question_detail/<int:question_pk>/', views.question_detail, name='question_detail'),
    path('quiz/add_options/<int:question_pk>/', views.add_options, name='add_options'),
    path('quiz/add_question/<int:quiz_pk>/', views.add_question, name='add_question'),
    path('take_quiz/<int:quiz_pk>/', views.take_quiz, name='take_quiz'),
    path('edit_question/<int:question_pk>/', views.edit_question, name='edit_question'),
    path('edit_options/<int:question_pk>/', views.edit_options, name='edit_options'),
    path('delete_question/<int:question_pk>/', views.delete_question, name='delete_question'),
    path('delete_quiz/<int:quiz_pk>/', views.delete_quiz, name='delete_quiz'),
    path('result/<int:quiz_pk>/', views.quiz_result, name='quiz_result'),
    path('student_home', views.student_home, name='student_home'),
    path('result_view', views.result_view, name='result_view'),
    path('report_view/<int:quiz_pk>/', views.report_view, name='report_view'),
    path('publish_quiz/<int:quiz_pk>/', views.publish_quiz, name='publish_quiz'),
    path('offline_quiz/<int:quiz_pk>/', views.offline_quiz, name='offline_quiz'),
]

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('my-results/', views.my_results, name='my_results'),
    path('my-results/<int:attempt_id>/', views.attempt_detail, name='attempt_detail'),
    path('<slug:course_slug>/quiz/', views.take_course_quiz, name='take_course_quiz'),
    path('<slug:course_slug>/module/<slug:module_slug>/quiz/', views.take_module_quiz, name='take_module_quiz'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/quiz/', views.take_quiz, name='take_quiz'),
]
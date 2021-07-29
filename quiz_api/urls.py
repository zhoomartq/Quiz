from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quiz_api import views


router = DefaultRouter()

router.register('quizzes', views.QuizViewSet)
router.register('quizzes/(?P<id>\d+)/questions', views.QuestionViewSet, basename='questions')

router.register('quizzes/(?P<id>\d+)/questions/(?P<question_pk>\d+)/choices', views.ChoiceViewSet, basename='choices')

router.register('all_quizzes', views.QuizListViewSet)
router.register('quizzes/(?P<id>\d+)/questions/(?P<question_pk>\d+)/answers', views.AnswerViewSet, basename='answers')

router.register('user_quizzes', views.UserListViewSet, basename='user_list')

urlpatterns = [
    path('', include(router.urls))
]
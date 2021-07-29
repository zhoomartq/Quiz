from rest_framework import viewsets, mixins, permissions
from rest_framework.generics import get_object_or_404
from .models import *
from .serializers import *

from datetime import datetime
from django.db.models import Q


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.IsAdminUser, )


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, id=self.kwargs['id'])
        return quiz.questions.all()

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['id'])
        serializer.save(quiz=quiz)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        question = get_object_or_404(Question, id=self.kwargs['question_pk'])
        return question.choices.all()

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'], quiz__id=self.kwargs['id'])
        serializer.save(question=question)


class AnswerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_serializer_class(self):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'], quiz__id=self.kwargs['id'])

        if question.type == 'text_answer':
            return TextSerializer
        elif question.type == 'one_answer':
            return OneAnswerSerializer
        else:
            return MultipleAnswersSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'], quiz__id=self.kwargs['id'])
        serializer.save(user=self.request.user, question=question)


class QuizListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Quiz.objects.filter(end__gte=datetime.today())
    serializer_class = QuizSerializer
    permission_classes = (permissions.AllowAny, )


class UserListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserQuizSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Quiz.objects.exclude(~Q(questions__answers__user__id=user_id))
        return queryset







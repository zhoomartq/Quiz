from rest_framework import serializers
from .models import *
from django.db.models import Q



class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'title']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionListSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        model = Question
        fields = ['title', 'answers']

    def get_answers(self, question):
        user_id = self.context.get('request').user.id
        answers = Answer.objects.filter(Q(question=question) & Q(user__id=user_id))
        serializer = AnswerSerializer(instance=answers, many=True)
        return serializer.data


class UserQuizSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = '__all__'



class UserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        question_id = self.context.get('request').parser_context['kwargs'][
            'question_pk']
        request = self.context.get('request', None)
        queryset = super(UserPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)



class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text_answer']


class OneAnswerSerializer(serializers.ModelSerializer):
    one_answer = UserPrimaryKeyRelatedField(many=False, queryset=Choice.objects.all())

    class Meta:
        model = Answer
        fields = ['one_answer']


class MultipleAnswersSerializer(serializers.ModelSerializer):
    multiple_answers = UserPrimaryKeyRelatedField(many=True, queryset=Choice.objects.all())

    class Meta:
        model = Answer
        fields = ['multiple_answers']












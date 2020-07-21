from django import forms
from django.contrib.auth.forms import UserCreationForm

from QuizApp.models import User, Question, Quiz


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'is_teacher', 'is_student', 'gender')


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

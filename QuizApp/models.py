from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    objects = UserManager()

    def __str__(self):
        return self.email


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField('publish', default=False)

    class Meta:
        verbose_name_plural: 'Quizzes'

    def __str__(self):
        return f'{self.owner.username} {self.name}'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField('Question', max_length=255)

    def __str__(self):
        return f'{self.quiz.name} {self.text}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return f'{self.question.text} {self.text}'


class Result(models.Model):
    taken_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural: 'TakenQuizzes'

    def __str__(self):
        return f'{self.taken_by.email} {self.quiz.name} {self.score}'


class AnswerOption(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Attempted')
    answer = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='Choosed')

    def __str__(self):
        return f'{self.question.quiz.name} {self.question.text} {self.answer.text}'

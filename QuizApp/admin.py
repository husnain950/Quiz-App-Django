from django.contrib import admin

from QuizApp.models import  Option, User, Question, AnswerOption, Result, Quiz



class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date', 'total_questions')

    def total_questions(self, obj):
        return f'{obj.questions.all().count()}'


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_options')

    def question_options(self, obj):
        options = obj.answers.all()
        return f'A. {options[0]} B. {options[1]} C. {options[2]} D. {options[3]} '


class ResultAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'taken_by', 'score', 'date']


class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')


class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answer', 'is_correct')

    def is_correct(self, obj):
        return obj.answer.is_correct


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(AnswerOption, AnswerOptionAdmin)
admin.site.register(User)

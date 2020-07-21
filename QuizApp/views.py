import datetime
import random

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_control
from QuizApp.forms import QuizForm, QuestionForm, CustomUserCreationForm
from QuizApp.models import Option, User, Question, AnswerOption, Result, Quiz


def signup(request):
    if request.method == 'POST':
        t = True if request.POST.get('desig') == 'T' else False
        s = True if request.POST.get('desig') == 'S' else False
        user = User.objects.create_user(username=request.POST.get('uname'),
                                 email=request.POST.get('email'),
                                 password=request.POST.get('pas1'),
                                 is_teacher=t,
                                 is_student=s)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# @login_required
def home(request):
    if request.method == 'POST':
        user = get_object_or_404(User,username=request.POST.get('uname'))
        if user.check_password(request.POST.get('pas')):
            login(request, user)
            if request.user.is_student:
                return redirect('student_home')
            else:
                quiz_list = Quiz.objects.filter(owner=request.user)
                return render(request, 'home.html', {'quizzes': quiz_list})
        else:
            messages.add_message(request,messages.ERROR,'Invalid Credentials')
            return render(request, 'registration/login.html')
    if request.user.is_authenticated:
        if request.user.is_student:
                return redirect('student_home')
        else:
            quiz_list = Quiz.objects.filter(owner=request.user)
            return render(request, 'home.html', {'quizzes': quiz_list})
        if request.user.is_student:
            return redirect('student_home')
        quiz_list = Quiz.objects.filter(owner=request.user)
        return render(request, 'home.html', {'quizzes': quiz_list})
    return render(request,'registration/login.html')

        

@login_required
def add_quiz(request):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.owner = request.user
            quiz.save()
        return redirect('add_question', quiz.pk)
    else:
        form = QuizForm()
    return render(request, 'add_quiz.html', {'form': form})


@login_required
def quiz_details(request, quiz_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    quiz = Quiz.objects.get(pk=quiz_pk)
    return render(request, 'quiz_details.html', {'quiz': quiz, 'questions': quiz.questions.all()})


@login_required
def add_question(request, quiz_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_id = quiz_pk
            question.save()
            return redirect('add_options', question.pk)
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form, 'quiz': get_object_or_404(Quiz, pk=quiz_pk)})


@login_required
def add_options(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if request.method == 'POST':
        option1 = {'text': request.POST.get('A'), 'is_correct': True if request.POST.get('Correct') == 'A' else False,
                   'question_id': question_pk}
        option2 = {'text': request.POST.get('B'), 'is_correct': True if request.POST.get('Correct') == 'B' else False,
                   'question_id': question_pk}
        option3 = {'text': request.POST.get('C'), 'is_correct': True if request.POST.get('Correct') == 'C' else False,
                   'question_id': question_pk}
        option4 = {'text': request.POST.get('D'), 'is_correct': True if request.POST.get('Correct') == 'D' else False,
                   'question_id': question_pk}
        Option.objects.create(**option1)
        Option.objects.create(**option2)
        Option.objects.create(**option3)
        Option.objects.create(**option4)
        return redirect('add_question', Question.objects.get(pk=question_pk).quiz.id)
    else:
        return render(request, 'add_options.html', {'question': Question.objects.get(pk=question_pk)})


@login_required
def question_detail(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    question = get_object_or_404(Question, pk=question_pk)
    return render(request, 'question_detail.html', {'question': question, 'answers': question.answers.all()})


@login_required
def take_quiz(request, quiz_pk):
    if not request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if Result.objects.filter(taken_by=request.user, quiz_id=quiz_pk).exists():
        return HttpResponseBadRequest(content='Already Taken, Cannot Retake')
    quiz_questions = [question for question in get_object_or_404(Quiz, pk=quiz_pk).questions.all() if
                      question.answers.all().count() == 4]
    if request.method == 'POST':
        submitted_ans = Option.objects.filter(pk__in=[request.POST.get(str(quiz.pk)) for quiz in quiz_questions])
        score = Option.objects.filter(id__in=[ans.id for ans in submitted_ans]).filter(is_correct=True).count()
        correct_ans = [question.answers.get(is_correct=True) for question in quiz_questions]
        quiz_solution = zip(quiz_questions, correct_ans, submitted_ans)
        Result.objects.create(taken_by=request.user, quiz_id=quiz_pk, score=score)
        for question, answer in zip(quiz_questions, submitted_ans):
            AnswerOption.objects.create(student=request.user, question=question, answer=answer)
        return render(request, 'result.html', {'quiz_sol': quiz_solution, 'score': score, 'total': len(quiz_questions), 'quiz': get_object_or_404(Quiz, pk=quiz_pk)})
    random.shuffle(quiz_questions, random.random)
    return render(request, 'take_quiz.html', {'questions': enumerate(quiz_questions, start=1)})


@login_required
def edit_question(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    form = QuestionForm(request.POST or None, instance=Question.objects.get(pk=question_pk))

    if form.is_valid():
        form.save()
        return redirect('question_detail', question_pk)
    return render(request, 'edit_question.html', {'form': form})


@login_required
def edit_options(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    answers = Question.objects.get(pk=question_pk).answers.all()
    if request.method == 'POST':
        for answer in answers:
            answer.text = request.POST.get(str(answer.pk))
            answer.is_correct = True if int(request.POST.get('correct')) == answer.pk else False
            answer.save()
        return redirect('question_detail', question_pk)
    if answers.count() == 0:
        return redirect('question_detail', get_object_or_404(Question, pk=question_pk).quiz_id, question_pk)
    return render(request, 'edit_options.html', {'answers': answers})


@login_required
def delete_question(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    question = get_object_or_404(Question, pk=question_pk)
    quiz_id = question.quiz_id
    question.delete()
    return redirect('quiz_details', quiz_id)


@login_required
def delete_quiz(request, quiz_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.delete()
    return redirect('home')


@login_required
def quiz_result(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk).taken_quizzes.all()
    return render(request, 'quiz_result.html', {'quizzes': quiz})


@login_required
def student_home(request):
    if request.user.is_teacher:
        return HttpResponseBadRequest(content='Not Authorized')
    student = request.user
    quiz_list = Quiz.objects.exclude(publish=False).exclude(
        id__in=[quiz.quiz_id for quiz in Result.objects.filter(taken_by=student)])
    return render(request, 'student_home.html', {'quizzes': quiz_list})


@login_required
def result_view(request):
    if not request.user.is_student:
        return HttpResponseBadRequest(content='Not authorized')
    results = Result.objects.filter(taken_by=request.user)
    return render(request, 'result_view.html', {'results': results})


@login_required
def result_details(request, quiz_pk, student_pk):
    result = AnswerOption.objects.filter(student_id=student_pk,
                                         question__in=get_object_or_404(Quiz, pk=quiz_pk).questions.all())
    name = get_object_or_404(User,pk=student_pk).username                
    return render(request, 'result_details.html', {'result': result, 'name': name})


@login_required
def report_view(request, quiz_pk):
    questions = get_object_or_404(Quiz, pk=quiz_pk).questions.all()
    correct_attempts = list()
    correct_ans = list()

    for question in questions:
        if question.answers.exists():
            correct_ans.append(question.answers.get(is_correct=True))

    for ans in correct_ans:
        correct_attempts.append(AnswerOption.objects.filter(answer_id=ans.pk).count())

    report = zip(correct_ans, correct_attempts)
    return render(request, 'report.html', {'report': report, 'quiz': get_object_or_404(Quiz, pk=quiz_pk)})


@login_required
def publish_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.publish = True
    quiz.date = datetime.datetime.now()
    quiz.save()
    return redirect('home')


@login_required
def offline_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.publish = False
    quiz.save()
    return redirect('home')

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import (
    Category, Course, Module, Lesson,
    Quiz, Question, Answer,
    UserAttempt, UserAnswer, Comment,
)


def course_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.annotate(course_count=Count('courses'))

    if category_slug:
        courses_qs = Course.objects.filter(category__slug=category_slug)
    else:
        courses_qs = Course.objects.all()

    total_count = Course.objects.count()

    paginator = Paginator(courses_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'total_count': total_count,
    })


@login_required
def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    first_lesson = Lesson.objects.filter(module__course=course).order_by('module__order', 'order').first()
    if first_lesson:
        return redirect('courses:lesson_detail', course_slug=course.slug, lesson_slug=first_lesson.slug)
    return render(request, 'courses/course_detail.html', {'course': course})


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, module__course=course)

    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id')
        if text:
            parent = None
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id, lesson=lesson)
            Comment.objects.create(
                lesson=lesson, author=request.user, text=text, parent=parent
            )
            return redirect(
                reverse('courses:lesson_detail', args=[course.slug, lesson.slug]) + '#comments'
            )

    # Build a flat list of all lessons in this course
    all_lessons = []
    for module in course.modules.all():
        for l in module.lessons.all():
            all_lessons.append(l)

    prev_lesson = None
    next_lesson = None
    for i, l in enumerate(all_lessons):
        if l.id == lesson.id:
            if i > 0:
                prev_lesson = all_lessons[i - 1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i + 1]
            break

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses:course_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def process_quiz_submission(request, quiz):
    score = 0
    total = quiz.questions.count()

    attempt = UserAttempt.objects.create(
        user=request.user, quiz=quiz, score=0, passed=False
    )

    for question in quiz.questions.all():
        submitted = request.POST.getlist(f'question_{question.id}')
        correct_ids = set(
            question.answers.filter(is_correct=True).values_list('id', flat=True)
        )
        submitted_ids = set(map(int, submitted)) if submitted else set()

        is_correct = submitted_ids == correct_ids
        if is_correct:
            score += 1

        user_answer = UserAnswer.objects.create(
            attempt=attempt, question=question, is_correct=is_correct
        )
        user_answer.selected.set(submitted_ids)

    percentage = int((score / total) * 100) if total else 0
    attempt.score = percentage
    attempt.passed = percentage >= quiz.passing_score
    attempt.save()
    return attempt


@login_required
def take_quiz(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, module__course=course)
    quiz = get_object_or_404(Quiz, lesson=lesson)

    if request.method == 'POST':
        attempt = process_quiz_submission(request, quiz)
        return redirect('courses:attempt_detail', attempt_id=attempt.id)

    return render(request, 'courses/take_quiz.html', {
        'quiz': quiz,
        'submit_url': reverse('courses:take_quiz', args=[course.slug, lesson.slug]),
    })


@login_required
def take_module_quiz(request, course_slug, module_slug):
    course = get_object_or_404(Course, slug=course_slug)
    module = get_object_or_404(Module, slug=module_slug, course=course)
    quiz = get_object_or_404(Quiz, module=module)

    if request.method == 'POST':
        attempt = process_quiz_submission(request, quiz)
        return redirect('courses:attempt_detail', attempt_id=attempt.id)

    return render(request, 'courses/take_quiz.html', {
        'quiz': quiz,
        'submit_url': reverse('courses:take_module_quiz', args=[course.slug, module.slug]),
    })


@login_required
def take_course_quiz(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, course=course)

    if request.method == 'POST':
        attempt = process_quiz_submission(request, quiz)
        return redirect('courses:attempt_detail', attempt_id=attempt.id)

    return render(request, 'courses/take_quiz.html', {
        'quiz': quiz,
        'submit_url': reverse('courses:take_course_quiz', args=[course.slug]),
    })


@login_required
def attempt_detail(request, attempt_id):
    attempt = get_object_or_404(UserAttempt, pk=attempt_id, user=request.user)
    return render(request, 'courses/attempt_detail.html', {'attempt': attempt})


@login_required
def my_results(request):
    attempts = UserAttempt.objects.filter(user=request.user).order_by('-created_at')
    passed_count = attempts.filter(passed=True).count()
    failed_count = attempts.filter(passed=False).count()

    if attempts.exists():
        average_score = round(sum(a.score for a in attempts) / attempts.count())
    else:
        average_score = 0

    return render(request, 'courses/my_results.html', {
        'attempts': attempts,
        'passed_count': passed_count,
        'failed_count': failed_count,
        'average_score': average_score,
    })


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'courses/quiz_list.html', {'quizzes': quizzes})
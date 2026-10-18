from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    Category, Course, Module, Lesson,
    Quiz, Question, Answer, UserAttempt,
)

class CategorySlugTests(TestCase):
    def test_slug_is_generated_from_title(self):
        category = Category.objects.create(title='Web Development')
        self.assertEqual(category.slug, 'web-development')

    def test_existing_slug_is_preserved(self):
        category = Category.objects.create(title='Web Development', slug='custom-slug')
        self.assertEqual(category.slug, 'custom-slug')


class CourseCascadeTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title='Django Basics')
        self.module = Module.objects.create(course=self.course, title='Getting Started', order=1)
        self.lesson = Lesson.objects.create(module=self.module, title='Intro', order=1)

    def test_deleting_course_deletes_modules_and_lessons(self):
        self.course.delete()
        self.assertEqual(Module.objects.count(), 0)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_deleting_category_keeps_courses(self):
        category = Category.objects.create(title='Programming')
        course = Course.objects.create(title='Python', category=category)
        category.delete()
        course.refresh_from_db()
        self.assertIsNone(course.category)


class LessonOrderingTests(TestCase):
    def test_modules_ordered_by_order_field(self):
        course = Course.objects.create(title='Test')
        Module.objects.create(course=course, title='Second', order=2)
        Module.objects.create(course=course, title='First', order=1)
        titles = list(course.modules.values_list('title', flat=True))
        self.assertEqual(titles, ['First', 'Second'])


class QuizSubmissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='test12345')
        self.client.login(username='tester', password='test12345')

        self.course = Course.objects.create(title='Django Basics')
        self.quiz = Quiz.objects.create(title='Django Quiz', course=self.course, passing_score=70)

        self.q1 = Question.objects.create(
            quiz=self.quiz, text='What is Django?', question_type='single', order=1
        )
        self.a1_correct = Answer.objects.create(question=self.q1, text='Web framework', is_correct=True)
        self.a1_wrong = Answer.objects.create(question=self.q1, text='JS library', is_correct=False)

        self.q2 = Question.objects.create(
            quiz=self.quiz, text='Which are Django components?', question_type='multiple', order=2
        )
        self.a2_first = Answer.objects.create(question=self.q2, text='ORM', is_correct=True)
        self.a2_second = Answer.objects.create(question=self.q2, text='Templates', is_correct=True)
        self.a2_wrong = Answer.objects.create(question=self.q2, text='React', is_correct=False)

    def test_single_and_multiple_scoring(self):
        response = self.client.post(
            reverse('courses:take_course_quiz', args=[self.course.slug]),
            {
                f'question_{self.q1.id}': str(self.a1_correct.id),
                f'question_{self.q2.id}': [str(self.a2_first.id), str(self.a2_second.id)],
            },
        )
        attempt = UserAttempt.objects.first()
        self.assertEqual(attempt.score, 100)
        self.assertTrue(attempt.passed)

    def test_multiple_requires_exact_match(self):
        response = self.client.post(
            reverse('courses:take_course_quiz', args=[self.course.slug]),
            {
                f'question_{self.q1.id}': str(self.a1_correct.id),
                f'question_{self.q2.id}': [str(self.a2_first.id)],
            },
        )
        attempt = UserAttempt.objects.first()
        self.assertEqual(attempt.score, 50)
        self.assertFalse(attempt.passed)


class CourseListViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Programming')
        for i in range(8):
            Course.objects.create(title=f'Course {i}', category=self.category)

    def test_pagination_splits_courses(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)

    def test_filter_by_category_returns_only_matching(self):
        other = Category.objects.create(title='DevOps')
        Course.objects.create(title='Docker', category=other)

        response = self.client.get(reverse('courses:course_list'), {'category': 'programming'})
        courses = response.context['page_obj'].object_list
        self.assertTrue(all(c.category.slug == 'programming' for c in courses))


class AuthRequiredTests(TestCase):
    def test_course_detail_requires_login(self):
        course = Course.objects.create(title='Private Course')
        response = self.client.get(reverse('courses:course_detail', args=[course.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_attempt_detail_protects_other_users_data(self):
        owner = User.objects.create_user(username='owner', password='pass12345')
        intruder = User.objects.create_user(username='intruder', password='pass12345')

        course = Course.objects.create(title='Course')
        quiz = Quiz.objects.create(title='Quiz', course=course)
        attempt = UserAttempt.objects.create(
            user=owner, quiz=quiz, score=100, passed=True
        )

        self.client.login(username='intruder', password='pass12345')
        response = self.client.get(reverse('courses:attempt_detail', args=[attempt.id]))
        self.assertEqual(response.status_code, 404)
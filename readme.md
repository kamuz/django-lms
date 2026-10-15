# Django LearnHub — покроковий гайд

## Як користуватись

- Кроки йдуть послідовно: частина коду в наступних кроках доповнює попередню
- Ранні кроки містять навчальні фрагменти; повні актуальні Python-файли наведені в додатку наприкінці README.
- Фінальні HTML-шаблони наведені у кроках 19–20 і синхронізовані з файлами репозиторію; ранні HTML-приклади — проміжні навчальні версії.
- П’ять JSON-fixture у `courses/fixtures/` наведені в кроці 8 і відповідають файлам у репозиторії.
- Якщо ранній приклад відрізняється від повного лістингу, використовуй повний актуальний лістинг.
- `views.py` і `urls.py` наповнюються **поступово** — по одному контролеру / маршруту за крок
- Фікстури розбиті по моделях: `categories.json`, `courses.json`, `modules.json`, `lessons.json`, `quizzes.json`
- Кроки створення проєкту та допоміжні команди описують процес розробки, а не лише поточні файли репозиторію

## План

**Частина 1: Каркас + дані**

1. Оточення, проєкт, базовий шаблон
2. Модель Category + Course
3. Модель Module + Lesson
4. Модель Quiz + Question + Answer
5. Модель UserAttempt + UserAnswer
6. Модель Comment
7. Admin — фінальний
8. Фікстури (5 файлів)

**Частина 2: Публічні сторінки (голий HTML)**

9. Список курсів + фільтри + пагінація
10. Сторінка курсу
11. Сторінка уроку + prev/next
12. Авторизація + реєстрація
13. Список тестів
14. Проходження тесту
15. Деталізація спроби
16. Мої результати
17. Коментарі
18. Markdown

**Частина 3: Tailwind CSS**

19. Підключення Tailwind + темна тема
20. Рестайл сторінок

---

# ЧАСТИНА 1: Каркас + дані

## Крок 1: Оточення, проєкт, базовий шаблон

### 1.1 Команди

```bash
mkdir learnhub && cd learnhub
python -m venv myenv
source myenv/bin/activate
pip install django
django-admin startproject config .
python manage.py startapp courses

mkdir -p templates
mkdir -p courses/templates/courses
mkdir -p courses/templates/registration
mkdir -p courses/fixtures
mkdir -p courses/templatetags
touch courses/templatetags/__init__.py
```

### 1.2 `config/settings.py` — ключові зміни

Додай `'courses'` у `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',
]
```

У `TEMPLATES` заміни `'DIRS': []` на:

```python
'DIRS': [BASE_DIR / 'templates'],
```

У **кінець** файлу:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'courses:course_list'
LOGOUT_REDIRECT_URL = 'courses:course_list'

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
```

**Пояснення:**

- **`LOGIN_URL = 'login'`** — куди редіректити неавторизованих при `@login_required`
- **`LOGIN_REDIRECT_URL` / `LOGOUT_REDIRECT_URL`** — куди йти після входу / виходу
- **`SECURE_REFERRER_POLICY`** — виправляє YouTube error 153 при вбудовуванні відео
- **`DIRS`** — де шукати базовий шаблон (поза додатками)

### 1.3 `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses import views as course_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', course_views.register, name='register'),
    path('', include('courses.urls')),
]
```

### 1.4 `courses/urls.py` — стартова заглушка

```python
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
]
```

### 1.5 `courses/views.py` — стартова заглушка

```python
from django.shortcuts import render


def course_list(request):
    return render(request, 'courses/course_list.html', {'page_obj': None})


def register(request):
    return render(request, 'registration/register.html', {'form': None})
```

### 1.6 `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}LearnHub{% endblock %}</title>
</head>
<body>
<p>
    <a href="/">Courses</a>
    {% if user.is_authenticated %}
        | Logged in as {{ user.username }}
        <form method="post" action="{% url 'logout' %}" style="display:inline;">
            {% csrf_token %}
            <button type="submit">Logout</button>
        </form>
    {% else %}
        | <a href="{% url 'login' %}">Login</a> or <a href="{% url 'register' %}">Register</a>
    {% endif %}
</p>
<hr>
{% block content_full %}
<main>
    {% block content %}{% endblock %}
</main>
{% endblock %}
</body>
</html>
```

### 1.7 Мінімальні шаблони

`courses/templates/courses/course_list.html`:

```html
{% extends 'base.html' %}

{% block title %}Courses{% endblock %}

{% block content %}
<h1>Courses</h1>
{% endblock %}
```

`courses/templates/registration/login.html`:

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<h1>Login</h1>
{% endblock %}
```

`courses/templates/registration/register.html`:

```html
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<h1>Register</h1>
{% endblock %}
```

### 1.8 Міграції та суперкористувач

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### ✅ Перевірка Кроку 1

- *http://127.0.0.1:8000/* — «Courses» + меню
- *http://127.0.0.1:8000/admin/* — адмінка відкривається

---

## Крок 2: Модель Category + Course

### 2.1 `courses/models.py`

```python
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
```

**Пояснення:**

- **`Category`** — категорія курсу. `verbose_name_plural = 'categories'`
- **`Course.category`** — `ForeignKey` з `on_delete=models.SET_NULL` — видалення категорії не видаляє курси
- **`slug`** — генерується автоматично в `save()` через `slugify`
- **`created_at`** — `auto_now_add=True`, проставляється один раз при створенні

### 2.2 Міграції

```bash
python manage.py makemigrations courses
python manage.py migrate
```

Очікуваний вивід:

```
Migrations for 'courses':
  courses/migrations/0001_initial.py
    - Create model Category
    - Create model Course
```

### 2.3 `courses/admin.py`

```python
from django.contrib import admin
from .models import Category, Course

admin.site.register(Category)
admin.site.register(Course)
```

### ✅ Перевірка Кроку 2

1. *http://127.0.0.1:8000/admin/courses/category/add/* — додай категорію «Programming»
2. *http://127.0.0.1:8000/admin/courses/course/add/* — додай курс «Test Course» із порожнім slug
3. Після збереження slug має стати `test-course`

---

## Крок 3: Модель Module + Lesson

### 3.1 Додай у кінець `courses/models.py`

```python
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
```

**Пояснення:**

- **`CASCADE`** — видалення курсу тягне модулі; видалення модуля тягне уроки
- **`related_name`** — `course.modules.all()`, `module.lessons.all()`
- **`order` + `Meta.ordering`** — ручне сортування

### 3.2 Міграції

```bash
python manage.py makemigrations courses
python manage.py migrate
```

Очікуваний вивід:

```
Migrations for 'courses':
  courses/migrations/0002_module_lesson.py
    - Create model Module
    - Create model Lesson
```

### 3.3 `courses/admin.py` — повний файл

```python
from django.contrib import admin
from .models import Category, Course, Module, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    list_display = ['title', 'slug', 'category', 'created_at']
    list_filter = ['category']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    list_display = ['title', 'course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'module', 'order']
```

**Пояснення:**

- **`TabularInline`** — вбудовані рядки таблиці на сторінці батька
- **`prepopulated_fields`** — slug заповнюється на льоту з title
- **Django admin не підтримує трирівневий inline** — Course містить Module, Module містить Lesson

### ✅ Перевірка Кроку 3

1. Відкрий «Test Course» в адмінці → унизу блок «Modules» → додай модуль «Module 1»
2. Збережи, відкрий модуль → додай урок «Lesson 1»
3. Перевір, що `order` впливає на порядок

---

## Крок 4: Модель Quiz + Question + Answer

### 4.1 Додай у кінець `courses/models.py`

```python
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    course = models.OneToOneField(
        Course, on_delete=models.CASCADE, related_name='quiz'
    )
    passing_score = models.PositiveIntegerField(default=70)

    def __str__(self):
        return self.title


class Question(models.Model):
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    QUESTION_TYPES = [
        (SINGLE, 'Single answer (radio)'),
        (MULTIPLE, 'Multiple answers (checkbox)'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=SINGLE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
```

**Пояснення:**

- **`Quiz.course`** — `OneToOneField` — один тест на один курс
- **`Question.question_type`** — `single` (radio) або `multiple` (checkbox), тип на рівні питання
- **`Answer.is_correct`** — для `single` рівно один True; для `multiple` — один або більше

### 4.2 Міграції

```bash
python manage.py makemigrations courses
python manage.py migrate
```

### 4.3 Доповни `courses/admin.py`

Заміни імпорт на:

```python
from .models import Category, Course, Module, Lesson, Quiz, Question, Answer
```

Додай у кінець:

```python
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'question_type', 'order']
    list_filter = ['question_type']
    inlines = [AnswerInline]
    search_fields = ['text']
    autocomplete_fields = ['quiz']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score']
    search_fields = ['title']
    autocomplete_fields = ['course']
```

**Пояснення:**

- **`autocomplete_fields`** — dropdown із пошуком (працює, лише якщо в цільовій моделі є `search_fields`)
- **`min_num = 2`** — щонайменше 2 варіанти відповіді

### ✅ Перевірка Кроку 4

```bash
python manage.py check
```

Має вивести:

```
System check identified no issues (0 silenced).
```

У адмінці створи Quiz для «Test Course» і додай питання.

---

## Крок 5: Модель UserAttempt + UserAnswer

### 5.1 Додай у кінець `courses/models.py`

```python
class UserAttempt(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.quiz} — {self.score}%"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.ManyToManyField(Answer)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.attempt} — {self.question.text[:30]}"
```

**Пояснення:**

- **`UserAttempt`** — підсумок спроби: `score`, `passed`, `created_at`
- **`UserAnswer.selected`** — `ManyToManyField` — для single 1 об'єкт, для multiple — кілька
- **`UserAnswer.is_correct`** — чи зараховано питання

### 5.2 Міграції

```bash
python manage.py makemigrations courses
python manage.py migrate
```

### 5.3 Доповни `courses/admin.py`

Заміни імпорт на:

```python
from .models import (
    Category, Course, Module, Lesson,
    Quiz, Question, Answer,
    UserAttempt, UserAnswer,
)
```

Додай у кінець:

```python
admin.site.register(UserAttempt)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['question__text']
    autocomplete_fields = ['question']
```

---

## Крок 6: Модель Comment

### 6.1 Додай у кінець `courses/models.py`

```python
class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"
```

**Пояснення:**

- **`parent`** — самопосилання для відповідей. `null=True` — кореневий коментар
- **`related_name='replies'`** — `comment.replies.all()`

### 6.2 Міграції

```bash
python manage.py makemigrations courses
python manage.py migrate
```

### 6.3 Доповни `courses/admin.py`

Додай у імпорт `Comment`, і в кінець:

```python
admin.site.register(Comment)
```

---

## Крок 7: Admin — фінальна версія

Повний `courses/admin.py`:

```python
from django.contrib import admin
from .models import (
    Category, Course, Module, Lesson,
    Quiz, Question, Answer,
    UserAttempt, UserAnswer, Comment,
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    min_num = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug']
    search_fields = ['title']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    list_display = ['title', 'slug', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['title']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    list_display = ['title', 'course', 'order']
    search_fields = ['title', 'course__title']
    autocomplete_fields = ['course']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'module', 'order']
    search_fields = ['title', 'module__title']
    autocomplete_fields = ['module']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'question_type', 'order']
    list_filter = ['question_type']
    inlines = [AnswerInline]
    search_fields = ['text']
    autocomplete_fields = ['quiz']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score']
    search_fields = ['title']
    autocomplete_fields = ['course']


admin.site.register(UserAttempt)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['question__text']
    autocomplete_fields = ['question']


admin.site.register(Comment)
```

### ✅ Перевірка Кроку 7

```bash
python manage.py check
```

Має вивести `System check identified no issues (0 silenced).`

---

## Крок 8: Фікстури — 5 файлів

### 8.1 `courses/fixtures/categories.json`

```json
[
  {
    "model": "courses.category",
    "pk": 1,
    "fields": {
      "title": "Programming",
      "slug": "programming"
    }
  },
  {
    "model": "courses.category",
    "pk": 2,
    "fields": {
      "title": "Web Development",
      "slug": "web-development"
    }
  },
  {
    "model": "courses.category",
    "pk": 3,
    "fields": {
      "title": "Databases",
      "slug": "databases"
    }
  },
  {
    "model": "courses.category",
    "pk": 4,
    "fields": {
      "title": "DevOps",
      "slug": "devops"
    }
  },
  {
    "model": "courses.category",
    "pk": 5,
    "fields": {
      "title": "Tools",
      "slug": "tools"
    }
  }
]
```

### 8.2 `courses/fixtures/courses.json`

```json
[
  {
    "model": "courses.course",
    "pk": 1,
    "fields": {
      "title": "Django Basics",
      "slug": "django-basics",
      "description": "Introduction to Django framework: models, views, templates, admin.",
      "category": 2,
      "created_at": "2026-01-01T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 2,
    "fields": {
      "title": "Python Advanced",
      "slug": "python-advanced",
      "description": "Advanced Python topics: decorators, generators, async, typing.",
      "category": 1,
      "created_at": "2026-01-02T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 3,
    "fields": {
      "title": "Web Development Fundamentals",
      "slug": "web-development-fundamentals",
      "description": "HTML, HTTP, client-server basics, and how the web works.",
      "category": 2,
      "created_at": "2026-01-03T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 4,
    "fields": {
      "title": "Python for Beginners",
      "slug": "python-for-beginners",
      "description": "Start from zero: variables, loops, functions, and your first scripts.",
      "category": 1,
      "created_at": "2026-01-04T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 5,
    "fields": {
      "title": "Databases and SQL",
      "slug": "databases-and-sql",
      "description": "Relational databases, SQL queries, indexes, and normalization.",
      "category": 3,
      "created_at": "2026-01-05T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 6,
    "fields": {
      "title": "Git and Version Control",
      "slug": "git-and-version-control",
      "description": "Commits, branches, merges, remotes, and collaboration workflows.",
      "category": 5,
      "created_at": "2026-01-06T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 7,
    "fields": {
      "title": "REST API Design",
      "slug": "rest-api-design",
      "description": "Resources, HTTP methods, status codes, versioning, and best practices.",
      "category": 2,
      "created_at": "2026-01-07T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 8,
    "fields": {
      "title": "Testing in Python",
      "slug": "testing-in-python",
      "description": "Unit tests, pytest, fixtures, mocks, and test-driven development.",
      "category": 1,
      "created_at": "2026-01-08T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 9,
    "fields": {
      "title": "Linux Command Line",
      "slug": "linux-command-line",
      "description": "Files, permissions, processes, pipes, and shell scripting basics.",
      "category": 4,
      "created_at": "2026-01-09T10:00:00Z"
    }
  },
  {
    "model": "courses.course",
    "pk": 10,
    "fields": {
      "title": "Deployment and DevOps",
      "slug": "deployment-and-devops",
      "description": "Servers, Docker, CI/CD, environment variables, and going live.",
      "category": 4,
      "created_at": "2026-01-10T10:00:00Z"
    }
  }
]
```

### 8.3 `courses/fixtures/modules.json`

```json
[
  {
    "model": "courses.module",
    "pk": 1,
    "fields": { "course": 1, "title": "Getting Started", "slug": "getting-started", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 2,
    "fields": { "course": 1, "title": "Models and Database", "slug": "models-and-database", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 3,
    "fields": { "course": 1, "title": "Views and Templates", "slug": "views-and-templates", "order": 3 }
  },
  {
    "model": "courses.module",
    "pk": 4,
    "fields": { "course": 2, "title": "Decorators and Closures", "slug": "decorators-and-closures", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 5,
    "fields": { "course": 2, "title": "Generators and Iterators", "slug": "generators-and-iterators", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 6,
    "fields": { "course": 4, "title": "First Steps", "slug": "first-steps", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 7,
    "fields": { "course": 4, "title": "Control Flow", "slug": "control-flow", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 8,
    "fields": { "course": 3, "title": "How the Web Works", "slug": "how-the-web-works", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 9,
    "fields": { "course": 3, "title": "HTML Basics", "slug": "html-basics", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 10,
    "fields": { "course": 5, "title": "Relational Model", "slug": "relational-model", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 11,
    "fields": { "course": 5, "title": "SQL Queries", "slug": "sql-queries", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 12,
    "fields": { "course": 6, "title": "Basic Commands", "slug": "basic-commands", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 13,
    "fields": { "course": 6, "title": "Branching and Merging", "slug": "branching-and-merging", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 14,
    "fields": { "course": 7, "title": "HTTP and Resources", "slug": "http-and-resources", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 15,
    "fields": { "course": 7, "title": "Status Codes and Errors", "slug": "status-codes-and-errors", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 16,
    "fields": { "course": 8, "title": "Unit Testing", "slug": "unit-testing", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 17,
    "fields": { "course": 8, "title": "Mocks and Fixtures", "slug": "mocks-and-fixtures", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 18,
    "fields": { "course": 9, "title": "Files and Directories", "slug": "files-and-directories", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 19,
    "fields": { "course": 9, "title": "Pipes and Redirection", "slug": "pipes-and-redirection", "order": 2 }
  },
  {
    "model": "courses.module",
    "pk": 20,
    "fields": { "course": 10, "title": "Servers and Environments", "slug": "servers-and-environments", "order": 1 }
  },
  {
    "model": "courses.module",
    "pk": 21,
    "fields": { "course": 10, "title": "CI and CD", "slug": "ci-and-cd", "order": 2 }
  }
]
```

### 8.4 `courses/fixtures/lessons.json`

Повний файл `courses/fixtures/lessons.json` з актуальними даними проєкту:

```json
[
  {
    "model": "courses.lesson",
    "pk": 1,
    "fields": {
      "module": 1,
      "title": "What is Django",
      "slug": "what-is-django",
      "content": "# What is Django\n\nDjango is a **high-level** Python web framework that encourages rapid development.\n\n## Key features\n\n- ORM for database access\n- Template engine\n- Automatic admin panel\n- URL routing\n\nRead more at the [official documentation](https://docs.djangoproject.com/).",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 2,
    "fields": {
      "module": 1,
      "title": "Installing Django",
      "slug": "installing-django",
      "content": "# Installing Django\n\nInstall Django with pip:\n\n```bash\npip install django\n```\n\nThen create a new project:\n\n```bash\ndjango-admin startproject config .\n```\n\nRun the development server:\n\n```bash\npython manage.py runserver\n```",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 3,
    "fields": {
      "module": 2,
      "title": "Your First Model",
      "slug": "your-first-model",
      "content": "# Your First Model\n\nModels are Python classes that map to database tables.\n\nEach attribute of the class is a field.\n\n```python\nfrom django.db import models\n\n\nclass Course(models.Model):\n    title = models.CharField(max_length=200)\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 4,
    "fields": {
      "module": 2,
      "title": "Migrations Explained",
      "slug": "migrations-explained",
      "content": "# Migrations Explained\n\nMigrations are Django's way of propagating changes to your models into the database schema.\n\n## Commands\n\n- `makemigrations` — create migration files\n- `migrate` — apply migrations to the database\n- `showmigrations` — list all migrations and their status",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 5,
    "fields": {
      "module": 3,
      "title": "Function Views",
      "slug": "function-views",
      "content": "# Function Views\n\nA view is a Python function that takes a web request and returns a web response.\n\n```python\nfrom django.shortcuts import render\n\n\ndef index(request):\n    return render(request, 'index.html')\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 6,
    "fields": {
      "module": 3,
      "title": "Template Basics",
      "slug": "template-basics",
      "content": "# Template Basics\n\nTemplates are HTML files with special tags that Django renders with context data.\n\n## Common tags\n\n- `{% raw %}{{ variable }}{% endraw %}` — output a value\n- `{% raw %}{% if condition %}{% endraw %}` — conditional\n- `{% raw %}{% for item in list %}{% endraw %}` — loop",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 7,
    "fields": {
      "module": 4,
      "title": "Understanding Decorators",
      "slug": "understanding-decorators",
      "content": "# Understanding Decorators\n\nA decorator is a function that takes another function and extends its behavior without modifying it.\n\n```python\ndef my_decorator(func):\n    def wrapper():\n        print('Before')\n        func()\n        print('After')\n    return wrapper\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 8,
    "fields": {
      "module": 5,
      "title": "Generator Functions",
      "slug": "generator-functions",
      "content": "# Generator Functions\n\nGenerators produce values lazily using the `yield` keyword instead of returning a list.\n\n```python\ndef count_up(n):\n    for i in range(n):\n        yield i\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 9,
    "fields": {
      "module": 6,
      "title": "Variables and Types",
      "slug": "variables-and-types",
      "content": "# Variables and Types\n\nPython is **dynamically typed**. Variables are names bound to objects.\n\n## Common types\n\n- `int` — integers\n- `float` — floating point numbers\n- `str` — strings\n- `list` — ordered collections\n- `dict` — key-value mappings",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 10,
    "fields": {
      "module": 7,
      "title": "If Statements",
      "slug": "if-statements",
      "content": "# If Statements\n\nConditional execution uses `if`, `elif`, `else`. Indentation defines blocks in Python.\n\n```python\nx = 10\nif x > 5:\n    print('big')\nelse:\n    print('small')\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 11,
    "fields": {
      "module": 8,
      "title": "Client and Server",
      "slug": "client-and-server",
      "content": "# Client and Server\n\nThe client sends a request, the server responds.\n\nHTTP is the protocol between them.\n\n## Request flow\n\n- Client (browser) sends request\n- Server processes it\n- Server sends back response\n- Client renders the result",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 12,
    "fields": {
      "module": 8,
      "title": "HTTP Methods",
      "slug": "http-methods",
      "content": "# HTTP Methods\n\nEach method has a semantic meaning:\n\n- `GET` — retrieve data\n- `POST` — create data\n- `PUT` — replace data\n- `PATCH` — update part of data\n- `DELETE` — remove data",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 13,
    "fields": {
      "module": 9,
      "title": "Tags and Elements",
      "slug": "tags-and-elements",
      "content": "# Tags and Elements\n\nHTML documents are built from nested elements, each defined by tags.\n\n```html\n<div class=\"container\">\n    <h1>Hello</h1>\n    <p>World</p>\n</div>\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 14,
    "fields": {
      "module": 10,
      "title": "Tables and Rows",
      "slug": "tables-and-rows",
      "content": "# Tables and Rows\n\nRelational databases store data in **tables** with **rows** and **columns**.\n\nEach row is a record, each column is a field.",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 15,
    "fields": {
      "module": 10,
      "title": "Primary and Foreign Keys",
      "slug": "primary-and-foreign-keys",
      "content": "# Primary and Foreign Keys\n\n- **Primary key** — uniquely identifies a row in a table\n- **Foreign key** — links a row to a row in another table\n\nThese keys enforce referential integrity.",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 16,
    "fields": {
      "module": 11,
      "title": "SELECT Statements",
      "slug": "select-statements",
      "content": "# SELECT Statements\n\n`SELECT` retrieves data from one or more tables. `WHERE` filters rows.\n\n```sql\nSELECT title, description\nFROM courses\nWHERE category_id = 1;\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 17,
    "fields": {
      "module": 11,
      "title": "JOIN Operations",
      "slug": "join-operations",
      "content": "# JOIN Operations\n\n`JOIN` combines rows from two tables based on a related column.\n\n```sql\nSELECT c.title, m.title\nFROM courses c\nJOIN modules m ON m.course_id = c.id;\n```",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 18,
    "fields": {
      "module": 12,
      "title": "Git Init and Commit",
      "slug": "git-init-and-commit",
      "content": "# Git Init and Commit\n\n`git init` creates a repository. `git commit` saves a snapshot of your changes.\n\n```bash\ngit init\ngit add .\ngit commit -m \"Initial commit\"\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 19,
    "fields": {
      "module": 12,
      "title": "Viewing History",
      "slug": "viewing-history",
      "content": "# Viewing History\n\n- `git log` — show commit history\n- `git diff` — show changes between commits\n- `git show` — show details of a commit",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 20,
    "fields": {
      "module": 13,
      "title": "Creating Branches",
      "slug": "creating-branches",
      "content": "# Creating Branches\n\n- `git branch name` — create a branch\n- `git checkout name` — switch to it\n- `git merge name` — merge into current branch\n\n```bash\ngit branch feature\ngit checkout feature\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 21,
    "fields": {
      "module": 14,
      "title": "Resources and URIs",
      "slug": "resources-and-uris",
      "content": "# Resources and URIs\n\nREST models everything as a **resource**, identified by a URI.\n\nExamples:\n\n- `/courses` — collection of courses\n- `/courses/1` — single course\n- `/courses/1/modules` — modules of a course",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 22,
    "fields": {
      "module": 14,
      "title": "Stateless Requests",
      "slug": "stateless-requests",
      "content": "# Stateless Requests\n\nEach request contains all information needed to process it — **no session state** on the server.\n\nAuthentication is sent with every request (tokens, headers).",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 23,
    "fields": {
      "module": 15,
      "title": "2xx and 4xx Codes",
      "slug": "2xx-and-4xx-codes",
      "content": "# 2xx and 4xx Codes\n\n- **2xx** — success\n- **4xx** — client error\n\nCommon codes:\n\n- `200 OK`\n- `201 Created`\n- `404 Not Found`\n- `400 Bad Request`",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 24,
    "fields": {
      "module": 16,
      "title": "Writing Your First Test",
      "slug": "writing-your-first-test",
      "content": "# Writing Your First Test\n\nA test is a function that asserts behavior.\n\n```python\ndef test_addition():\n    assert 1 + 1 == 2\n```\n\nRun tests with `pytest` or `python -m unittest`.",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 25,
    "fields": {
      "module": 17,
      "title": "Mocks and Patches",
      "slug": "mocks-and-patches",
      "content": "# Mocks and Patches\n\nMocks replace real objects in tests to isolate behavior and avoid side effects.\n\n```python\nfrom unittest.mock import Mock\n\nmock = Mock()\nmock.return_value = 42\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 26,
    "fields": {
      "module": 18,
      "title": "ls, cd, pwd",
      "slug": "ls-cd-pwd",
      "content": "# ls, cd, pwd\n\nBasic navigation commands:\n\n- `ls` — list files\n- `cd` — change directory\n- `pwd` — print current directory\n\n```bash\npwd\nls -la\ncd /var/log\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 27,
    "fields": {
      "module": 18,
      "title": "File Permissions",
      "slug": "file-permissions",
      "content": "# File Permissions\n\n- `chmod` — change file mode\n- `chown` — change owner\n\nPermissions are `rwx` for user, group, and others.\n\n```bash\nchmod 755 script.sh\n```",
      "order": 2
    }
  },
  {
    "model": "courses.lesson",
    "pk": 28,
    "fields": {
      "module": 19,
      "title": "The Pipe Operator",
      "slug": "the-pipe-operator",
      "content": "# The Pipe Operator\n\nThe `|` operator sends stdout of one command to stdin of another.\n\n```bash\nls -la | grep \".py\"\ncat file.txt | wc -l\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 29,
    "fields": {
      "module": 20,
      "title": "Environment Variables",
      "slug": "environment-variables",
      "content": "# Environment Variables\n\nEnvironment variables configure apps without changing code.\n\n```python\nimport os\n\nsecret = os.environ.get('SECRET_KEY')\n```\n\nSet in shell:\n\n```bash\nexport SECRET_KEY=\"abc123\"\n```",
      "order": 1
    }
  },
  {
    "model": "courses.lesson",
    "pk": 30,
    "fields": {
      "module": 21,
      "title": "Continuous Integration",
      "slug": "continuous-integration",
      "content": "# Continuous Integration\n\nCI runs tests automatically on every push. Catches regressions early.\n\nCommon CI providers:\n\n- GitHub Actions\n- GitLab CI\n- CircleCI",
      "order": 1
    }
  }
]
```

### 8.5 `courses/fixtures/quizzes.json`

Повний файл `courses/fixtures/quizzes.json` з актуальними даними проєкту:

```json
[
  {
    "model": "courses.quiz",
    "pk": 1,
    "fields": { "title": "Django Basics Course Quiz", "course": 1, "passing_score": 70 }
  },
  {
    "model": "courses.quiz",
    "pk": 2,
    "fields": { "title": "Python Advanced Course Quiz", "course": 2, "passing_score": 70 }
  },
  {
    "model": "courses.quiz",
    "pk": 3,
    "fields": { "title": "Python for Beginners Course Quiz", "course": 4, "passing_score": 60 }
  },
  {
    "model": "courses.quiz",
    "pk": 4,
    "fields": { "title": "Databases and SQL Course Quiz", "course": 5, "passing_score": 70 }
  },
  {
    "model": "courses.quiz",
    "pk": 5,
    "fields": { "title": "Git and Version Control Course Quiz", "course": 6, "passing_score": 60 }
  },

  {
    "model": "courses.question",
    "pk": 1,
    "fields": { "quiz": 1, "text": "What is Django?", "question_type": "single", "order": 1 }
  },
  {
    "model": "courses.question",
    "pk": 2,
    "fields": { "quiz": 1, "text": "Which of these are Django components?", "question_type": "multiple", "order": 2 }
  },
  {
    "model": "courses.question",
    "pk": 3,
    "fields": { "quiz": 1, "text": "Which command creates a new Django project?", "question_type": "single", "order": 3 }
  },

  {
    "model": "courses.question",
    "pk": 4,
    "fields": { "quiz": 2, "text": "What does a Python decorator do?", "question_type": "single", "order": 1 }
  },
  {
    "model": "courses.question",
    "pk": 5,
    "fields": { "quiz": 2, "text": "Which of these are Python generator features?", "question_type": "multiple", "order": 2 }
  },

  {
    "model": "courses.question",
    "pk": 6,
    "fields": { "quiz": 3, "text": "Which keyword defines a function in Python?", "question_type": "single", "order": 1 }
  },
  {
    "model": "courses.question",
    "pk": 7,
    "fields": { "quiz": 3, "text": "Which of these are valid Python data types?", "question_type": "multiple", "order": 2 }
  },

  {
    "model": "courses.question",
    "pk": 8,
    "fields": { "quiz": 4, "text": "What does SQL stand for?", "question_type": "single", "order": 1 }
  },
  {
    "model": "courses.question",
    "pk": 9,
    "fields": { "quiz": 4, "text": "Which of these are SQL JOIN types?", "question_type": "multiple", "order": 2 }
  },

  {
    "model": "courses.question",
    "pk": 10,
    "fields": { "quiz": 5, "text": "Which command initializes a new Git repository?", "question_type": "single", "order": 1 }
  },
  {
    "model": "courses.question",
    "pk": 11,
    "fields": { "quiz": 5, "text": "Which of these are Git commands?", "question_type": "multiple", "order": 2 }
  },
  {
    "model": "courses.question",
    "pk": 12,
    "fields": { "quiz": 5, "text": "What is a Git branch?", "question_type": "single", "order": 3 }
  },

  {
    "model": "courses.answer",
    "pk": 1,
    "fields": { "question": 1, "text": "A Python web framework", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 2,
    "fields": { "question": 1, "text": "A JavaScript library", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 3,
    "fields": { "question": 1, "text": "A database engine", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 4,
    "fields": { "question": 2, "text": "ORM", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 5,
    "fields": { "question": 2, "text": "Template engine", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 6,
    "fields": { "question": 2, "text": "React", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 7,
    "fields": { "question": 2, "text": "Admin panel", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 8,
    "fields": { "question": 3, "text": "django-admin startproject", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 9,
    "fields": { "question": 3, "text": "django-admin createproject", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 10,
    "fields": { "question": 3, "text": "python manage.py startapp", "is_correct": false }
  },

  {
    "model": "courses.answer",
    "pk": 11,
    "fields": { "question": 4, "text": "Extends the behavior of a function", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 12,
    "fields": { "question": 4, "text": "Deletes a function", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 13,
    "fields": { "question": 4, "text": "Renames a function", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 14,
    "fields": { "question": 5, "text": "Uses the yield keyword", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 15,
    "fields": { "question": 5, "text": "Produces values lazily", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 16,
    "fields": { "question": 5, "text": "Always returns a list", "is_correct": false }
  },

  {
    "model": "courses.answer",
    "pk": 17,
    "fields": { "question": 6, "text": "def", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 18,
    "fields": { "question": 6, "text": "func", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 19,
    "fields": { "question": 6, "text": "function", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 20,
    "fields": { "question": 7, "text": "int", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 21,
    "fields": { "question": 7, "text": "str", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 22,
    "fields": { "question": 7, "text": "list", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 23,
    "fields": { "question": 7, "text": "number", "is_correct": false }
  },

  {
    "model": "courses.answer",
    "pk": 24,
    "fields": { "question": 8, "text": "Structured Query Language", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 25,
    "fields": { "question": 8, "text": "Simple Query Language", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 26,
    "fields": { "question": 8, "text": "Standard Question Language", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 27,
    "fields": { "question": 9, "text": "INNER JOIN", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 28,
    "fields": { "question": 9, "text": "LEFT JOIN", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 29,
    "fields": { "question": 9, "text": "RIGHT JOIN", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 30,
    "fields": { "question": 9, "text": "MIDDLE JOIN", "is_correct": false }
  },

  {
    "model": "courses.answer",
    "pk": 31,
    "fields": { "question": 10, "text": "git init", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 32,
    "fields": { "question": 10, "text": "git start", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 33,
    "fields": { "question": 10, "text": "git create", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 34,
    "fields": { "question": 11, "text": "git commit", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 35,
    "fields": { "question": 11, "text": "git push", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 36,
    "fields": { "question": 11, "text": "git merge", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 37,
    "fields": { "question": 11, "text": "git save", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 38,
    "fields": { "question": 12, "text": "A parallel line of development", "is_correct": true }
  },
  {
    "model": "courses.answer",
    "pk": 39,
    "fields": { "question": 12, "text": "A copy of the whole project", "is_correct": false }
  },
  {
    "model": "courses.answer",
    "pk": 40,
    "fields": { "question": 12, "text": "A type of commit", "is_correct": false }
  }
]
```

### 8.6 Перевірка JSON

```bash
python -m json.tool courses/fixtures/categories.json > /dev/null && echo "categories OK"
python -m json.tool courses/fixtures/courses.json > /dev/null && echo "courses OK"
python -m json.tool courses/fixtures/modules.json > /dev/null && echo "modules OK"
python -m json.tool courses/fixtures/lessons.json > /dev/null && echo "lessons OK"
python -m json.tool courses/fixtures/quizzes.json > /dev/null && echo "quizzes OK"
```

Має вивести 5 рядків `OK`.

### 8.7 Завантаження

```bash
python manage.py loaddata categories.json courses.json modules.json lessons.json quizzes.json
```

**Порядок критичний**: `categories` → `courses` → `modules` → `lessons` → `quizzes`. Django завантажує файли зліва направо.

Очікуваний вивід:

```
Installed 5 object(s) from 1 fixture(s)
Installed 10 object(s) from 1 fixture(s)
Installed 21 object(s) from 1 fixture(s)
Installed 30 object(s) from 1 fixture(s)
Installed 57 object(s) from 1 fixture(s)
```

### 8.8 `reload_fixtures.sh`

```bash
#!/bin/bash
set -e

echo "Clearing database..."
python manage.py shell -c "
from courses.models import (
    Comment,
    UserAnswer, UserAttempt, Answer, Question, Quiz,
    Lesson, Module, Course, Category,
)
Comment.objects.all().delete()
UserAnswer.objects.all().delete()
UserAttempt.objects.all().delete()
Answer.objects.all().delete()
Question.objects.all().delete()
Quiz.objects.all().delete()
Lesson.objects.all().delete()
Module.objects.all().delete()
Course.objects.all().delete()
Category.objects.all().delete()
print('  cleared')
"

echo "Validating JSON..."
python -m json.tool courses/fixtures/categories.json > /dev/null && echo "  categories OK"
python -m json.tool courses/fixtures/courses.json > /dev/null && echo "  courses OK"
python -m json.tool courses/fixtures/modules.json > /dev/null && echo "  modules OK"
python -m json.tool courses/fixtures/lessons.json > /dev/null && echo "  lessons OK"
python -m json.tool courses/fixtures/quizzes.json > /dev/null && echo "  quizzes OK"

echo "Loading fixtures..."
python manage.py loaddata categories.json courses.json modules.json lessons.json quizzes.json

echo "Done."
```

```bash
chmod +x reload_fixtures.sh
./reload_fixtures.sh
```

### ✅ Перевірка Кроку 8

```bash
python manage.py shell -c "
from courses.models import Category, Course, Module, Lesson, Quiz, Question, Answer
print('Categories:', Category.objects.count())
print('Courses:', Course.objects.count())
print('Modules:', Module.objects.count())
print('Lessons:', Lesson.objects.count())
print('Quizzes:', Quiz.objects.count())
print('Questions:', Question.objects.count())
print('Answers:', Answer.objects.count())
"
```

Має вивести:

```
Categories: 5
Courses: 10
Modules: 21
Lessons: 30
Quizzes: 5
Questions: 12
Answers: 40
```

---

# ЧАСТИНА 2: Публічні сторінки (голий HTML)

## Крок 9: Список курсів + фільтри + пагінація

### 9.1 `courses/views.py` — заміни повністю

```python
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Category, Course


def course_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.annotate(course_count=Count('courses'))

    courses_qs = Course.objects.annotate(lesson_count=Count('modules__lessons'))

    if category_slug:
        courses_qs = courses_qs.filter(category__slug=category_slug)

    total_count = Course.objects.count()

    paginator = Paginator(courses_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'total_count': total_count,
    })


def register(request):
    return render(request, 'registration/register.html', {'form': None})
```

**Пояснення:**

- **`annotate(course_count=Count('courses'))`** — до кожної категорії додає кількість курсів
- **`request.GET.get('category')`** — читає `?category=programming`
- **`Paginator(courses_qs, 6)`** — 6 курсів на сторінку
- **`annotate(lesson_count=Count('modules__lessons'))`** — рахує уроки для картки курсу
- **`paginator.get_page(page_number)`** — безпечна обробка `?page=999`

### 9.2 `courses/templates/courses/course_list.html`

> Це спрощений навчальний шаблон без стилів: він показує дані з контексту `course_list`. Tailwind-оформлення додається у кроці 20.1.

```html
{% extends 'base.html' %}

{% block title %}Courses{% endblock %}

{% block content %}
<h1>Courses</h1>

<p>
    <a href="{% url 'courses:course_list' %}">All ({{ total_count }})</a>
    {% for category in categories %}
        | <a href="{% url 'courses:course_list' %}?category={{ category.slug }}">
            {{ category.title }} ({{ category.course_count }})
        </a>
    {% endfor %}
</p>

<ul>
{% for course in page_obj %}
    <li>
        <a href="{% url 'courses:course_detail' course.slug %}">{{ course.title }}</a>
        {% if course.category %}— {{ course.category.title }}{% endif %}
        ({{ course.lesson_count }} lessons)
        {% if course.quiz %}— Quiz available{% endif %}
    </li>
{% empty %}
    <li>No courses in this category.</li>
{% endfor %}
</ul>

{% if page_obj.has_other_pages %}
    <p>
        {% if page_obj.has_previous %}
            <a href="?{% if selected_category %}category={{ selected_category }}&{% endif %}page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}
        {% for num in page_obj.paginator.page_range %}
            {% if num == page_obj.number %}
                <strong>{{ num }}</strong>
            {% else %}
                <a href="?{% if selected_category %}category={{ selected_category }}&{% endif %}page={{ num }}">{{ num }}</a>
            {% endif %}
        {% endfor %}
        {% if page_obj.has_next %}
            <a href="?{% if selected_category %}category={{ selected_category }}&{% endif %}page={{ page_obj.next_page_number }}">Next</a>
        {% endif %}
    </p>
{% endif %}
{% endblock %}
```

### ✅ Перевірка Кроку 9

- *http://127.0.0.1:8000/* — до 6 курсів на сторінці + фільтри + пагінація
- *http://127.0.0.1:8000/?category=programming* — 3 курси
- *http://127.0.0.1:8000/?page=2* — друга сторінка
- *http://127.0.0.1:8000/?category=programming&page=1* — фільтр + пагінація

---

## Крок 10: Сторінка курсу

### 10.1 `courses/urls.py`

```python
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
]
```

### 10.2 `courses/views.py` — додай імпорти й контролер

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Category, Course, Lesson
```

Додай у кінець:

```python
@login_required
def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    first_lesson = Lesson.objects.filter(
        module__course=course
    ).order_by('module__order', 'order').first()

    if first_lesson:
        return redirect(
            'courses:lesson_detail',
            course_slug=course.slug,
            lesson_slug=first_lesson.slug
        )
    return render(request, 'courses/course_detail.html', {'course': course})
```

**Пояснення:**

- **`order_by('module__order', 'order')`** — спочатку за `order` модуля, потім за `order` уроку
- **`.first()`** — бере перший урок курсу
- **`redirect`** — якщо є уроки → редірект; якщо ні → рендер сторінки порожнього курсу

### 10.3 `courses/templates/courses/course_detail.html`

```html
{% extends 'base.html' %}

{% block title %}{{ course.title }}{% endblock %}

{% block content %}
<h1>{{ course.title }}</h1>
{% if course.category %}<p>{{ course.category.title }}</p>{% endif %}
<p>{{ course.description }}</p>

{% if course.modules.all %}
    <h2>Modules</h2>
    {% for module in course.modules.all %}
        <h3>{{ module.title }}</h3>
        <ul>
        {% for lesson in module.lessons.all %}
            <li><a href="#">{{ lesson.title }}</a></li>
        {% endfor %}
        </ul>
    {% endfor %}
{% else %}
    <p>No lessons yet.</p>
    <p><a href="{% url 'courses:course_list' %}">Back to all courses</a></p>
{% endif %}
{% endblock %}
```

### 10.4 Онови `course_list.html` — посилання на курс

Заміни `<a href="#">{{ course.title }}</a>` на:

```html
<a href="{% url 'courses:course_detail' course.slug %}">{{ course.title }}</a>
```

### ✅ Перевірка Кроку 10

- Клік на «Django Basics» → редірект на майбутню сторінку уроку (поки 404)
- Створи порожній курс через адмінку → клік → побачиш «No lessons yet»

---

## Крок 11: Сторінка уроку + prev/next

### 11.1 `courses/urls.py`

```python
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
```

### 11.2 `courses/views.py` — додай

```python
@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, module__course=course)

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
```

**Пояснення:**

- **`module__course=course`** — Django подвійне підкреслення проходить через зв'язки. Гарантує, що урок належить курсу
- **`all_lessons`** — плаский список усіх уроків курсу
- **Prev/Next** — сусіди в цьому списку

### 11.3 `courses/templates/courses/lesson_detail.html`

```html
{% extends 'base.html' %}

{% block title %}{{ lesson.title }}{% endblock %}

{% block content %}
<h1>{{ lesson.title }}</h1>
<div>{{ lesson.content }}</div>

<hr>

<p>
    {% if prev_lesson %}
        <a href="{% url 'courses:lesson_detail' course.slug prev_lesson.slug %}">← {{ prev_lesson.title }}</a>
    {% else %}
        ← No previous lesson
    {% endif %}
    | <a href="{% url 'courses:course_detail' course.slug %}">Back to course</a> |
    {% if next_lesson %}
        <a href="{% url 'courses:lesson_detail' course.slug next_lesson.slug %}">{{ next_lesson.title }} →</a>
    {% else %}
        No next lesson →
    {% endif %}
</p>

<hr>

<h2>Course contents</h2>
<ul>
{% for module in course.modules.all %}
    <li>
        <strong>{{ module.title }}</strong>
        <ul>
        {% for l in module.lessons.all %}
            <li>
                {% if l.id == lesson.id %}
                    <strong>{{ l.title }} (current)</strong>
                {% else %}
                    <a href="{% url 'courses:lesson_detail' course.slug l.slug %}">{{ l.title }}</a>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    </li>
{% endfor %}
</ul>
{% endblock %}
```

### 11.4 Онови `course_detail.html` — посилання на урок

Заміни `<li><a href="#">{{ lesson.title }}</a></li>` на:

```html
<li><a href="{% url 'courses:lesson_detail' course.slug lesson.slug %}">{{ lesson.title }}</a></li>
```

### ✅ Перевірка Кроку 11

- *http://127.0.0.1:8000/django-basics/what-is-django/* — сторінка уроку
- Клік «Installing Django» → далі
- Клік «← What is Django» → назад
- У бічній панелі поточний урок жирним

---

## Крок 12: Авторизація + реєстрація

### 12.1 `courses/forms.py`

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First name')
    last_name = forms.CharField(max_length=30, required=True, label='Last name')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
```

### 12.2 `courses/views.py` — заміни `register`

Додай імпорти:

```python
from django.contrib.auth import login
from .forms import CustomUserCreationForm
```

Заміни `register`:

```python
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
```

### 12.3 `courses/templates/registration/login.html`

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<h1>Login</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
<p><a href="{% url 'register' %}">Register</a></p>
{% endblock %}
```

### 12.4 `courses/templates/registration/register.html`

```html
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<h1>Register</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
<p><a href="{% url 'login' %}">Already have an account? Login</a></p>
{% endblock %}
```

### ✅ Перевірка Кроку 12

- *http://127.0.0.1:8000/accounts/register/* — форма з 6 полів
- Зареєструйся → автологін → редірект на список курсів
- У шапці — «Logged in as username»
- «Logout» працює

---

## Крок 13: Список тестів

### 13.1 `courses/urls.py`

```python
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
```

### 13.2 `courses/views.py` — додай

Додай імпорт:

```python
from .models import Category, Course, Lesson, Quiz
```

Додай контролер:

```python
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'courses/quiz_list.html', {'quizzes': quizzes})
```

### 13.3 `courses/templates/courses/quiz_list.html`

```html
{% extends 'base.html' %}

{% block title %}All Quizzes{% endblock %}

{% block content %}
<h1>All Quizzes</h1>

{% if quizzes %}
    <ul>
    {% for quiz in quizzes %}
        <li>
            <strong>{{ quiz.title }}</strong>
            — {{ quiz.course.title }}
            — <a href="#">Take quiz</a>
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>No quizzes yet.</p>
{% endif %}
{% endblock %}
```

### 13.4 Онови `templates/base.html` — додай «Quizzes»

```html
<p>
    <a href="{% url 'courses:course_list' %}">Courses</a> |
    <a href="{% url 'courses:quiz_list' %}">Quizzes</a> |
    {% if user.is_authenticated %}
        ...
    {% endif %}
</p>
```

### ✅ Перевірка Кроку 13

*http://127.0.0.1:8000/quizzes/* — список тестів із назвами курсів.

---

## Крок 14: Проходження тесту

### 14.1 `courses/urls.py`

```python
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('<slug:course_slug>/quiz/', views.take_course_quiz, name='take_course_quiz'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
```

### 14.2 `courses/views.py` — додай

Додай імпорти:

```python
from django.urls import reverse
from .models import Category, Course, Lesson, Quiz, UserAttempt, UserAnswer
```

Додай функції:

```python
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
```

**Пояснення `process_quiz_submission`:**

- **`request.POST.getlist(f'question_{question.id}')`** — усі значення полів з однаковим `name`
- **`correct_ids`** — `set` ID правильних відповідей
- **`submitted_ids == correct_ids`** — для `single` — рівно один; для `multiple` — точна рівність множин
- **`UserAnswer.selected.set(...)`** — `ManyToManyField` потребує окремого `.set()`
- **`redirect` після POST** — PRG-патерн

### 14.3 `courses/templates/courses/take_quiz.html`

```html
{% extends 'base.html' %}

{% block title %}{{ quiz.title }}{% endblock %}

{% block content %}
<h1>{{ quiz.title }}</h1>
<form method="post" action="{{ submit_url }}">
{% csrf_token %}
{% for question in quiz.questions.all %}
    <fieldset>
        <legend>{{ forloop.counter }}. {{ question.text }}</legend>
        {% if question.question_type == 'single' %}
            {% for answer in question.answers.all %}
                <label>
                    <input type="radio" name="question_{{ question.id }}" value="{{ answer.id }}">
                    {{ answer.text }}
                </label><br>
            {% endfor %}
        {% else %}
            {% for answer in question.answers.all %}
                <label>
                    <input type="checkbox" name="question_{{ question.id }}" value="{{ answer.id }}">
                    {{ answer.text }}
                </label><br>
            {% endfor %}
        {% endif %}
    </fieldset>
{% endfor %}
<button type="submit">Submit</button>
</form>
{% endblock %}
```

### 14.4 Онови `quiz_list.html` — посилання «Take quiz»

Заміни `<a href="#">Take quiz</a>` на:

```html
<a href="{% url 'courses:take_course_quiz' quiz.course.slug %}">Take quiz</a>
```

### 14.5 Онови `lesson_detail.html` — кнопка quiz

Додай перед `{% endblock %}`:

```html
{% if not next_lesson and course.quiz %}
    <hr>
    <p><a href="{% url 'courses:take_course_quiz' course.slug %}">Start course quiz</a></p>
{% endif %}
```

### ✅ Перевірка Кроку 14

1. Увійди та відкрий `/quizzes/` або сторінку курсу з тестом.
2. Перейди за посиланням тесту → відкриється форма тесту курсу.
3. Дай відповіді → Submit → редірект (поки 404 на `attempt_detail`)
4. У shell:

```bash
python manage.py shell -c "
from courses.models import UserAttempt
for a in UserAttempt.objects.all():
    print(a.user, a.quiz.title, a.score, a.passed)
"
```

---

## Крок 15: Деталізація спроби

### 15.1 `courses/urls.py`

```python
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('my-results/', views.my_results, name='my_results'),
    path('my-results/<int:attempt_id>/', views.attempt_detail, name='attempt_detail'),
    path('<slug:course_slug>/quiz/', views.take_course_quiz, name='take_course_quiz'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
```

### 15.2 `courses/views.py` — додай

```python
@login_required
def attempt_detail(request, attempt_id):
    attempt = get_object_or_404(UserAttempt, pk=attempt_id, user=request.user)
    return render(request, 'courses/attempt_detail.html', {'attempt': attempt})
```

**Пояснення:**

- **`user=request.user`** — захист: користувач бачить лише свої спроби

### 15.3 `courses/templates/courses/attempt_detail.html`

```html
{% extends 'base.html' %}

{% block title %}Attempt — {{ attempt.quiz.title }}{% endblock %}

{% block content %}
<h1>{{ attempt.quiz.title }}</h1>
<p>Score: {{ attempt.score }}%</p>
<p>{% if attempt.passed %}Passed{% else %}Not passed{% endif %}</p>
<p><small>{{ attempt.created_at }}</small></p>

<h2>Details</h2>
{% for ua in attempt.user_answers.all %}
    <fieldset>
        <legend>
            {{ forloop.counter }}. {{ ua.question.text }}
            {% if ua.is_correct %}✓{% else %}✗{% endif %}
        </legend>
        {% for answer in ua.question.answers.all %}
            <div>
                {{ answer.text }}
                {% if answer in ua.selected.all %}(your choice){% endif %}
                {% if answer.is_correct %}(correct){% endif %}
            </div>
        {% endfor %}
    </fieldset>
{% endfor %}

<p><a href="#">My Results</a></p>
{% endblock %}
```

### ✅ Перевірка Кроку 15

1. Пройди тест із частково правильними відповідями
2. Після Submit — редірект на `/my-results/<id>/`
3. Побачиш кожне питання з `(your choice)` і `(correct)`

---

## Крок 16: Мої результати

### 16.1 `courses/views.py` — додай

```python
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
```

### 16.2 `courses/templates/courses/my_results.html`

```html
{% extends 'base.html' %}

{% block title %}My Results{% endblock %}

{% block content %}
<h1>My Results</h1>

{% if attempts %}
    <p>Total: {{ attempts.count }} | Passed: {{ passed_count }} | Failed: {{ failed_count }} | Average: {{ average_score }}%</p>
    <ul>
    {% for attempt in attempts %}
        <li>
            <a href="{% url 'courses:attempt_detail' attempt.id %}">{{ attempt.quiz.title }}</a>
            — {{ attempt.score }}% {% if attempt.passed %}(passed){% else %}(failed){% endif %}
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>No attempts yet.</p>
{% endif %}
{% endblock %}
```

### 16.3 Онови `templates/base.html` — додай «Results»

```html
{% if user.is_authenticated %}
    <a href="{% url 'courses:my_results' %}">Results</a> |
    ...
{% endif %}
```

### 16.4 Онови `attempt_detail.html`

Заміни `<a href="#">My Results</a>` на:

```html
<a href="{% url 'courses:my_results' %}">My Results</a>
```

### ✅ Перевірка Кроку 16

- *http://127.0.0.1:8000/my-results/* — список спроб + статистика
- Клік на спробу → деталізація

---

## Крок 17: Коментарі

### 17.1 `courses/views.py` — заміни `lesson_detail`

Додай у імпорт `Comment`:

```python
from .models import (
    Category, Course, Lesson, Quiz,
    UserAttempt, UserAnswer, Comment,
)
```

Заміни `lesson_detail`:

```python
@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, module__course=course)

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
```

### 17.2 Онови `lesson_detail.html` — додай коментарі

Додай перед закриваючим `{% endblock %}`:

```html
<hr>
<h2 id="comments">Comments</h2>

{% if user.is_authenticated %}
<form method="post">
    {% csrf_token %}
    <textarea name="text" rows="3" cols="50" placeholder="Write a comment..."></textarea><br>
    <button type="submit">Post</button>
</form>
{% else %}
<p><a href="{% url 'login' %}?next={{ request.path }}">Login</a> to comment</p>
{% endif %}

{% for comment in lesson.comments.all %}
    {% if not comment.parent %}
        <div>
            <strong>{{ comment.author }}</strong>: {{ comment.text }}
            <br><small>{{ comment.created_at }}</small>

            {% for reply in comment.replies.all %}
                <div style="margin-left:2rem;">
                    <strong>{{ reply.author }}</strong>: {{ reply.text }}
                </div>
            {% endfor %}

            {% if user.is_authenticated %}
                <a href="#reply-form-{{ comment.id }}"
                   onclick="toggleReply(event, {{ comment.id }})">Reply</a>
                <form method="post" id="reply-form-{{ comment.id }}" style="display:none;">
                    {% csrf_token %}
                    <input type="hidden" name="parent_id" value="{{ comment.id }}">
                    <input type="text" name="text" placeholder="Reply...">
                    <button type="submit">Send</button>
                </form>
            {% endif %}
        </div>
    {% endif %}
{% endfor %}

<script>
function toggleReply(event, id) {
    event.preventDefault();
    var form = document.getElementById('reply-form-' + id);
    form.style.display = (form.style.display === 'none') ? 'block' : 'none';
}
</script>
```

### ✅ Перевірка Кроку 17

1. Увійди, відкрий урок, напиши коментар → Post
2. Клікни «Reply» під коментарем → форма розкриється
3. Напиши відповідь → Send → з'явиться з відступом

---

## Крок 18: Markdown

### 18.1 `courses/templatetags/markdown_extras.py`

```python
import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


def _escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


@register.filter(name='markdown_inline')
@stringfilter
def markdown_inline_filter(value):
    value = _escape_html(value)
    return mark_safe(_inline(value))


@register.filter(name='markdown')
@stringfilter
def markdown_filter(value):
    code_blocks = []

    def _save_code(match):
        code_blocks.append(match.group(1))
        return f'\x00CODE{len(code_blocks) - 1}\x00'

    value = re.sub(r'```[^\n]*\n(.*?)```', _save_code, value, flags=re.DOTALL)

    lines = value.split('\n')
    html_parts = []
    in_ul = False
    paragraph = []

    def flush_paragraph():
        if paragraph:
            html_parts.append('<p>' + _inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    def flush_list():
        nonlocal in_ul
        if in_ul:
            html_parts.append('</ul>')
            in_ul = False

    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_paragraph()
            flush_list()
            level = len(m.group(1))
            html_parts.append(f'<h{level}>{_inline(m.group(2))}</h{level}>')
            continue

        if line.startswith('- '):
            flush_paragraph()
            if not in_ul:
                html_parts.append('<ul>')
                in_ul = True
            html_parts.append(f'<li>{_inline(line[2:])}</li>')
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        if line.strip().startswith('<iframe'):
            flush_paragraph()
            flush_list()
            html_parts.append(line)
            continue

        if line.startswith('\x00CODE'):
            flush_paragraph()
            flush_list()
            html_parts.append(line)
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()

    result = '\n'.join(html_parts)

    for i, code in enumerate(code_blocks):
        result = result.replace(
            f'\x00CODE{i}\x00',
            f'<pre><code>{_escape_html(code)}</code></pre>'
        )

    return mark_safe(result)


@register.filter(name='markdown_safe')
@stringfilter
def markdown_safe_filter(value):
    value = _escape_html(value)
    return markdown_filter(value)
```

### 18.2 Онови `lesson_detail.html`

На початку шаблону:

```html
{% extends 'base.html' %}
{% load markdown_extras %}
```

Заміни `<div>{{ lesson.content }}</div>` на:

```html
<div>{{ lesson.content|markdown }}</div>
```

Заміни `{{ comment.text }}` на `{{ comment.text|markdown_safe }}`, і `{{ reply.text }}` на `{{ reply.text|markdown_safe }}`.

### ✅ Перевірка Кроку 18

1. **Перезапусти сервер** — Django кешує `templatetags`
2. Відкрий урок — побачиш відрендерений Markdown
3. Блоки коду — з сірим фоном
4. Коментар із `**жирним**` → відрендериться

---

# ЧАСТИНА 3: Tailwind CSS

## Крок 19: Підключення Tailwind + темна тема

### 19.1 `templates/base.html` — повний файл

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}LearnHub{% endblock %}</title>
    <script>
        (function() {
            const theme = localStorage.getItem('theme');
            if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            }
        })();
    </script>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        accent: {
                            DEFAULT: '#3eaf7c',
                            dark: '#369a6a',
                        },
                    },
                    maxWidth: {
                        content: '740px',
                        page: '1100px',
                        wide: '1280px',
                    },
                },
            },
        }
    </script>
    <style>
        .prose code {
            font-weight: 400;
            background-color: #f0f0f0;
            color: #2c3e50;
            padding: 0.15rem 0.35rem;
            border-radius: 3px;
            font-size: 0.9em;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        }

        .prose code::before,
        .prose code::after {
            content: none;
        }

        .prose pre {
            background-color: #f6f6f6;
            color: #2c3e50;
            padding: 1rem;
            border-radius: 0;
            border: none;
            overflow-x: auto;
            font-size: 0.875rem;
            line-height: 1.6;
        }

        .prose pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            font-size: inherit;
            font-weight: 400;
        }

        .dark .prose code {
            background-color: #252525;
            color: #eaecef;
        }

        .dark .prose pre {
            background-color: #252525;
            color: #eaecef;
            border-color: #2c2c2c;
        }
    </style>
</head>
<body class="bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 antialiased">

<header class="sticky top-0 z-30 bg-white dark:bg-[#1a1a1a] border-b border-gray-200 dark:border-[#2c2c2c]">
    <div class="max-w-wide mx-auto px-4 h-16 flex items-center gap-6">
        <a href="{% url 'courses:course_list' %}" class="flex items-center gap-2 font-semibold text-lg hover:text-accent transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none" class="w-7 h-7 text-accent">
                <path d="M4 8c4-2 8-2 12 0v18c-4-2-8-2-12 0V8z" fill="currentColor" opacity="0.2" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>
                <path d="M28 8c-4-2-8-2-12 0v18c4-2 8-2 12 0V8z" fill="currentColor" opacity="0.1" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>
                <path d="M16 8v18" stroke="currentColor" stroke-width="1.75"/>
                <path d="M22 8v8l-2-1.5L18 16V8h4z" fill="currentColor"/>
            </svg>
            <span>LearnHub</span>
        </a>

        <nav class="hidden md:flex items-center gap-6 text-sm text-gray-600 dark:text-gray-400">
            <a href="{% url 'courses:course_list' %}"
               class="{% if request.resolver_match.url_name == 'course_list' %}text-accent font-medium{% else %}hover:text-gray-900 dark:hover:text-gray-100{% endif %}">
                Courses
            </a>
            <a href="{% url 'courses:quiz_list' %}"
               class="{% if request.resolver_match.url_name == 'quiz_list' %}text-accent font-medium{% else %}hover:text-gray-900 dark:hover:text-gray-100{% endif %}">
                Quizzes
            </a>
            {% if user.is_authenticated %}
                <a href="{% url 'courses:my_results' %}"
                   class="{% if request.resolver_match.url_name == 'my_results' %}text-accent font-medium{% else %}hover:text-gray-900 dark:hover:text-gray-100{% endif %}">
                    Results
                </a>
            {% endif %}
        </nav>

        <div class="ml-auto flex items-center gap-3 text-sm">
            {% if user.is_authenticated %}
                <span class="hidden sm:inline text-gray-600 dark:text-gray-400">
                    Welcome, {{ user.get_full_name|default:user.username }}
                </span>
                <form method="post" action="{% url 'logout' %}" class="inline">
                    {% csrf_token %}
                    <button type="submit" class="text-gray-600 dark:text-gray-400 hover:text-accent">Logout</button>
                </form>
            {% else %}
                <a href="{% url 'login' %}" class="text-gray-600 dark:text-gray-400 hover:text-accent">Login</a>
                <a href="{% url 'register' %}" class="text-gray-600 dark:text-gray-400 hover:text-accent">Register</a>
            {% endif %}

            <button type="button" onclick="toggleTheme()"
                    class="relative inline-flex items-center w-10 h-5 rounded-full transition-colors
                           bg-gray-200 dark:bg-[#252525]"
                    aria-label="Toggle theme">
                <span class="absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white shadow-sm
                             flex items-center justify-center text-[10px] leading-none
                             transition-transform duration-200
                             dark:translate-x-5">
                    <span class="hidden dark:inline">☀</span>
                    <span class="inline dark:hidden">☾</span>
                </span>
            </button>
        </div>
    </div>
</header>

{% block content_full %}
<main class="max-w-wide mx-auto px-6 py-12">
    {% block content %}{% endblock %}
</main>
{% endblock %}

<footer class="border-t border-gray-200 dark:border-[#2c2c2c] mt-20">
    <div class="max-w-wide mx-auto px-6 py-8 text-sm text-gray-500 dark:text-gray-400">
        LearnHub — simple learning platform
    </div>
</footer>

<script>
function toggleTheme() {
    const html = document.documentElement;
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}
</script>

</body>
</html>
```

**Пояснення:**

- **`?plugins=typography`** — підключає плагін `prose`
- **`tailwind.config`** — кастомний акцент `#3eaf7c`, `max-w-wide`, `darkMode: 'class'`
- **Скрипт у `<head>`** — застосовує тему до рендеру (без блимання)
- **`<style>`** — перекриває Tailwind Typography для `.prose code` і `.prose pre` (без лапок, без рамки, без заокруглення)

### ✅ Перевірка Кроку 19

- Онови сторінку — стилізований хедер
- Перемикач теми → тема змінюється
- Онови — тема збереглась

---

## Крок 20: Рестайл сторінок

### 20.1 `courses/templates/courses/course_list.html`

```html
{% extends 'base.html' %}

{% block title %}Courses{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <h1 class="text-3xl font-semibold mb-6 pb-2">Courses</h1>

    {% if not user.is_authenticated %}
        <p class="mb-6 text-[#476582] dark:text-[#9ba9b8]">
            Please <a href="{% url 'login' %}?next={{ request.path }}" class="text-accent hover:underline">login</a> to view course content.
        </p>
    {% endif %}

    <div class="mb-8 flex flex-wrap items-center gap-2 text-sm">
        <a href="{% url 'courses:course_list' %}"
           class="inline-flex items-center gap-1 px-3 py-1.5 rounded font-medium transition-colors
                  {% if not selected_category %}bg-accent text-white hover:bg-accent-dark{% else %}bg-white dark:bg-[#252525] text-[#2c3e50] dark:text-[#eaecef] border border-gray-200 dark:border-[#2c2c2c] hover:border-gray-300 dark:hover:border-[#3a3a3a]{% endif %}">
            All
            <span class="text-xs opacity-70">{{ total_count }}</span>
        </a>

        {% for category in categories %}
            <a href="{% url 'courses:course_list' %}?category={{ category.slug }}"
               class="inline-flex items-center gap-1 px-3 py-1.5 rounded font-medium transition-colors
                      {% if selected_category == category.slug %}bg-accent text-white hover:bg-accent-dark{% else %}bg-white dark:bg-[#252525] text-[#2c3e50] dark:text-[#eaecef] border border-gray-200 dark:border-[#2c2c2c] hover:border-gray-300 dark:hover:border-[#3a3a3a]{% endif %}">
                {{ category.title }}
                <span class="text-xs opacity-70">{{ category.course_count }}</span>
            </a>
        {% endfor %}
    </div>

    {% if page_obj %}
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for course in page_obj %}
                <article class="flex flex-col gap-6 rounded-xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">

                    <header>
                        <div class="flex items-center justify-between">
                            {% if course.category %}
                                <a href="{% url 'courses:course_list' %}?category={{ course.category.slug }}"
                                   class="inline-flex items-center gap-1.5 rounded-full border border-zinc-200 bg-zinc-100 px-2.5 py-1 text-xs font-medium text-zinc-700 transition-colors hover:border-accent hover:text-accent dark:border-zinc-800 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:border-accent dark:hover:text-accent">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-3.5 h-3.5">
                                        <path d="M6 14l1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"></path>
                                    </svg>
                                    {{ course.category.title }}
                                </a>
                            {% else %}
                                <span></span>
                            {% endif %}
                        </div>

                        <h3 class="mt-3 text-lg font-semibold">
                            <a href="{% url 'courses:course_detail' course.slug %}" class="hover:text-accent transition-colors">
                                {{ course.title }}
                            </a>
                        </h3>
                        {% if course.description %}
                            <p class="mt-1 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
                                {{ course.description|truncatewords:15 }}
                            </p>
                        {% endif %}
                    </header>

                    <section class="flex gap-4 text-xs text-zinc-500 dark:text-zinc-400">
                        <span class="flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                            </svg>
                            {{ course.lesson_count }} lesson{{ course.lesson_count|pluralize }}
                        </span>
                        {% if course.quiz %}
                            <span class="flex items-center gap-1">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                                </svg>
                                Quiz
                            </span>
                        {% endif %}
                    </section>

                    <footer class="mt-auto">
                        <a href="{% url 'courses:course_detail' course.slug %}"
                           class="inline-flex w-full items-center justify-center rounded-md bg-[#D8EFE5] px-4 py-2 text-sm font-medium text-zinc-800 shadow-sm transition-colors hover:bg-[#C5E5D7] dark:bg-[#2a3d35] dark:text-zinc-100 dark:hover:bg-[#354a41]">
                            Start course
                        </a>
                    </footer>
                </article>
            {% empty %}
                <p class="col-span-full text-center text-[#476582] dark:text-[#9ba9b8] py-8">
                    No courses in this category.
                </p>
            {% endfor %}
        </div>

        {% if page_obj.has_other_pages %}
            <nav class="mt-8 flex justify-center items-center gap-2 text-sm">
                {% if page_obj.has_previous %}
                    <a href="?{% if selected_category %}category={{ selected_category }}&{% endif %}page={{ page_obj.previous_page_number }}"
                       class="inline-flex items-center gap-1 px-3 py-1 rounded border border-gray-200 dark:border-[#2c2c2c] text-[#476582] dark:text-[#9ba9b8] hover:text-accent hover:border-accent">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                            <polyline points="11 17 6 12 11 7"></polyline>
                            <polyline points="18 17 13 12 18 7"></polyline>
                        </svg>
                        <span>Prev</span>
                    </a>
                {% else %}
                    <span class="inline-flex items-center gap-1 px-3 py-1 rounded border border-gray-100 dark:border-[#222] text-gray-300 dark:text-[#444]">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                            <polyline points="11 17 6 12 11 7"></polyline>
                            <polyline points="18 17 13 12 18 7"></polyline>
                        </svg>
                        <span>Prev</span>
                    </span>
                {% endif %}

                {% for num in page_obj.paginator.page_range %}
                    {% if num == page_obj.number %}
                        <span class="px-3 py-1 rounded bg-accent text-white">{{ num }}</span>
                    {% else %}
                        <a href="?{% if selected_category %}category={{ selected_category }}&{% endif %}page={{ num }}"
                           class="px-3 py-1 rounded border border-gray-200 dark:border-[#2c2c2c] text-[#476582] dark:text-[#9ba9b8] hover:text-accent hover:border-accent">{{ num }}</a>
                    {% endif %}
                {% endfor %}

                {% if page_obj.has_next %}
                    <a href="?{% if selected_category %}category={{ selected_category }}&{% endif %}page={{ page_obj.next_page_number }}"
                       class="inline-flex items-center gap-1 px-3 py-1 rounded border border-gray-200 dark:border-[#2c2c2c] text-[#476582] dark:text-[#9ba9b8] hover:text-accent hover:border-accent">
                        <span>Next</span>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                            <polyline points="13 17 18 12 13 7"></polyline>
                            <polyline points="6 17 11 12 6 7"></polyline>
                        </svg>
                    </a>
                {% else %}
                    <span class="inline-flex items-center gap-1 px-3 py-1 rounded border border-gray-100 dark:border-[#222] text-gray-300 dark:text-[#444]">
                        <span>Next</span>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                            <polyline points="13 17 18 12 13 7"></polyline>
                            <polyline points="6 17 11 12 6 7"></polyline>
                        </svg>
                    </span>
                {% endif %}
            </nav>
        {% endif %}
    {% else %}
        <p class="text-center text-[#476582] dark:text-[#9ba9b8] py-8">No courses yet.</p>
    {% endif %}
</div>
{% endblock %}
```

### 20.2 Повні шаблони

Нижче наведені повні версії решти шаблонів, звірені з однойменними файлами у репозиторії. Шлях до кожного файла вказаний у заголовку.


#### `courses/templates/courses/course_detail.html`

```html
{% extends 'base.html' %}

{% block title %}{{ course.title }}{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">

    <header class="mb-8">
        <h1 class="text-3xl font-semibold mb-3">{{ course.title }}</h1>
        {% if course.category %}
            <span class="inline-block text-xs px-2.5 py-1 rounded-full bg-gray-100 dark:bg-[#252525] text-gray-600 dark:text-gray-400">
                {{ course.category.title }}
            </span>
        {% endif %}
        {% if course.description %}
            <p class="mt-4 text-gray-600 dark:text-gray-400 leading-relaxed">{{ course.description }}</p>
        {% endif %}
    </header>

    {% if course.modules.all %}
        <div class="space-y-10">
            {% for module in course.modules.all %}
                <section>
                    <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
                        <h2 class="text-xl font-semibold flex items-center gap-3">
                            <span class="w-7 h-7 rounded-full bg-accent/10 text-accent text-sm font-semibold flex items-center justify-center">
                                {{ forloop.counter }}
                            </span>
                            {{ module.title }}
                        </h2>
                    </div>

                    <ul class="space-y-1">
                        {% for lesson in module.lessons.all %}
                            <li>
                                <a href="{% url 'courses:lesson_detail' course.slug lesson.slug %}"
                                   class="group flex items-center gap-3 px-3 py-2 -mx-3 rounded-lg hover:bg-gray-50 dark:hover:bg-[#252525] transition-colors">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 text-gray-400 dark:text-gray-500 group-hover:text-accent shrink-0">
                                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                        <polyline points="14 2 14 8 20 8"></polyline>
                                    </svg>
                                    <span class="text-gray-900 dark:text-gray-100 group-hover:text-accent transition-colors">
                                        {{ lesson.title }}
                                    </span>
                                </a>
                            </li>
                        {% endfor %}
                    </ul>
                </section>
            {% endfor %}
        </div>

        {% if course.quiz %}
            <div class="mt-12 bg-gray-50 dark:bg-[#252525] rounded-lg p-6 flex flex-wrap items-center gap-4">
                <div class="flex-1 min-w-0">
                    <h3 class="font-semibold mb-1">Ready for the final quiz?</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Test your knowledge of {{ course.title }}.</p>
                </div>
                <a href="{% url 'courses:take_course_quiz' course.slug %}"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent text-white hover:bg-accent-dark font-medium text-sm shrink-0">
                    <span>Start quiz</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </a>
            </div>
        {% endif %}
    {% else %}
        <div class="border border-dashed border-gray-300 dark:border-[#3a3a3a] rounded-lg p-12 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="w-14 h-14 mx-auto mb-4 text-gray-300 dark:text-[#3a3a3a]">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="9" y1="13" x2="15" y2="13"></line>
                <line x1="9" y1="17" x2="13" y2="17"></line>
            </svg>
            <h2 class="text-xl font-semibold mb-2">No lessons yet</h2>
            <p class="text-gray-600 dark:text-gray-400 max-w-md mx-auto mb-6">
                This course doesn't have any modules or lessons yet. Check back later or explore other courses.
            </p>

            <div class="flex flex-wrap justify-center gap-3">
                <a href="{% url 'courses:course_list' %}"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent text-white hover:bg-accent-dark font-medium text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                        <line x1="8" y1="6" x2="21" y2="6"></line>
                        <line x1="8" y1="12" x2="21" y2="12"></line>
                        <line x1="8" y1="18" x2="21" y2="18"></line>
                        <line x1="3" y1="6" x2="3.01" y2="6"></line>
                        <line x1="3" y1="12" x2="3.01" y2="12"></line>
                        <line x1="3" y1="18" x2="3.01" y2="18"></line>
                    </svg>
                    <span>All courses</span>
                </a>

                <a href="{% url 'courses:quiz_list' %}"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-gray-100 dark:bg-[#2c2c2c] text-gray-900 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#3a3a3a] font-medium text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                        <path d="M9 11H3v10h6V11z"></path>
                        <path d="M21 3h-6v18h6V3z"></path>
                        <path d="M15 7H9v14h6V7z"></path>
                    </svg>
                    <span>All quizzes</span>
                </a>
            </div>
        </div>
    {% endif %}

</div>
{% endblock %}
```


#### `courses/templates/courses/lesson_detail.html`

```html
{% extends 'base.html' %}
{% load markdown_extras %}

{% block title %}{{ lesson.title }}{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <div class="lg:grid lg:grid-cols-[280px_1fr] lg:gap-12">

        <aside class="hidden lg:block">
            <div class="sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto pr-2">

                <div class="text-xs uppercase tracking-wider text-[#476582] dark:text-[#9ba9b8] font-semibold mb-6">
                    Course contents
                </div>

                <nav class="space-y-8">
                    {% for module in course.modules.all %}
                        <div>
                            <div class="text-sm font-semibold text-[#2c3e50] dark:text-[#eaecef] mb-3 pl-1">
                                {{ module.title }}
                            </div>
                            <ul class="space-y-1.5 border-l-2 border-gray-100 dark:border-[#2c2c2c]">
                            {% for l in module.lessons.all %}
                                <li>
                                    {% if l.id == lesson.id %}
                                        <span class="block pl-4 pr-2 py-1 -ml-0.5 border-l-2 border-accent text-accent text-sm font-medium leading-snug">
                                            {{ l.title }}
                                        </span>
                                    {% else %}
                                        <a href="{% url 'courses:lesson_detail' course.slug l.slug %}"
                                           class="block pl-4 pr-2 py-1 -ml-0.5 border-l-2 border-transparent text-sm text-[#476582] dark:text-[#9ba9b8] hover:text-accent hover:border-accent transition-colors leading-snug">
                                            {{ l.title }}
                                        </a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                            </ul>
                        </div>
                    {% endfor %}
                </nav>

                <div class="mt-8 pt-6 border-t border-gray-200 dark:border-[#2c2c2c]">
                    <a href="{% url 'courses:course_detail' course.slug %}"
                       class="inline-flex items-center gap-1.5 text-sm text-[#476582] dark:text-[#9ba9b8] hover:text-accent transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                            <path d="m17 2 4 4-4 4"></path>
                            <path d="M3 11v-1a4 4 0 0 1 4-4h14"></path>
                            <path d="m7 22-4-4 4-4"></path>
                            <path d="M21 13v1a4 4 0 0 1-4 4H3"></path>
                        </svg>
                        <span>Restart course</span>
                    </a>
                </div>
        </aside>

        <div class="min-w-0">

            <details class="lg:hidden mb-6 border border-gray-200 dark:border-[#2c2c2c] rounded">
                <summary class="cursor-pointer px-4 py-2 text-sm font-medium text-[#476582] dark:text-[#9ba9b8]">
                    Contents — {{ course.title }}
                </summary>
                <div class="px-4 py-3 border-t border-gray-200 dark:border-[#2c2c2c]">
                    {% for module in course.modules.all %}
                        <div class="mb-4">
                            <div class="text-sm font-semibold mb-2">{{ module.title }}</div>
                            <ul class="space-y-1 ml-3">
                            {% for l in module.lessons.all %}
                                <li>
                                    {% if l.id == lesson.id %}
                                        <span class="text-sm text-accent font-medium">{{ l.title }} (current)</span>
                                    {% else %}
                                        <a href="{% url 'courses:lesson_detail' course.slug l.slug %}"
                                           class="text-sm text-[#476582] dark:text-[#9ba9b8] hover:text-accent">{{ l.title }}</a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                            </ul>
                        </div>
                    {% endfor %}
                </div>
            </details>

            <article class="prose prose-sm prose-slate dark:prose-invert max-w-none">
                {{ lesson.content|markdown }}
            </article>

            {% if not next_lesson and course.quiz %}
                <div class="mt-10 pt-6 border-t border-gray-200 dark:border-[#2c2c2c]">
                    <div class="bg-accent/5 dark:bg-accent/10 border border-accent/20 rounded-lg p-6 text-center">
                        <h2 class="text-lg font-semibold mb-2">Ready for the final quiz?</h2>
                        <p class="text-sm text-[#476582] dark:text-[#9ba9b8] mb-4">
                            You've reached the end of {{ course.title }}. Test your knowledge with the course quiz.
                        </p>
                        <a href="{% url 'courses:take_course_quiz' course.slug %}"
                           class="inline-flex items-center gap-2 px-5 py-2.5 rounded bg-accent text-white hover:bg-accent-dark font-medium">
                            <span>Start course quiz</span>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                                <path d="M4 6v12l8-6-8-6zm10 0v12l8-6-8-6z"/>
                            </svg>
                        </a>
                    </div>
                </div>
            {% endif %}

            <nav class="mt-12 grid grid-cols-2 gap-4 text-sm border-t border-gray-200 dark:border-[#2c2c2c] pt-6">
                <div>
                    {% if prev_lesson %}
                        <div class="text-xs uppercase tracking-wide text-[#476582] dark:text-[#9ba9b8] mb-1">Previous</div>
                        <a href="{% url 'courses:lesson_detail' course.slug prev_lesson.slug %}"
                           class="inline-flex items-center gap-1 text-accent hover:underline">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                                <line x1="19" y1="12" x2="5" y2="12"></line>
                                <polyline points="12 19 5 12 12 5"></polyline>
                            </svg>
                            <span>{{ prev_lesson.title }}</span>
                        </a>
                    {% endif %}
                </div>
                <div class="text-right">
                    {% if next_lesson %}
                        <div class="text-xs uppercase tracking-wide text-[#476582] dark:text-[#9ba9b8] mb-1">Next</div>
                        <a href="{% url 'courses:lesson_detail' course.slug next_lesson.slug %}"
                           class="inline-flex items-center gap-1 text-accent hover:underline">
                            <span>{{ next_lesson.title }}</span>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                                <polyline points="12 5 19 12 12 19"></polyline>
                            </svg>
                        </a>
                    {% endif %}
                </div>
            </nav>

            <section class="mt-16">
                <h2 id="comments" class="text-2xl font-semibold mb-6 pb-2 border-b border-gray-200 dark:border-[#2c2c2c]">
                    Comments
                </h2>

                {% if user.is_authenticated %}
                <form method="post" class="mb-8">
                    {% csrf_token %}
                    <textarea name="text" rows="3" placeholder="Write a comment..."
                              class="w-full px-3 py-2 rounded border border-gray-200 dark:border-[#2c2c2c] bg-white dark:bg-[#252525] focus:outline-none focus:border-accent text-sm"></textarea>
                    <button type="submit"
                            class="mt-2 px-4 py-1.5 rounded bg-accent text-white hover:bg-accent-dark text-sm font-medium">
                        Post
                    </button>
                </form>
                {% else %}
                <p class="mb-8 text-sm text-[#476582] dark:text-[#9ba9b8]">
                    <a href="{% url 'login' %}?next={{ request.path }}" class="text-accent hover:underline">Login</a> to comment
                </p>
                {% endif %}

                <div class="space-y-6">
                {% for comment in lesson.comments.all %}
                    {% if not comment.parent %}
                        <div class="pb-4 border-b border-gray-100 dark:border-[#2c2c2c]">
                            <div class="text-sm mb-2">
                                <strong class="text-[#2c3e50] dark:text-[#eaecef]">{{ comment.author }}</strong>
                                <span class="ml-2 text-xs text-[#476582] dark:text-[#9ba9b8]">{{ comment.created_at|date:"Y-m-d H:i" }}</span>
                            </div>
                            <div class="text-sm leading-relaxed mb-3 prose prose-sm dark:prose-invert max-w-none">{{ comment.text|markdown_safe }}</div>

                            {% for reply in comment.replies.all %}
                                <div class="ml-6 mt-3 pl-4 border-l-2 border-gray-200 dark:border-[#2c2c2c]">
                                    <div class="text-sm mb-1">
                                        <strong class="text-[#2c3e50] dark:text-[#eaecef]">{{ reply.author }}</strong>
                                        <span class="ml-2 text-xs text-[#476582] dark:text-[#9ba9b8]">{{ reply.created_at|date:"Y-m-d H:i" }}</span>
                                    </div>
                                    <div class="text-sm leading-relaxed prose prose-sm dark:prose-invert max-w-none">{{ reply.text|markdown_safe }}</div>
                                </div>
                            {% endfor %}

                            {% if user.is_authenticated %}
                                <a href="#reply-form-{{ comment.id }}"
                                   onclick="toggleReply(event, {{ comment.id }})"
                                   class="inline-flex items-center gap-1 mt-3 text-xs text-[#476582] dark:text-[#9ba9b8] hover:text-accent">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-3 h-3">
                                        <polyline points="9 14 4 9 9 4"></polyline>
                                        <path d="M20 20v-7a4 4 0 0 0-4-4H4"></path>
                                    </svg>
                                    <span>Reply</span>
                                </a>
                                <form method="post" id="reply-form-{{ comment.id }}" class="hidden mt-3">
                                    {% csrf_token %}
                                    <input type="hidden" name="parent_id" value="{{ comment.id }}">
                                    <textarea name="text" rows="3" placeholder="Reply..."
                                              class="w-full px-3 py-2 rounded border border-gray-200 dark:border-[#2c2c2c] bg-white dark:bg-[#252525] focus:outline-none focus:border-accent text-sm resize-y"></textarea>
                                    <button type="submit"
                                            class="mt-2 px-4 py-1.5 rounded bg-accent text-white hover:bg-accent-dark text-sm font-medium">
                                        Send
                                    </button>
                                </form>
                            {% endif %}
                        </div>
                    {% endif %}
                {% endfor %}
                </div>
            </section>

        </div>
    </div>
</div>

<script>
function toggleReply(event, id) {
    event.preventDefault();
    var form = document.getElementById('reply-form-' + id);
    form.classList.toggle('hidden');
}
</script>
{% endblock %}
```


#### `courses/templates/courses/quiz_list.html`

```html
{% extends 'base.html' %}

{% block title %}All Quizzes{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <h1 class="text-3xl font-semibold mb-5">All Quizzes</h1>

    {% if quizzes %}
        <ul class="space-y-3">
        {% for quiz in quizzes %}
            <li class="py-3 border-b border-gray-100 dark:border-[#2c2c2c]">
                <div class="font-medium">{{ quiz.title }}</div>
                <div class="text-xs text-[#476582] dark:text-[#9ba9b8] mt-1">
                    Course: {{ quiz.course.title }}
                </div>
                <div class="mt-2">
                    <a href="{% url 'courses:take_course_quiz' quiz.course.slug %}"
                       class="inline-flex items-center gap-1 text-sm text-accent hover:underline">
                        <span>Take quiz</span>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </a>
                </div>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p class="text-[#476582] dark:text-[#9ba9b8]">No quizzes yet.</p>
    {% endif %}
</div>
{% endblock %}
```


#### `courses/templates/courses/take_quiz.html`

```html
{% extends 'base.html' %}

{% block title %}{{ quiz.title }}{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <h1 class="text-3xl font-semibold mb-6 pb-2">{{ quiz.title }}</h1>

    <form method="post" action="{{ submit_url }}" class="space-y-6">
    {% csrf_token %}
    {% for question in quiz.questions.all %}
        <fieldset class="border-b border-gray-100 dark:border-[#2c2c2c] pb-4">
            <legend class="font-medium mb-3">{{ forloop.counter }}. {{ question.text }}</legend>
            <div class="space-y-2 text-sm">
            {% if question.question_type == 'single' %}
                {% for answer in question.answers.all %}
                    <label class="flex items-start gap-2 cursor-pointer hover:text-accent">
                        <input type="radio" name="question_{{ question.id }}" value="{{ answer.id }}"
                               class="mt-1 accent-[#3eaf7c]">
                        <span>{{ answer.text }}</span>
                    </label>
                {% endfor %}
            {% else %}
                {% for answer in question.answers.all %}
                    <label class="flex items-start gap-2 cursor-pointer hover:text-accent">
                        <input type="checkbox" name="question_{{ question.id }}" value="{{ answer.id }}"
                               class="mt-1 accent-[#3eaf7c]">
                        <span>{{ answer.text }}</span>
                    </label>
                {% endfor %}
            {% endif %}
            </div>
        </fieldset>
    {% endfor %}

    <button type="submit"
            class="px-6 py-2 rounded bg-accent text-white hover:bg-accent-dark font-medium">
        Submit
    </button>
    </form>
</div>
{% endblock %}
```


#### `courses/templates/courses/attempt_detail.html`

```html
{% extends 'base.html' %}

{% block title %}Attempt — {{ attempt.quiz.title }}{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <h1 class="text-3xl font-semibold mb-4 pb-2">
        {{ attempt.quiz.title }}
    </h1>

    <div class="mb-8 flex flex-wrap items-center gap-4">
        <span class="text-3xl font-semibold {% if attempt.passed %}text-accent{% else %}text-red-500{% endif %}">
            {{ attempt.score }}%
        </span>
        {% if attempt.passed %}
            <span class="px-3 py-1 rounded-full bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-sm">Passed</span>
        {% else %}
            <span class="px-3 py-1 rounded-full bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 text-sm">Not passed</span>
        {% endif %}
        <span class="text-sm text-[#476582] dark:text-[#9ba9b8]">{{ attempt.created_at }}</span>
    </div>

    <h2 class="text-xl font-semibold mb-4">Details</h2>

    <div class="space-y-6">
    {% for user_answer in attempt.user_answers.all %}
        <div class="border-b border-gray-100 dark:border-[#2c2c2c] pb-5">
            <div class="font-medium mb-3 text-sm flex items-center gap-2">
                <span>{{ forloop.counter }}. {{ user_answer.question.text }}</span>
                {% if user_answer.is_correct %}
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 text-accent">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                {% else %}
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 text-red-500">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                {% endif %}
            </div>
            <ul class="list-disc pl-6 space-y-1 text-sm text-[#2c3e50] dark:text-[#eaecef]">
            {% for answer in user_answer.question.answers.all %}
                <li>
                    <span>{{ answer.text }}</span>
                    {% if answer in user_answer.selected.all %}
                        <span class="ml-2 px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs">your choice</span>
                    {% endif %}
                    {% if answer.is_correct %}
                        <span class="ml-2 px-2 py-0.5 rounded bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs">correct</span>
                    {% endif %}
                </li>
            {% endfor %}
            </ul>
        </div>
    {% endfor %}
    </div>

    <div class="mt-10 pt-4 border-t border-gray-200 dark:border-[#2c2c2c] flex flex-wrap gap-4 text-sm">
        <a href="{% url 'courses:course_detail' attempt.quiz.course.slug %}"
           class="inline-flex items-center gap-1 text-accent hover:underline">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            <span>Back to course</span>
        </a>
        <a href="{% url 'courses:my_results' %}" class="text-accent hover:underline">My Results</a>
    </div>
</div>
{% endblock %}
```


#### `courses/templates/courses/my_results.html`

```html
{% extends 'base.html' %}

{% block title %}My Results{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">

    <h1 class="text-3xl font-semibold mb-8">My Results</h1>

    {% if attempts %}
        <div class="mb-8 grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="bg-gray-50 dark:bg-[#252525] rounded-lg p-4">
                <div class="text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1">Total attempts</div>
                <div class="text-2xl font-semibold">{{ attempts.count }}</div>
            </div>
            <div class="bg-gray-50 dark:bg-[#252525] rounded-lg p-4">
                <div class="text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1">Passed</div>
                <div class="text-2xl font-semibold text-accent">{{ passed_count }}</div>
            </div>
            <div class="bg-gray-50 dark:bg-[#252525] rounded-lg p-4">
                <div class="text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1">Failed</div>
                <div class="text-2xl font-semibold text-red-500">{{ failed_count }}</div>
            </div>
            <div class="bg-gray-50 dark:bg-[#252525] rounded-lg p-4">
                <div class="text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1">Average score</div>
                <div class="text-2xl font-semibold">{{ average_score }}%</div>
            </div>
        </div>

        <div class="space-y-3">
            {% for attempt in attempts %}
                <a href="{% url 'courses:attempt_detail' attempt.id %}"
                   class="block bg-gray-50 dark:bg-[#252525] rounded-lg p-4 hover:bg-gray-100 dark:hover:bg-[#2f2f2f] transition-colors">
                    <div class="flex flex-wrap items-center gap-4">
                        <div class="flex-1 min-w-0">
                            <div class="font-medium truncate">{{ attempt.quiz.title }}</div>
                            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                {{ attempt.quiz.course.title }}
                            </div>
                        </div>

                        <div class="flex items-center gap-4">
                            <span class="text-2xl font-semibold {% if attempt.passed %}text-accent{% else %}text-red-500{% endif %}">
                                {{ attempt.score }}%
                            </span>

                            {% if attempt.passed %}
                                <span class="px-2.5 py-1 rounded-full bg-accent/10 text-accent text-xs font-medium">
                                    Passed
                                </span>
                            {% else %}
                                <span class="px-2.5 py-1 rounded-full bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-xs font-medium">
                                    Failed
                                </span>
                            {% endif %}

                            <span class="hidden sm:inline text-xs text-gray-500 dark:text-gray-400">
                                {{ attempt.created_at|date:"M d, Y" }}
                            </span>
                        </div>
                    </div>
                </a>
            {% endfor %}
        </div>
    {% else %}
        <div class="border border-dashed border-gray-300 dark:border-[#3a3a3a] rounded-lg p-12 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="w-14 h-14 mx-auto mb-4 text-gray-300 dark:text-[#3a3a3a]">
                <path d="M9 11H3v10h6V11z"></path>
                <path d="M21 3h-6v18h6V3z"></path>
                <path d="M15 7H9v14h6V7z"></path>
            </svg>
            <h2 class="text-xl font-semibold mb-2">No attempts yet</h2>
            <p class="text-gray-600 dark:text-gray-400 max-w-md mx-auto mb-6">
                You haven't taken any quizzes yet. Explore courses and test your knowledge.
            </p>

            <div class="flex flex-wrap justify-center gap-3">
                <a href="{% url 'courses:course_list' %}"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent text-white hover:bg-accent-dark font-medium text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                        <line x1="8" y1="6" x2="21" y2="6"></line>
                        <line x1="8" y1="12" x2="21" y2="12"></line>
                        <line x1="8" y1="18" x2="21" y2="18"></line>
                        <line x1="3" y1="6" x2="3.01" y2="6"></line>
                        <line x1="3" y1="12" x2="3.01" y2="12"></line>
                        <line x1="3" y1="18" x2="3.01" y2="18"></line>
                    </svg>
                    <span>All courses</span>
                </a>

                <a href="{% url 'courses:quiz_list' %}"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-gray-100 dark:bg-[#2c2c2c] text-gray-900 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-[#3a3a3a] font-medium text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                        <path d="M9 11H3v10h6V11z"></path>
                        <path d="M21 3h-6v18h6V3z"></path>
                        <path d="M15 7H9v14h6V7z"></path>
                    </svg>
                    <span>All quizzes</span>
                </a>
            </div>
        </div>
    {% endif %}

</div>
{% endblock %}
```


#### `courses/templates/registration/login.html`

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <div class="max-w-sm mx-auto mt-8">
        <h1 class="text-3xl font-semibold mb-6 pb-2">Login</h1>

        <form method="post" class="space-y-5">
            {% csrf_token %}

            {% if form.non_field_errors %}
                <div class="text-sm text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900 rounded px-3 py-2 bg-red-50 dark:bg-red-900/20">
                    {{ form.non_field_errors }}
                </div>
            {% endif %}

            {% for field in form %}
                <div>
                    <label for="{{ field.id_for_label }}" class="block text-sm font-medium mb-1">
                        {{ field.label }}
                    </label>
                    <input type="{{ field.field.widget.input_type }}"
                           name="{{ field.name }}"
                           id="{{ field.id_for_label }}"
                           {% if field.value %}value="{{ field.value }}"{% endif %}
                           {% if field.field.required %}required{% endif %}
                           class="w-full px-3 py-2 rounded border text-sm
                                  bg-white dark:bg-[#252525]
                                  border-gray-200 dark:border-[#2c2c2c]
                                  focus:outline-none focus:border-accent
                                  {% if field.errors %}border-red-400 dark:border-red-800{% endif %}">

                    {% if field.errors %}
                        <div class="mt-1 text-xs text-red-600 dark:text-red-400">
                            {{ field.errors }}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            <button type="submit"
                    class="w-full px-4 py-2 rounded bg-accent text-white hover:bg-accent-dark font-medium">
                Login
            </button>
        </form>

        <p class="mt-6 text-sm text-[#476582] dark:text-[#9ba9b8]">
            Don't have an account yet? Create one to start learning —
            <a href="{% url 'register' %}" class="text-accent hover:underline">Register</a>
        </p>
    </div>
</div>
{% endblock %}
```


#### `courses/templates/registration/register.html`

```html
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content_full %}
<div class="max-w-page mx-auto px-4 py-8">
    <div class="max-w-sm mx-auto mt-8">
        <h1 class="text-3xl font-semibold mb-6 pb-2">Register</h1>

        <form method="post" class="space-y-5">
            {% csrf_token %}

            {% if form.non_field_errors %}
                <div class="text-sm text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900 rounded px-3 py-2 bg-red-50 dark:bg-red-900/20">
                    {{ form.non_field_errors }}
                </div>
            {% endif %}

            {% for field in form %}
                <div>
                    <label for="{{ field.id_for_label }}" class="block text-sm font-medium mb-1">
                        {{ field.label }}
                    </label>
                    <input type="{{ field.field.widget.input_type }}"
                           name="{{ field.name }}"
                           id="{{ field.id_for_label }}"
                           {% if field.value %}value="{{ field.value }}"{% endif %}
                           {% if field.field.required %}required{% endif %}
                           class="w-full px-3 py-2 rounded border text-sm
                                  bg-white dark:bg-[#252525]
                                  border-gray-200 dark:border-[#2c2c2c]
                                  focus:outline-none focus:border-accent
                                  {% if field.errors %}border-red-400 dark:border-red-800{% endif %}">

                    {% if field.help_text %}
                        <div class="mt-1 text-xs text-[#476582] dark:text-[#9ba9b8] leading-relaxed
                                    [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:my-1 [&_li]:my-0.5">
                            {{ field.help_text }}
                        </div>
                    {% endif %}

                    {% if field.errors %}
                        <div class="mt-1 text-xs text-red-600 dark:text-red-400">
                            {{ field.errors }}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            <button type="submit"
                    class="w-full px-4 py-2 rounded bg-accent text-white hover:bg-accent-dark font-medium">
                Register
            </button>
        </form>

        <p class="mt-6 text-sm text-[#476582] dark:text-[#9ba9b8]">
            Already have an account?
            <a href="{% url 'login' %}" class="text-accent hover:underline">Login</a>
        </p>
    </div>
</div>
{% endblock %}
```
**Основні класи для уніфікації:**

- Обгортка: `max-w-wide mx-auto px-6 py-12` (або `max-w-4xl` для коротких сторінок)
- Заголовок: `text-3xl font-semibold mb-8`
- Картки: `bg-gray-50 dark:bg-[#252525] rounded-lg p-4`
- Порожній стан: `border border-dashed border-gray-300 dark:border-[#3a3a3a] rounded-lg p-12 text-center`
- Кнопки: `rounded-lg bg-accent text-white hover:bg-accent-dark font-medium text-sm`
- Посилання: `text-accent hover:underline`

### ✅ Перевірка Кроку 20

Пройди всі сторінки:

- *http://127.0.0.1:8000/* — курси з фільтрами
- *http://127.0.0.1:8000/quizzes/* — тести
- *http://127.0.0.1:8000/my-results/* — результати
- *http://127.0.0.1:8000/accounts/login/* — вхід
- *http://127.0.0.1:8000/accounts/register/* — реєстрація
- Клік на курс → урок → коментарі
- Пройди тест

Перемкни тему. Перевір на мобільному розмірі (DevTools → responsive mode).

---

## Підсумок

- **Частина 1** — проєкт, моделі, admin, фікстури (5 файлів)
- **Частина 2** — публічні сторінки на голому HTML, `views.py` і `urls.py` наповнюються поступово
- **Частина 3** — Tailwind CSS, темна тема, рестайл

Після кожного кроку — перевірка: що має працювати, як виглядати, що показати в браузері.

---

## Додаток: повні актуальні Python-файли проєкту

Цей додаток містить повні поточні Python-файли проєкту. Він є остаточним знімком стану після покрокових прикладів вище; для порожніх `__init__.py` окремий лістинг не потрібен. HTML-шаблони та JSON-fixture наведені повністю у кроках 8, 19 і 20.

### `config/asgi.py`

```python
"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
```

### `config/settings.py`

```python
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 6.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ia4mmwfk6cx%!akwmj3te(6e=!cf!z!xx(@5#zvzx6df6c!@10'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'courses:course_list'
LOGOUT_REDIRECT_URL = 'courses:course_list'

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
```

### `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses import views as course_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', course_views.register, name='register'),
    path('', include('courses.urls')),
]
```

### `config/wsgi.py`

```python
"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
```

### `courses/admin.py`

```python
from django.contrib import admin
from .models import (
    Category, Course, Module, Lesson,
    Quiz, Question, Answer,
    UserAttempt, UserAnswer, Comment,
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    prepopulated_fields = {'slug': ('title',)}


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    min_num = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug']
    search_fields = ['title']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    list_display = ['title', 'slug', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['title']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    list_display = ['title', 'course', 'order']
    search_fields = ['title', 'course__title']
    autocomplete_fields = ['course']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'module', 'order']
    search_fields = ['title', 'module__title']
    autocomplete_fields = ['module']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'question_type', 'order']
    list_filter = ['question_type']
    inlines = [AnswerInline]
    search_fields = ['text']
    autocomplete_fields = ['quiz']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score']
    search_fields = ['title']
    autocomplete_fields = ['course']


admin.site.register(UserAttempt)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['question__text']
    autocomplete_fields = ['question']


admin.site.register(Comment)
```

### `courses/apps.py`

```python
from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'courses'
```

### `courses/forms.py`

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First name')
    last_name = forms.CharField(max_length=30, required=True, label='Last name')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
```

### `courses/migrations/0001_initial.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
```

### `courses/migrations/0002_module_lesson.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('content', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.module')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
```

### `courses/migrations/0003_question_answer_quiz_question_quiz_userattempt.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 13:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_module_lesson'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question_type', models.CharField(choices=[('single', 'Single answer (radio)'), ('multiple', 'Multiple answers (checkbox)')], default='single', max_length=10)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('passing_score', models.PositiveIntegerField(default=70)),
                ('lesson', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.lesson')),
                ('module', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.module')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.quiz'),
        ),
        migrations.CreateModel(
            name='UserAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('passed', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
```

### `courses/migrations/0004_useranswer.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_question_answer_quiz_question_quiz_userattempt'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField()),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='courses.userattempt')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
                ('selected', models.ManyToManyField(to='courses.answer')),
            ],
        ),
    ]
```

### `courses/migrations/0005_quiz_course.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_useranswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.course'),
        ),
    ]
```

### `courses/migrations/0006_category_course_category.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_quiz_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.category'),
        ),
    ]
```

### `courses/migrations/0007_comment.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 16:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_category_course_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.lesson')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='courses.comment')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
```

### `courses/migrations/0008_remove_quiz_lesson_remove_quiz_module_and_more.py`

```python
# Generated by Django 6.1.2 on 2026-10-14 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='module',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.course'),
        ),
    ]
```

### `courses/models.py`

```python
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    course = models.OneToOneField(
        Course, on_delete=models.CASCADE, related_name='quiz'
    )
    passing_score = models.PositiveIntegerField(default=70)

    def __str__(self):
        return self.title


class Question(models.Model):
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    QUESTION_TYPES = [
        (SINGLE, 'Single answer (radio)'),
        (MULTIPLE, 'Multiple answers (checkbox)'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=SINGLE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserAttempt(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()  # percentage
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.quiz} — {self.score}%"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.ManyToManyField(Answer)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.attempt} — {self.question.text[:30]}"

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"
```

### `courses/templatetags/markdown_extras.py`

```python
import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


def _escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


@register.filter(name='markdown_inline')
@stringfilter
def markdown_inline_filter(value):
    value = _escape_html(value)
    return mark_safe(_inline(value))


@register.filter(name='markdown')
@stringfilter
def markdown_filter(value):
    code_blocks = []

    def _save_code(match):
        code_blocks.append(match.group(1))
        return f'\x00CODE{len(code_blocks) - 1}\x00'

    value = re.sub(r'```[^\n]*\n(.*?)```', _save_code, value, flags=re.DOTALL)

    lines = value.split('\n')
    html_parts = []
    in_ul = False
    paragraph = []

    def flush_paragraph():
        if paragraph:
            html_parts.append('<p>' + _inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()

    def flush_list():
        nonlocal in_ul
        if in_ul:
            html_parts.append('</ul>')
            in_ul = False

    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_paragraph()
            flush_list()
            level = len(m.group(1))
            html_parts.append(f'<h{level}>{_inline(m.group(2))}</h{level}>')
            continue

        if line.startswith('- '):
            flush_paragraph()
            if not in_ul:
                html_parts.append('<ul>')
                in_ul = True
            html_parts.append(f'<li>{_inline(line[2:])}</li>')
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        if line.strip().startswith('<iframe'):
            flush_paragraph()
            flush_list()
            html_parts.append(line)
            continue

        if line.startswith('\x00CODE'):
            flush_paragraph()
            flush_list()
            html_parts.append(line)
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()

    result = '\n'.join(html_parts)

    for i, code in enumerate(code_blocks):
        result = result.replace(
            f'\x00CODE{i}\x00',
            f'<pre><code>{_escape_html(code)}</code></pre>'
        )

    return mark_safe(result)


@register.filter(name='markdown_safe')
@stringfilter
def markdown_safe_filter(value):
    value = _escape_html(value)
    return markdown_filter(value)
```

### `courses/tests.py`

```python
from django.test import TestCase

# Create your tests here.
```

### `courses/urls.py`

```python
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('my-results/', views.my_results, name='my_results'),
    path('my-results/<int:attempt_id>/', views.attempt_detail, name='attempt_detail'),
    path('<slug:course_slug>/quiz/', views.take_course_quiz, name='take_course_quiz'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
```

### `courses/views.py`

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import (
    Category, Course, Lesson,
    Quiz, Question, Answer,
    UserAttempt, UserAnswer, Comment,
)


def course_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.annotate(course_count=Count('courses'))

    courses_qs = Course.objects.annotate(lesson_count=Count('modules__lessons'))

    if category_slug:
        courses_qs = courses_qs.filter(category__slug=category_slug)

    total_count = Course.objects.count()

    paginator = Paginator(courses_qs, 6)
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
```

### `manage.py`

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

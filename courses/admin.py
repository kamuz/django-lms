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
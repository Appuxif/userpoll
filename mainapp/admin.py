from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from mainapp.models import (
    Member,
    Poll,
    Question,
    MemberAnswer,
)

TokenAdmin.raw_id_fields = ('user', )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    raw_id_fields = 'user',


# class MemberInline(admin.TabularInline):
#     model = Poll.members.through
#     extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'date_started',
        'date_ended',
    )
    raw_id_fields = 'members',
    inlines = (
        # MemberInline,
        QuestionInline,
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    raw_id_fields = 'poll',


@admin.register(MemberAnswer)
class MemberAnswerAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'question',
        'member',
    )

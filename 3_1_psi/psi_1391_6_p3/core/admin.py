from django.contrib import admin

# Register your models here.

from .models import Teacher, LabGroup, TheoryGroup, Student, Pair, \
    GroupConstraints, OtherConstraints


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class PairAdmin(admin.ModelAdmin):
    list_display = ('student1', 'student2', 'validated', 'studentBreakRequest')


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(LabGroup)
admin.site.register(TheoryGroup)
admin.site.register(Student)
admin.site.register(Pair, PairAdmin)
admin.site.register(GroupConstraints)
admin.site.register(OtherConstraints)

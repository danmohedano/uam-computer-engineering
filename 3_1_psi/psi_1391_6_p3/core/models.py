import django
from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "(T) " + self.last_name + ", " + self.first_name


class Group(models.Model):
    GROUP_NAME_MAX_LENGTH = 50
    LANGUAGE_MAX_LENGTH = 50
    groupName = models.CharField(max_length=GROUP_NAME_MAX_LENGTH)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH)

    class Meta:
        ordering = ['groupName']

    def __str__(self):
        return self.groupName


class TheoryGroup(Group):
    def __str__(self):
        return "(TG) " + super().__str__()


class LabGroup(Group):
    SCHEDULE_MAX_LENGTH = 50
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=SCHEDULE_MAX_LENGTH)
    maxNumberStudents = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return "(LG) " + super().__str__()


class Student(User):
    DECIMAL_PLACES = 2
    MAX_DIGITS = 4
    gradeTheoryLastYear = models.DecimalField(decimal_places=DECIMAL_PLACES,
                                              max_digits=MAX_DIGITS,
                                              default=0)
    gradeLabLastYear = models.DecimalField(decimal_places=DECIMAL_PLACES,
                                           max_digits=MAX_DIGITS,
                                           default=0)
    convalidationGranted = models.BooleanField(default=False)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE,
                                 null=True, blank=True)
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE,
                                    null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.last_name + ", " + self.first_name


class Pair(models.Model):
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE,
                                 related_name='student1')
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE,
                                 related_name='student2')
    validated = models.BooleanField(default=False)
    studentBreakRequest = models.ForeignKey(Student, null=True, blank=True,
                                            on_delete=models.CASCADE,
                                            related_name='studentBreakRequest')

    def __str__(self):
        return self.student1.__str__() + " + " + self.student2.__str__()


class GroupConstraints(models.Model):
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    theoryGroup = models.ForeignKey(TheoryGroup, on_delete=models.CASCADE)

    class Meta:
        ordering = ['labGroup', 'theoryGroup']
        verbose_name_plural = 'Group Constraints'

    def __str__(self):
        return "Group Constraint: " + self.labGroup.__str__() + ", " + \
               self.theoryGroup.__str__()


class OtherConstraints(models.Model):
    DECIMAL_PLACES = 2
    MAX_DIGITS = 4
    minGradeTheoryConv = models.DecimalField(decimal_places=DECIMAL_PLACES,
                                             max_digits=MAX_DIGITS,
                                             default=0)
    minGradeLabConv = models.DecimalField(decimal_places=DECIMAL_PLACES,
                                          max_digits=MAX_DIGITS,
                                          default=0)
    selectGroupStartDate = models.DateTimeField(default=django.utils.timezone.
                                                now)

    class Meta:
        verbose_name_plural = 'Other Constraints'

    def __str__(self):
        return "Min Grades: " + str(self.minGradeTheoryConv) + " (T), " + \
               str(self.minGradeLabConv) + " (L), " + \
               str(self.selectGroupStartDate)

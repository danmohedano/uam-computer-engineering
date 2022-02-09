# Populate database
# This file has to be placed within the
# core/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate

import os
from collections import OrderedDict
import django
import decimal
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import hashers
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'labassign.settings')

django.setup()
from core.models import (OtherConstraints, Pair, Student,
                         GroupConstraints, TheoryGroup,
                         LabGroup, Teacher)

import csv


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
#
# Teachers, groups and constraints
# will be hardcoded in this file.
# Students will be read from a csv file
# last year grade will be obtained from another csv file
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help="""
        model to  update:
        all -> all models
        teacher
        labgroup
        theorygroup
        groupconstraints
        otherconstrains
        student (require csv file)
        studentgrade (require different csv file,
        update only existing students)
        pair
        """)
        parser.add_argument('studentinfo', type=str, help="""CSV file with 
        student information
        header= NIE, DNI, Apellidos, Nombre, Teoría
        if NIE or DNI == 0 skip this entry and print a warning""")
        parser.add_argument('studentinfolastyear', type=str, help="""CSV file 
        with student information
        header= NIE,DNI,Apellidos,Nombre,Teoría, grade lab, grade the
        if NIE or DNI == 0 skip this entry and print a warning""")

    # handle is another compulsory name, do not change it"
    def handle(self, *args, **kwargs):
        model = kwargs['model']
        cvsStudentFile = kwargs['studentinfo']
        cvsStudentFileGrades = kwargs['studentinfolastyear']
        # clean database
        if model == 'all':
            self.cleanDataBase()
        if model == 'teacher' or model == 'all':
            self.teacher()
        if model == 'labgroup' or model == 'all':
            self.labgroup()
        if model == 'theorygroup' or model == 'all':
            self.theorygroup()
        if model == 'groupconstraints' or model == 'all':
            self.groupconstraints()
        if model == 'otherconstrains' or model == 'all':
            self.otherconstrains()
        if model == 'student' or model == 'all':
            self.student(cvsStudentFile)
        if model == 'studentgrade' or model == 'all':
            self.studentgrade(cvsStudentFileGrades)
        if model == 'pair' or model == 'all':
            self.pair()

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        # TODO Check correct functionality
        Teacher.objects.all().delete()
        LabGroup.objects.all().delete()
        TheoryGroup.objects.all().delete()
        Student.objects.all().delete()
        Pair.objects.all().delete()
        GroupConstraints.objects.all().delete()
        OtherConstraints.objects.all().delete()

        try:
            Student.objects.get(username='alumnodb')
        except Exception:
            Student.objects.create_superuser('alumnodb', 'a@a.es', 'alumnodb')

    def teacher(self):
        teacher_dict = {1: {'id': 1,  # 1261, L 18:00, 1271 X 18-20
                            'first_name': 'No',
                            'last_name': 'Asignado1', },
                        2: {'id': 2,  # 1262 X 18-20, 1263/1273 V 17-19
                            'first_name': 'No',
                            'last_name': 'Asignado4', },
                        3: {'id': 3,  # 1272 V 17-19, 1291 L 18-20
                            'first_name': 'Julia',
                            'last_name': 'Diaz Garcia', },
                        4: {'id': 4,  # 1292/1251V 17:00
                            'first_name': 'Alvaro',
                            'last_name': 'del Val Latorre', },
                        5: {'id': 5,  # 1201 X 18:00
                            'first_name': 'Roberto',
                            'last_name': 'Marabini Ruiz', }}

        for index, t in teacher_dict.items():
            add_teacher(identifier=t['id'], first_name=t['first_name'],
                        last_name=t['last_name'])

    def labgroup(self):
        max_number_students = 23
        lab_group_dict = {1261: {'id': 1261,  # 1261, L 18:00, 1271 X 18-20
                                 'groupName': '1261',
                                 'teacher': 1,
                                 'schedule': 'Lunes/Monday 18-20',
                                 'language': 'español/Spanish',
                                 'maxNumberStudents': max_number_students},
                          1262: {'id': 1262,  # 1261, L 18:00, 1271 X 18-20
                                 'teacher': 2,
                                 'groupName': '1262',
                                 'schedule': 'Miércoles/Wednesday 18-20',
                                 'language': 'español/Spanish',
                                 'maxNumberStudents': max_number_students},
                          1263: {'id': 1263,  # 1261, L 18:00, 1271 X 18-20
                                 'teacher': 2,
                                 'groupName': '1263',
                                 'schedule': 'Viernes/Friday 17-19',
                                 'language': 'español/Spanish',
                                 'maxNumberStudents': max_number_students},
                          1271: {'id': 1271,  # 1261, L 18:00, 1271 X 18-20
                                 'teacher': 1,
                                 'groupName': '1271',
                                 'schedule': 'Miércoles/Wednesday 18-20',
                                 'language': 'español/Spanish',
                                 'maxNumberStudents': max_number_students},
                          1272: {'id': 1272,  # 1261, L 18:00, 1271 X 18-20
                                 'teacher': 3,
                                 'groupName': '1272',
                                 'schedule': 'Viernes/Friday 17-19',
                                 'language': 'español/Spanish',
                                 'maxNumberStudents': max_number_students},
                          1291: {'id': 1291,  # 1261, L 18:00, 1271 X 18-20
                                 'teacher': 3,
                                 'groupName': '1291',
                                 'schedule': 'Lunes/Monday 18-20',
                                 'language': 'inglés/English',
                                 'maxNumberStudents': max_number_students},
                          1292: {'id': 1292,
                                 'teacher': 4,
                                 'groupName': '1292',
                                 'schedule': 'Viernes/Friday 17-19',
                                 'language': 'inglés/English',
                                 'maxNumberStudents': max_number_students},
                          1201: {'id': 1201,
                                 'teacher': 5,
                                 'groupName': '1201',
                                 'schedule': 'Miércoles/Wednesday 18-20',
                                 'language': 'español/Spanish',
                                 'maxNumberStudents': max_number_students}}

        for index, lab_group in lab_group_dict.items():
            add_labgroup(lab_group['id'], lab_group['teacher'],
                         lab_group['groupName'], lab_group['language'],
                         lab_group['schedule'], lab_group['maxNumberStudents'])

    def theorygroup(self):
        theory_group_dict = {126: {'id': 126,
                                   'groupName': '126',
                                   'language': 'español/Spanish', },
                             127: {'id': 127,  # 127/120
                                   'groupName': '127',
                                   'language': 'español/Spanish', },
                             129: {'id': 129,  # 129/125
                                   'groupName': '129',
                                   'language': 'inglés/English', },
                             120: {'id': 120,  # 127/120
                                   'groupName': '120',
                                   'language': 'español/Spanish', },
                             125: {'id': 125,  # 129/125
                                   'groupName': '125',
                                   'language': 'inglés/English', }}

        for index, theory_group in theory_group_dict.items():
            add_theorygroup(theory_group['id'], theory_group['groupName'],
                            theory_group['language'])

    def groupconstraints(self):
        """ Follows which laboratory groups (4th column
            may be choosen by which theory groups (2nd column)
            theoryGroup: 126, labGroup: 1261
            theoryGroup: 126, labGroup: 1262
            theoryGroup: 126, labGroup: 1263
            theoryGroup: 127, labGroup: 1271
            theoryGroup: 127, labGroup: 1272
            theoryGroup: 120, labGroup: 1201
            theoryGroup: 129, labGroup: 1291
            theoryGroup: 125, labGroup: 1292"""
        group_constraints_dict = {1261: {'theoryGroup': 126,
                                         'labGroup': 1261},
                                  1262: {'theoryGroup': 126,
                                         'labGroup': 1262},
                                  1263: {'theoryGroup': 126,
                                         'labGroup': 1263},
                                  1271: {'theoryGroup': 127,
                                         'labGroup': 1271},
                                  1272: {'theoryGroup': 127,
                                         'labGroup': 1272},
                                  1201: {'theoryGroup': 120,
                                         'labGroup': 1201},
                                  1291: {'theoryGroup': 129,
                                         'labGroup': 1291},
                                  1292: {'theoryGroup': 125,
                                         'labGroup': 1292}}

        for index, constraint in group_constraints_dict.items():
            add_groupconstraint(constraint['theoryGroup'],
                                constraint['labGroup'])

    def pair(self):
        pair_dict = OrderedDict()
        pair_dict[1000] = {'student2': 1100, 'validated': False}
        pair_dict[1001] = {'student2': 1101, 'validated': False}
        pair_dict[1010] = {'student2': 1110, 'validated': True}
        pair_dict[1011] = {'student2': 1111, 'validated': True}
        pair_dict[1012] = {'student2': 1112, 'validated': True}

        for s1, item in pair_dict.items():
            add_pair(s1, item['student2'], item['validated'])

    def otherconstrains(self):
        start_date = datetime.datetime.now(datetime.timezone.utc) + \
                     datetime.timedelta(days=1)
        theory_grade = 3
        lab_grade = 7

        add_otherconstraint(theory_grade, lab_grade,
                            start_date)

    def student(self, csvStudentFile):
        # read csv file
        # structure NIE	DNI	Apellidos	Nombre	group-Teoría
        with open(csvStudentFile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 1000
            for row in reader:
                add_student(counter, str(row['NIE']), str(row['DNI']),
                            str(row['Apellidos']), str(row['Nombre']),
                            int(row['grupo-teoria']))
                counter += 1

    def studentgrade(self, csvStudentFileGrades):
        with open(csvStudentFileGrades, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                add_studentgrade(str(row['NIE']), row['nota-teoria'].strip(),
                                 row['nota-practicas'].strip())


def add_teacher(identifier, first_name, last_name):
    t = Teacher.objects.get_or_create(id=identifier)[0]
    t.first_name = first_name
    t.last_name = last_name
    t.save()
    return t


def add_labgroup(identifier, teacher, group_name, language, schedule,
                 max_number_students, counter=0):
    teacher_object = Teacher.objects.get(id=teacher)

    lg = LabGroup.objects.get_or_create(id=identifier,
                                        teacher=teacher_object)[0]
    lg.groupName = group_name
    lg.language = language
    lg.schedule = schedule
    lg.maxNumberStudents = max_number_students
    lg.counter = counter
    lg.save()
    return lg


def add_theorygroup(identifier, group_name, language):
    tg = TheoryGroup.objects.get_or_create(id=identifier)[0]
    tg.groupName = group_name
    tg.language = language
    tg.save()
    return tg


def add_groupconstraint(theory_group, lab_group):
    theory_group_object = TheoryGroup.objects.get(id=theory_group)
    lab_group_object = LabGroup.objects.get(id=lab_group)
    c = GroupConstraints.objects.get_or_create(theoryGroup=theory_group_object,
                                               labGroup=lab_group_object)[0]
    c.save()
    return c


def add_student(identifier, nie, dni, last_name, first_name, theory_group_id):
    theory_group_object = TheoryGroup.objects.get(id=theory_group_id)
    s = Student.objects.get_or_create(id=identifier)[0]
    s.username = nie
    s.password = hashers.make_password(dni)
    s.first_name = first_name.strip()
    s.last_name = last_name.strip()
    s.email = first_name.lower() + '.' + last_name.lower().replace(" ", "") + \
              '@estudiante.uam.es '
    s.theoryGroup = theory_group_object
    s.save()
    return s


def add_studentgrade(nie, theory_grade, lab_grade):
    try:
        s = Student.objects.get(username=nie)
    except Student.DoesNotExist:
        return

    s.gradeTheoryLastYear = decimal.Decimal(theory_grade)
    s.gradeLabLastYear = decimal.Decimal(lab_grade)
    s.save()
    return s


def add_pair(student1, student2, validated=False):
    s1_object = Student.objects.get(id=student1)
    s2_object = Student.objects.get(id=student2)
    p = Pair.objects.get_or_create(student1=s1_object, student2=s2_object)[0]
    p.validated = validated
    p.save()
    return p


def add_otherconstraint(theory_grade, lab_grade, start_date):
    c = OtherConstraints.objects.create(minGradeTheoryConv=theory_grade,
                                        minGradeLabConv=lab_grade,
                                        selectGroupStartDate=start_date)
    c.save()
    return c

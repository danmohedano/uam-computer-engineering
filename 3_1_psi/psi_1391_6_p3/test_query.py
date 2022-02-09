import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'labassign.settings')

django.setup()
from core.models import Student, Pair, OtherConstraints


def test():
    student_1000, created = Student.objects.get_or_create(id=1000)
    if created:
        student_1000.username = 'student1000'
        student_1000.email = 'a@a.es'
        student_1000.password = 'student1000'
        student_1000.first_name = 'Felipez'
        student_1000.last_name = 'Nomas'
        student_1000.save()

    student_1001, created = Student.objects.get_or_create(id=1001)
    if created:
        student_1001.username = 'student1001'
        student_1001.email = 'b@b.es'
        student_1001.password = 'student1001'
        student_1001.first_name = 'John'
        student_1001.last_name = 'Doe'
        student_1001.save()

    pair = Pair.objects.create(student1=student_1000, student2=student_1001)
    pair.save()

    for p in Pair.objects.filter(student1=student_1000):
        print(p)
        p.validated = True
        p.save()

    constraint = OtherConstraints.objects.create(selectGroupStartDate=datetime.
                                                 datetime.
                                                 now(datetime.timezone.utc) +
                                                 datetime.timedelta(days=1))

    constraint.save()
    all_constraints = OtherConstraints.objects.all()
    if all_constraints[0].selectGroupStartDate > datetime.datetime.\
            now(datetime.timezone.utc):
        print("SelectGroupStartDate is in the future!")
    else:
        print("SelectGroupStartDate is in the past!")


if __name__ == '__main__':
    test()

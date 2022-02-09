from core.models import Student, Pair, OtherConstraints, LabGroup, \
    GroupConstraints
from django.db.models import Q, F


def fetch_student(user):
    """
    Fetches the student that is logged in but as a Student object, rather than
    a User object.
    :author: Daniel Mohedano
    :param user: the user that is logged in
    :return: the student if exists, None otherwise
    """
    try:
        student = Student.objects.get(username=user.username)
        return student
    except Student.DoesNotExist:
        print("Student doesn't exist")
        return None


def fetch_available_students(student):
    """
    Fetches all available students for the pair selection process
    :author: Silvia Sopeña
    :param student: student requesting the available students
    :return: the list of students
    """
    # Filter out those that are part of a validated pair or have already
    # requested a pair (as student 1) with a student different than the one
    # requesting the list of students

    pair1 = Pair.objects.exclude(student2=student).values('student1')
    pair2 = Pair.objects.filter(validated=True).values('student2')
    students = Student.objects.filter(id__gt=999).exclude(id__in=pair1).\
        exclude(id__in=pair2).exclude(id=student.id)
    return students


def fetch_validated_pair(student):
    """
    Fetches the pair (validated) of which the student given is a part
    :author: Daniel Mohedano
    :param student: the student
    :return: the pair if exists, None otherwise
    """
    pair = Pair.objects.filter(student1=student, validated=True).first()
    if not pair:
        pair = Pair.objects.filter(student2=student, validated=True).first()

    return pair


def fetch_non_validated_pair(student):
    """
    Fetches the pair (not validated) of which the student given is a part and
    only if the student is the student that requested the pair (student 1).
    :author: Silvia Sopeña
    :param student: the student
    :return: the pair if exists, None otherwise
    """
    return Pair.objects.filter(student1=student).first()


def fetch_pairs(student):
    """
    Fetches the pairs to which the student is a part of (in general, no
    conditions applied)
    :author: Daniel Mohedano
    :param student:
    :return: the pairs
    """
    return Pair.objects.filter(Q(student1=student) | Q(student2=student))


def fetch_constraints():
    """
    Fetches the constraints.
    :author: Silvia Sopeña
    :return: the constraints
    """
    return OtherConstraints.objects.all().first()


def fetch_lab_groups(student):
    """
    Fetches the lab groups to which a student can apply.
    :author: Daniel Mohedano
    :param student: the student
    :return: the list of groups
    """
    if student.theoryGroup is None:
        return LabGroup.objects.none()

    # Take the group constraints of the student's theory group
    group_constraints = GroupConstraints.objects.filter(theoryGroup=student.
                                                        theoryGroup).\
        values('labGroup')

    # Extract the non-full lab groups from the constraints
    lab_groups = LabGroup.objects.filter(id__in=group_constraints).\
        exclude(counter__gte=F('maxNumberStudents'))

    return lab_groups

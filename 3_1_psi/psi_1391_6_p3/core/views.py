from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from core.models import Student, Pair, OtherConstraints, GroupConstraints, \
    LabGroup
from django.contrib.auth.decorators import login_required
import datetime


def home(request):
    """
    View used to display the home page
    :author: Silvia Sopeña
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        # If the user is authenticated, display the relevant information
        context_dict = {}
        student = fetch_student(request.user)
        if not student:
            return render(request, 'core/home.html')

        context_dict['name'] = student.first_name + " " + student.last_name
        if student.theoryGroup:
            context_dict['theoryGroup'] = student.theoryGroup

        context_dict['convalidation'] = student.convalidationGranted
        pairs = fetch_pairs(student)
        context_dict['pairs'] = pairs

        if student.labGroup:
            context_dict['labGroup'] = student.labGroup

        return render(request, 'core/home.html', context=context_dict)

    else:
        return render(request, 'core/home.html')


def user_login(request):
    """
    View used to login in the student from the form sent by login.html
    :author: Daniel Mohedano
    :param request:
    :return:
    """
    # Set an auxiliary variable in the context dictionary to tell the html
    # if it needs to print an error message or not.
    # error = 0 -> no error
    # error = 1 -> invalid username or password
    # error = 2 -> account disabled
    context_dict = {'error': 0}
    if request.user.is_authenticated:
        context_dict['error'] = 3
        return render(request, 'core/login.html', context=context_dict)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('core:index'))
        else:
            # If user doesn't exist, display error message
            context_dict['error'] = 1
            return render(request, 'core/login.html', context=context_dict)

    else:
        return render(request, 'core/login.html', context=context_dict)


@login_required
def user_logout(request):
    """
    View used to logout a user
    :author: Silvia Sopeña
    :param request:
    :return:
    """
    logout(request)
    return render(request, 'core/logout.html')


@login_required
def convalidation(request):
    """
    View to handle the convalidation process
    :author: Daniel Mohedano
    :param request:
    :return:
    """
    student = fetch_student(request.user)
    if not student:
        return redirect(reverse('core:index'))

    context_dict = {}
    if student.convalidationGranted is True:
        # Show error if grades are already convalidated
        context_dict['error'] = 5
        return render(request, 'core/convalidation.html', context=context_dict)

    if student.labGroup is not None:
        # Show error if the student already has a laboratory group
        context_dict['error'] = 1
        return render(request, 'core/convalidation.html', context=context_dict)

    if fetch_validated_pair(student) is not None:
        # Show error if the student is part of a validated pair
        context_dict['error'] = 2
        return render(request, 'core/convalidation.html', context=context_dict)

    if fetch_non_validated_pair(student) is not None:
        # Show error if the student is the first member of any pair
        context_dict['error'] = 3
        return render(request, 'core/convalidation.html', context=context_dict)

    grade_lab = student.gradeLabLastYear
    grade_theory = student.gradeTheoryLastYear
    constraint = fetch_constraints()

    if (grade_lab >= constraint.minGradeLabConv) and \
            (grade_theory >= constraint.minGradeTheoryConv):
        context_dict['error'] = 0
        student.convalidationGranted = True
        student.save()
        return render(request, 'core/convalidation.html', context=context_dict)
    else:
        # Show error if the grades are not enough
        context_dict['error'] = 4
        context_dict['lab_grade'] = grade_lab
        context_dict['theory_grade'] = grade_theory
        return render(request, 'core/convalidation.html', context=context_dict)


@login_required
def apply_pair(request):
    """
    View to handle the apply pair process
    :author: Silvia Sopeña
    :param request:
    :return:
    """
    context_dict = {'error': 0}
    student = fetch_student(request.user)
    if not student:
        return redirect(reverse('core:index'))

    if request.method == 'POST':
        if fetch_validated_pair(student) is not None or \
                (fetch_non_validated_pair(student) is not None):
            context_dict['error'] = 3
            return render(request, 'core/applypair.html', context=context_dict)

        s_requested_id = request.POST.get('secondMemberGroup')
        s_requested = Student.objects.get(id=s_requested_id)

        # Check if the student requested had already requested a pair
        # with the logged in student
        pair = fetch_non_validated_pair(s_requested)
        if pair is not None:
            # Just validate the pair
            pair.validated = True
            pair.save()
            if s_requested.labGroup is not None:
                student.labGroup = s_requested.labGroup
                student.save()
                s_requested.labGroup.counter += 1
                s_requested.labGroup.save()
            return redirect(reverse('core:index'))

        # If not, just create the non-validated pair
        pair = Pair.objects.get_or_create(student1=student,
                                          student2=s_requested)[0]
        pair.save()
        return redirect(reverse('core:index'))
    else:
        # Check if the student is already part of a validated pair
        if fetch_validated_pair(student) is not None:
            context_dict['error'] = 1
            return render(request, 'core/applypair.html', context=context_dict)

        # Check if the student has already requested a pair
        if fetch_non_validated_pair(student) is not None:
            context_dict['error'] = 2
            return render(request, 'core/applypair.html', context=context_dict)

        context_dict['students'] = fetch_available_students(student)
        return render(request, 'core/applypair.html', context=context_dict)


@login_required
def break_pair(request):
    """
    View to handle the break pair process
    :author: Daniel Mohedano
    :param request:
    :return:
    """
    context_dict = {'msg': 0}
    student = fetch_student(request.user)
    if not student:
        return redirect(reverse('core:index'))

    if request.method == 'POST':
        # Check if the student is already part of a validated pair
        pair = fetch_validated_pair(student)
        if pair is not None:
            if pair.studentBreakRequest is None:
                # If no student has not requested to break the pair
                pair.studentBreakRequest = student
                pair.save()
                context_dict['msg'] = 2
                if pair.student1 == student:
                    context_dict['student2'] = pair.student2
                else:
                    context_dict['student2'] = pair.student1
                return render(request, 'core/breakpair.html',
                              context=context_dict)
            else:
                # If the other student has already requested to break the pair
                pair.delete()
                context_dict['msg'] = 4
                return render(request, 'core/breakpair.html',
                              context=context_dict)

        # If the student just requested a pair (non-validated)
        pair = fetch_non_validated_pair(student)
        if pair is not None:
            pair.delete()
            context_dict['msg'] = 4
            return render(request, 'core/breakpair.html', context=context_dict)
        else:
            context_dict['msg'] = 1
            return render(request, 'core/breakpair.html', context=context_dict)
    else:
        # Check if the student is already part of a validated pair
        pair = fetch_validated_pair(student)
        if pair is not None:
            if pair.studentBreakRequest == student:
                context_dict['msg'] = 3
                return render(request, 'core/breakpair.html',
                              context=context_dict)

            context_dict['student1'] = pair.student1
            context_dict['student2'] = pair.student2
            return render(request, 'core/breakpair.html', context=context_dict)

        # Check if the student has already requested a pair
        pair = fetch_non_validated_pair(student)
        if pair is not None:
            context_dict['student1'] = pair.student1
            context_dict['student2'] = pair.student2
            return render(request, 'core/breakpair.html', context=context_dict)

        context_dict['msg'] = 1
        return render(request, 'core/breakpair.html', context=context_dict)


@login_required
def apply_group(request):
    """
    View to handle the apply group process
    :author: Silvia Sopeña
    :param request:
    :return:
    """
    context_dict = {'msg': 0}
    student = fetch_student(request.user)
    if not student:
        return redirect(reverse('core:index'))

    if request.method == 'POST':
        # Check the date in the constraints
        if OtherConstraints.objects.all().first().selectGroupStartDate > \
                (datetime.datetime.now(datetime.timezone.utc)):
            context_dict['msg'] = 2
            return render(request, 'core/applygroup.html',
                          context=context_dict)

        g_id = request.POST.get('myLabGroup')
        g = LabGroup.objects.get(id=g_id)
        if g not in fetch_lab_groups(student):
            context_dict['msg'] = 3
            return render(request, 'core/applygroup.html',
                          context=context_dict)
        # Add the student to the group
        student.labGroup = g
        student.save()
        g.counter += 1
        g.save()
        # If part of a validated pair, add the other student to the group
        pair = fetch_validated_pair(student)
        if pair is not None:
            if pair.student1 == student:
                pair.student2.labGroup = g
                pair.student2.save()
            else:
                pair.student1.labGroup = g
                pair.student1.save()

            g.counter += 1
            g.save()

        return redirect(reverse('core:applygroup'))
    else:
        # Check the date in the constraints
        if OtherConstraints.objects.all().first().selectGroupStartDate > \
                (datetime.datetime.now(datetime.timezone.utc)):
            context_dict['msg'] = 2
            return render(request, 'core/applygroup.html',
                          context=context_dict)
        # Check if the student is already part of a group
        if student.labGroup is not None:
            context_dict['msg'] = 1
            context_dict['labGroup'] = student.labGroup.groupName
            return render(request, 'core/applygroup.html',
                          context=context_dict)

        context_dict['groups'] = fetch_lab_groups(student)
        return render(request, 'core/applygroup.html', context=context_dict)


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
    # Get all real students (without alumnodb)
    students = Student.objects.filter(id__gt=999)
    # Filter out those that are part of a validated pair or have already
    # requested a pair (as student 1) with a student different than the one
    # requesting the list of students
    students_filtered = [s for s
                         in students
                         if (fetch_validated_pair(s) is None) and
                         (fetch_non_validated_pair(s) is None or
                          (fetch_non_validated_pair(s) is not None and
                           fetch_non_validated_pair(
                               s).student2 == student)) and
                         (s != student)]
    return students_filtered


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
    pairs = []
    new_pairs = Pair.objects.filter(student1=student)
    if new_pairs:
        for p in new_pairs:
            pairs.append(p)

    new_pairs = Pair.objects.filter(student2=student)
    if new_pairs:
        for p in new_pairs:
            pairs.append(p)

    return pairs


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
        return None

    # Take the group constraints of the student's theory group
    group_constraints = GroupConstraints.objects.filter(theoryGroup=student.
                                                        theoryGroup)

    # Extract the non-full lab groups from the constraints
    if fetch_validated_pair(student) is not None:
        lab_groups = [c.labGroup for c
                      in group_constraints
                      if c.labGroup.maxNumberStudents >
                      (c.labGroup.counter + 1)]
    else:
        lab_groups = [c.labGroup for c
                      in group_constraints
                      if c.labGroup.maxNumberStudents > c.labGroup.counter]

    return lab_groups

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from core.models import Pair, OtherConstraints
from django.contrib.auth.decorators import login_required
import datetime
from core.auxiliary import fetch_student, fetch_pairs, fetch_validated_pair, \
    fetch_non_validated_pair, fetch_constraints
from core.forms import LoginForm, ApplyPairForm, BreakPairForm, ApplyGroupForm


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
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect(reverse('core:index'))
            else:
                # If user doesn't exist, display error message
                context_dict['error'] = 1
                return render(request, 'core/login.html', context=context_dict)
        else:
            context_dict['error'] = 2
            return render(request, 'core/login.html', context=context_dict)

    else:
        context_dict['form'] = LoginForm()
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

        form = ApplyPairForm(student=student, data=request.POST)
        if not form.is_valid():
            context_dict['error'] = 4
            return render(request, 'core/applypair.html', context=context_dict)

        s_requested = form.cleaned_data.get('student')
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

        context_dict['form'] = ApplyPairForm(student=student)
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
        form = BreakPairForm(student=student, data=request.POST)
        if not form.is_valid():
            context_dict['msg'] = 3
            return render(request, 'core/breakpair.html', context=context_dict)

        pair = form.cleaned_data.get('pair')

        # Check if the pair is not validated
        if not pair.validated:
            # If the pair is not validated, it is deleted
            context_dict['s1'] = pair.student1
            context_dict['s2'] = pair.student2
            pair.delete()
            context_dict['msg'] = 1
            return render(request, 'core/breakpair.html', context=context_dict)
        else:
            if pair.studentBreakRequest is None:
                # If no one has requested to break the pair, update the field
                pair.studentBreakRequest = student
                pair.save()
                context_dict['msg'] = 2
                return render(request, 'core/breakpair.html',
                              context=context_dict)
            else:
                # If the student had already requested the break, do nothing
                if pair.studentBreakRequest == student:
                    context_dict['msg'] = 2
                    return render(request, 'core/breakpair.html',
                                  context=context_dict)
                else:
                    # The second student requests it, the pair is deleted
                    context_dict['s1'] = pair.student1
                    context_dict['s2'] = pair.student2
                    pair.delete()
                    context_dict['msg'] = 1
                    return render(request, 'core/breakpair.html',
                                  context=context_dict)
    else:
        context_dict['form'] = BreakPairForm(student=student)

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

        form = ApplyGroupForm(student=student, data=request.POST)
        if not form.is_valid():
            context_dict['msg'] = 4
            return render(request, 'core/applygroup.html',
                          context=context_dict)

        g = form.cleaned_data.get('group')

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

        context_dict['form'] = ApplyGroupForm(student=student)
        return render(request, 'core/applygroup.html', context=context_dict)

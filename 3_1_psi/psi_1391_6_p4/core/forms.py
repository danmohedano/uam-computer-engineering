from django import forms
from core.models import Student, Pair, LabGroup
from core.auxiliary import fetch_available_students, fetch_pairs, \
    fetch_lab_groups


class LoginForm(forms.Form):
    """
    Form to allow the user to login.
    :author: Daniel Mohedano
    """
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class ApplyPairForm(forms.Form):
    """
    Form to allow the user apply a pair.
    :author: Silvia Sopeña
    """
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    def __init__(self, student, *args, **kwargs):
        super(ApplyPairForm, self).__init__(*args, **kwargs)
        studentList = fetch_available_students(student)
        self.fields['student'].queryset = Student.objects.\
            filter(id__in=studentList)


class BreakPairForm(forms.Form):
    """
    Form to allow the user to break a pair.
    :author: Daniel Mohedano
    """

    pair = forms.ModelChoiceField(queryset=Pair.objects.all())

    def __init__(self, student, *args, **kwargs):
        super(BreakPairForm, self).__init__(*args, **kwargs)
        base_pairs = fetch_pairs(student)
        students_with_group = Student.objects.exclude(labGroup__isnull=True)
        self.fields['pair'].queryset = base_pairs.\
            exclude(student1__in=students_with_group).\
            exclude(student2__in=students_with_group)


class ApplyGroupForm(forms.Form):
    """
    Form to allow the user to apply group.
    :author: Silvia Sopeña
    """

    group = forms.ModelChoiceField(queryset=LabGroup.objects.all())

    def __init__(self, student, *args, **kwargs):
        super(ApplyGroupForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = fetch_lab_groups(student)

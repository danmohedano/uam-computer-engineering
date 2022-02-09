import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import (Student, OtherConstraints,
                         Pair, TheoryGroup, GroupConstraints,
                         LabGroup)
from core.management.commands.populate import Command
import re

USER_SESSION_ID = "_auth_user_id"

LOGIN_SERVICE = "core:login"
LOGOUT_SERVICE = "core:logout"
LOGIN_TITLE = "Login"

LANDING_TITLE = r"Home"  # redirect here after login
LANDING_PAGE = "core:home"

CONVALIDATION_SERVICE = 'core:convalidation'
CONVALIDATION_TITLE = 'Convalidation'

PAIR_SERVICE = "core:applypair"
PAIR_TITLE = 'Apply Pair'
PAIR_SAME_USER = 'You have already selected a pair'
PAIR_FORM_LABEL = 'student'
PAIR_SELECTION_ERROR = 'Could not process your request'
BREAK_SERVICE = "core:breakpair"
BREAK_TITLE = 'Break Pair'
BREAK_FORM_LABEL = 'pair'

GROUP_SERVICE = "core:applygroup"
GROUP_TITLE = 'Apply Group'
GROUP_FORM_LABEL = 'group'
GROUP_ERROR_NOT_VALID = 'Members of the theory group'

SERVICE_DEF = {LOGIN_SERVICE: {
    "title": LOGIN_TITLE,
    "pattern": r"Please login|Por favor autentiquese",
    "patternfail": r"You are already logged in"
},
    LANDING_PAGE: {
        "title": LANDING_TITLE,
        # search pattern "Hi <b> plus any string composed by [a-zA-Z0-9_]
        "pattern": r"This is your summary page, <b>(?P<username>\w+)",
        "patternfail": r"Hi!"
    },
    CONVALIDATION_SERVICE: {
        "title": CONVALIDATION_TITLE,
        "patternfail": r"do not satisfy",
        "pattern": r"Congratulations"
    },
    PAIR_SERVICE: {
        "title": PAIR_TITLE,
        "pattern": r"select the second"
    },
    BREAK_SERVICE: {
        "title": BREAK_TITLE,
        "pattern": r"Select the pair to be"
    },
    GROUP_SERVICE: {
        "title": GROUP_TITLE,
        "patternfail": r"Group selection is not active",
        "pattern": r"Select the group you want to join to"
    },
}


class BaseTest(TestCase):
    def setUp(self):
        self.params_user_non_student = {'username': 'NonStudent',
                                        'password': 'Password',
                                        'id': 50}

        self.params_user1 = {"username": 'user1',
                             "password": 'password1',
                             "first_name": 'first_name1',
                             "last_name": 'last_name1',
                             "id": 1000}

        self.params_user_non_exist = {"username": 'asdfasdf',
                                      "password": 'pasasdfasdsword1',
                                      "first_name": 'asdfasdf',
                                      "last_name": 'lastasdfa_name1',
                                      "id": 1500}
        self.params_user_long = {"username": 'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf'
                                             'asdfasdfasdfasdfasdf',
                                 "password": 'pasasdfasdsword1',
                                 "first_name": 'asdfasdf',
                                 "last_name": 'lastasdfa_name1',
                                 "id": 9999}

        self.params_user2 = {"username": 'gasd',
                             "password": 'asdfafwe',
                             "first_name": 'feadfa',
                             "last_name": 'asefasdfa',
                             "id": 1644}

        self.params_user3 = {"username": 'asdfa',
                             "password": 'gfdgr',
                             "first_name": 'sdgfjs',
                             "last_name": 'sdfgrs',
                             "id": 1647}

        self.user_non_student = User.objects.create_user(
            id=self.params_user_non_student['id'],
            username=self.params_user_non_student['username'],
            password=self.params_user_non_student['password'])

        self.user1 = Student.objects.create_user(
            id=self.params_user1["id"],
            username=self.params_user1["username"],
            password=self.params_user1["password"],
            first_name=self.params_user1["first_name"],
            last_name=self.params_user1["last_name"])

        self.user2 = Student.objects.create_user(
            id=self.params_user2["id"],
            username=self.params_user2["username"],
            password=self.params_user2["password"],
            first_name=self.params_user2["first_name"],
            last_name=self.params_user2["last_name"],
            convalidationGranted=True)

        self.user3 = Student.objects.create_user(
            id=self.params_user3["id"],
            username=self.params_user3["username"],
            password=self.params_user3["password"],
            first_name=self.params_user3["first_name"],
            last_name=self.params_user3["last_name"])

        self.client1 = self.client
        self.client2 = Client()
        self.client3 = Client()
        self.populate = Command()
        self.populate.teacher()
        self.populate.otherconstrains()
        self.populate.theorygroup()
        self.populate.labgroup()
        self.populate.groupconstraints()

        self.user1.theoryGroup = TheoryGroup.objects.all().first()
        self.user1.labGroup = LabGroup.objects.all().first()
        self.user1.save()

    def tearDown(self):
        self.populate.cleanDataBase()

    @classmethod
    def loginTestUser(cls, client, user):
        client.force_login(user)

    @classmethod
    def logoutTestUser(cls, client):
        client.logout()

    @classmethod
    def decode(cls, txt):
        return txt.decode("utf-8")

    def validate_login_required(self, client, service):
        self.logoutTestUser(client)
        response = client.get(reverse(service), follow=True)
        self.assertEqual(response.status_code, 200)
        self.is_login(response)

    def validate_response(self, service, response, fail=False, pattern=None):
        definition = SERVICE_DEF[service]
        self.assertRegex(self.decode(response.content), definition["title"])
        if pattern:
            m = re.search(pattern, self.decode(response.content))
        elif fail:
            # print(definition["patternfail"], self.decode(response.content))
            m = re.search(definition["patternfail"],
                          self.decode(response.content))
        else:
            # print(definition["pattern"], self.decode(response.content))
            m = re.search(definition["pattern"], self.decode(response.content))
        self.assertTrue(m)
        return m

    def is_login(self, response, fail=False):
        self.validate_response(LOGIN_SERVICE, response, fail)

    def is_request_pair(self, response):
        self.validate_response(PAIR_SERVICE, response)

    def is_convalidated(self, response, fail=False):
        self.validate_response(CONVALIDATION_SERVICE, response, fail)

    def is_landing_not_authenticated(self, response):
        self.validate_response(LANDING_PAGE, response, True)

    def is_landing_autenticated(self, response, user):
        m = self.validate_response(LANDING_PAGE, response)
        self.assertEqual(m.group("username"), user.first_name)

    def is_group(self, response, fail=False):
        self.validate_response(GROUP_SERVICE, response, fail)


class HomeTests(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_log_in_non_student(self):
        """
        Test that the home page displays correctly when logged in with a
        user that isn't a student
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE), self.params_user_non_student,
                          follow=True)
        response = self.client1.get(reverse(LANDING_PAGE), follow=True)
        self.is_landing_not_authenticated(response)

    def test02_log_in_student_groups(self):
        """
        Test that the home page displays correctly when logged in with a
        student with groups
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE), self.params_user1,
                          follow=True)
        response = self.client1.get(reverse(LANDING_PAGE), follow=True)
        self.is_landing_autenticated(response, self.user1)

    def test03_no_login(self):
        """
        Test landing page without login
        :return:
        """
        response = self.client1.get(reverse(LANDING_PAGE), follow=True)
        self.is_landing_not_authenticated(response)


class LoginTests(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_already_logged(self):
        """
        Test login page when already logged in
        :return:
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE), self.params_user1,
                          follow=True)
        response = self.client1.get(reverse(LOGIN_SERVICE), follow=True)
        self.is_login(response, True)

    def test02_non_existent_user(self):
        """
        Login incorrectly
        :return:
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.params_user_non_exist,
                                     follow=True)
        self.validate_response(LOGIN_SERVICE, response,
                               pattern=r"your username and password didn't "
                                       r"match")

    def test_03_invalid_form(self):
        """
        Login with a username too long
        :return:
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.params_user_long,
                                     follow=True)
        self.validate_response(LOGIN_SERVICE, response,
                               pattern=r"Invalid form")


class ConvalidationTests(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_display_non_student(self):
        """
        Test that the home page is displayed if the user is not a student
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.params_user_non_student,
                                     follow=True)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        self.is_landing_not_authenticated(response)

    def test02_display_convalidation_granted(self):
        """
        Test that an error message is displayed if the student has already
        convalidated the grades
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user2,
                          follow=True)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        self.validate_response(CONVALIDATION_SERVICE, response,
                               pattern=r"Your grades are already convalidated")

    def test03_display_labgroup(self):
        """
        Test that an error message is displayed if the student has already
        a lab group
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user1,
                          follow=True)
        response = self.client1.get(reverse(CONVALIDATION_SERVICE),
                                    follow=True)
        self.validate_response(CONVALIDATION_SERVICE, response,
                               pattern=r"You are already part of a "
                                       r"laboratory group")


class PairTests(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_display_non_student(self):
        """
        Test that the home page is displayed if the user is not a student
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.params_user_non_student,
                                     follow=True)
        response = self.client1.get(reverse(PAIR_SERVICE), follow=True)
        self.is_landing_not_authenticated(response)

    def test02_pair_with_student_labgroup(self):
        """
        Validate a pair with a student that already has a labgroup
        :return:
        """
        pair = Pair.objects.create(student1=self.user1, student2=self.user3)
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # login with student 3
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user3,
                          follow=True)
        data = {PAIR_FORM_LABEL: self.user1.id}
        # request pair
        response = self.client1.post(reverse(PAIR_SERVICE),
                                     data=data,
                                     follow=True)

        self.is_landing_autenticated(response, self.user3)
        pair.delete()

    def test03_already_convalidated_pair(self):
        """
        Test that an error message is displayed if the student is already part
        of a validated pair
        :return:
        """
        pair = Pair.objects.create(student1=self.user1, student2=self.user3,
                                   validated=True)
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # login with student 1
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user1,
                          follow=True)
        response = self.client1.get(reverse(PAIR_SERVICE),
                                    follow=True)
        self.validate_response(CONVALIDATION_SERVICE, response,
                               pattern=r"You are already part of a validated "
                                       r"pair")
        pair.delete()

    def test04_already_requested_pair(self):
        """
        Test that an error message is displayed if the student has already
        requested a pair
        :return:
        """
        pair = Pair.objects.create(student1=self.user1, student2=self.user3)
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # login with student 1
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user1,
                          follow=True)
        response = self.client1.get(reverse(PAIR_SERVICE),
                                    follow=True)
        self.validate_response(CONVALIDATION_SERVICE, response,
                               pattern=r"You have already requested a pair")
        pair.delete()

    def test05_non_existent_student(self):
        """
        Test that an error message is displayed if the form is not used
        correctly
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # login with student 3
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user3,
                          follow=True)
        data = {PAIR_FORM_LABEL: 99999}
        # request pair
        response = self.client1.post(reverse(PAIR_SERVICE),
                                     data=data,
                                     follow=True)
        self.validate_response(PAIR_SERVICE, response, pattern=r"Invalid form")


class GroupTests(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_display_non_student(self):
        """
        Test that the home page is displayed if the user is not a student
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.params_user_non_student,
                                     follow=True)
        response = self.client1.get(reverse(GROUP_SERVICE), follow=True)
        self.is_landing_not_authenticated(response)

    def test02_post_before_time(self):
        """ Test page for group selection before deadline
         Note that use must be informed if selection is not active """
        # login
        self.loginTestUser(self.client1, self.user3)
        # set othercostraint.selectGroupStart to now plus 1 day
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now + datetime.timedelta(1)
        o.save()
        # connect to create group page
        response = self.client1.post(reverse(GROUP_SERVICE), follow=True)
        self.is_group(response, fail=True)

    def test03_apply_with_validate_pair(self):
        """
        Test that it works correctly if requesting a group while being part
        of a validated pair
        :return:
        """
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now
        o.save()
        pair = Pair.objects.create(student1=self.user3, student2=self.user1,
                                   validated=True)
        self.loginTestUser(self.client1, self.user3)
        c = GroupConstraints.objects.all().first()
        self.user3.theoryGroup = c.theoryGroup
        self.user3.labGroup = None
        self.user3.save()
        data = {GROUP_FORM_LABEL: c.labGroup.id}
        response = self.client1.post(reverse(GROUP_SERVICE),
                                     data=data,
                                     follow=True)
        self.validate_response(GROUP_SERVICE, response,
                               pattern=r"ou are already part of group")
        pair.delete()

    def test04_display_no_theory(self):
        o = OtherConstraints.objects.all().first()
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        o.selectGroupStartDate = now
        o.save()
        self.loginTestUser(self.client1, self.user3)
        self.user3.theoryGroup = None
        self.user3.save()
        response = self.client1.get(reverse(GROUP_SERVICE), follow=True)
        self.is_group(response)


class BreakPairTests(BaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test01_display_non_student(self):
        """
        Test that the home page is displayed if the user is not a student
        """
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        response = self.client1.post(reverse(LOGIN_SERVICE),
                                     self.params_user_non_student,
                                     follow=True)
        response = self.client1.get(reverse(BREAK_SERVICE),
                                    follow=True)
        self.is_landing_not_authenticated(response)

    def test02_display_not_part_of_pair(self):
        """
        Test that an error message is displayed if the student is not part of
        the pair they are requesting to break
        """
        pair = Pair.objects.create(student1=self.user2, student2=self.user3)
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user1,
                          follow=True)
        data = {BREAK_FORM_LABEL: pair.id}
        response = self.client1.post(reverse(BREAK_SERVICE),
                                     data=data,
                                     follow=True)
        self.validate_response(BREAK_SERVICE, response,
                               pattern=r"Could not process your request.")
        pair.delete()

    def test03_display_student_with_lab_group(self):
        """
        Test that an error message is displayed if the student requests to
        break a pair in which some student already has a labgroup
        """
        pair = Pair.objects.create(student1=self.user1, student2=self.user2)
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user1,
                          follow=True)
        data = {BREAK_FORM_LABEL: pair.id}
        response = self.client1.post(reverse(BREAK_SERVICE),
                                     data=data,
                                     follow=True)
        self.validate_response(BREAK_SERVICE, response,
                               pattern=r"Could not process your request.")
        pair.delete()

    def test04_student_break_more_than_once(self):
        """
        Test that there is no error if the student tries to break again
        the pair
        """
        pair = Pair.objects.create(student1=self.user2, student2=self.user3,
                                   validated=True)
        # no student logged in
        self.assertFalse(self.client1.session.get(USER_SESSION_ID, False))
        # log in
        self.client1.post(reverse(LOGIN_SERVICE),
                          self.params_user2,
                          follow=True)
        data = {BREAK_FORM_LABEL: pair.id}
        response = self.client1.post(reverse(BREAK_SERVICE),
                                     data=data,
                                     follow=True)
        self.validate_response(BREAK_SERVICE, response,
                               pattern=r"Pair has not been deleted")
        response = self.client1.post(reverse(BREAK_SERVICE),
                                     data=data,
                                     follow=True)
        self.validate_response(BREAK_SERVICE, response,
                               pattern=r"Pair has not been deleted")
        pair.delete()

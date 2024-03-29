"""
Models for app dashboard
"""
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.utils import timezone
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse


class UserManager(BaseUserManager):
    """
    Model for managing users
    """
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password and name.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a mentor(staff) user with the
        given email and password and name.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a course admin(superuser)
        with the given email and password and name.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Class for users (Mentors and Course admins)
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField('Course Administrator', default=False)
    admin = models.BooleanField('Superadmin', default=False)
    name = models.CharField('Name', max_length=80, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Username is set to email
    REQUIRED_FIELDS = []  # Email and Password are required fields

    def get_full_name(self):
        """
        User is identified by email
        """
        return self.email

    def get_short_name(self):
        """
        The user is identified by their email address
        """
        return self.email

    def __str__(self):
        """
        Return email as string
        """
        return str(self.name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

# Dashboard classes


class StudentMentorCard(models.Model):
    """
    Model representing a card that
    contains the mentor and
    the student paired.
    """
    # Foreign Key used because StudentMentorCard can only have one student.
    student = models.ForeignKey(
        'Student', on_delete=models.SET_NULL, null=True
        )
    student_email = models.CharField(
        'Student email',
        max_length=200,
        blank=True
        )
    summary = models.TextField(
        max_length=2000,
        help_text='Enter a summary of Student '
        'overall progress from Mentor perspective.',
        blank=True
        )
    student_github = models.URLField(
        'Student GitHub',
        max_length=200,
        blank=True
        )
    slack_name = models.CharField('Slack name', max_length=200, blank=True)
    student_linkedin = models.URLField(
        'Student linkedin',
        max_length=200,
        blank=True
        )
    # List of mentors that can be connected to the student.
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
        )

    def __str__(self):
        """
        String for representing the Model object.
        """
        return str(self.student)

    def get_absolute_url(self):
        """
        Returns the URL to access a detail record for this student card.
        """
        return reverse('student-mentor-card', args=[str(self.id)])


class MentorNotes(models.Model):
    """
    Allows the mentor to create short notes
    connected to the student
    """
    student_card = models.ForeignKey(
        'StudentMentorCard', on_delete=models.SET_NULL, null=True
        )

    mentor_note = models.TextField(
        max_length=500,
        help_text='A note on a Student',
        blank=True
        )

    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        """
        Meta fields
        """
        ordering = ['created_date']

    def __str__(self):
        """
        String that represents the model object
        """
        return str(self.mentor_note)

    def get_absolute_url(self):
        """
        Returns the URL to access a detailed note
        """
        return reverse('mentor-notes', args=[str(self.id)])


class StudentSession(models.Model):
    """
    Model representing a specific
    session between the mentor and the
    student
    """
    StudentMentorCard = models.ForeignKey(
        'StudentMentorCard',
        on_delete=models.RESTRICT,
        null=True, blank=False
        )
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=False
        )
    summary = models.TextField(
        max_length=2000,
        help_text='Enter a summary of session with student',
        blank=False
        )
    session_date = models.DateField('Session date', null=True, blank=False)
    project_link = models.URLField('Projent URL', max_length=200, blank=True)
    project_repo = models.URLField(
        'Project repository',
        max_length=200,
        blank=True
        )

    TIME_OF_SESSION = (
        (15, '15 minutes'),
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '60 minutes'),
    )

    time_spent = models.IntegerField(
        'Length of session',
        choices=TIME_OF_SESSION,
        blank=False,
        default=15,
        help_text='Lenght of session'
    )

    MEETING_TYPE = (
        ('i', 'Introduction'),
        ('1', 'Milestone Proj. 1'),
        ('2', 'Milestone Proj. 2'),
        ('3', 'Milestone Proj. 3'),
        ('4', 'Milestone Proj. 4'),
        ('5', 'Milestone Proj. 5'),
    )

    type = models.CharField(
        'Type of session',
        max_length=1,
        choices=MEETING_TYPE,
        blank=False,
        default='i',
        help_text='Type of session',
    )
    MEETING_SUBJECT = (
        ('1', 'Milestone meeting 1'),
        ('2', 'Milestone meeting 2'),
        ('3', 'Milestone meeting 3'),
    )

    subject = models.CharField(
        'Type of subject',
        max_length=1,
        choices=MEETING_SUBJECT,
        blank=False,
        default='1',
        help_text='Type of subject',
    )

    class Meta:
        """
        Meta fields
        """
        ordering = ['session_date']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.StudentMentorCard}'

    def get_absolute_url(self):
        """
        Returns the URL to access a session.
        """
        return reverse('student-session', args=[str(self.id)])


class Student(models.Model):
    """
    Model for student details
    """
    name = models.CharField(max_length=100)
    date_program_start = models.DateField(
        'Program start date',
        null=True,
        blank=True
        )
    date_program_end = models.DateField(
        'Program end date',
        null=True,
        blank=True
        )

    class Meta:
        """
        Meta fields
        """
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the URL to access a particular student.
        """
        return reverse('student-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.name}'

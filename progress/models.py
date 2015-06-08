from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,
        email,
        date_of_birth,
        society,
        first_name,
        last_name,
        position,
        gender,
        role,
        contact_number,
        nominated_on,
        nominated_through,
        password
    ):
        """
        Creates a new user
        """

        if not email:
            raise ValueError('User must have a valid email address')

        s = Society.objects.get(pk=society)

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            society=s,
            first_name=first_name,
            last_name=last_name,
            position=position,
            gender=gender,
            role=role,
            contact_number=contact_number,
            nominated_on=nominated_on,
            nominated_through=nominated_through
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        date_of_birth,
        society,
        first_name,
        last_name,
        position,
        gender,
        role,
        contact_number,
        nominated_on,
        nominated_through,
        password
    ):
        """
        Creates a new superuser
        """


        user = self.create_user(
            email=email,
            date_of_birth=date_of_birth,
            society=society,
            first_name=first_name,
            last_name=last_name,
            position=position,
            gender=gender,
            role=role,
            contact_number=contact_number,
            nominated_on=nominated_on,
            nominated_through=nominated_through,
            password=password,
        )

        user.is_staff = True
        user.save(using=self._db)
        return user

class Society(models.Model):
    name = models.CharField(max_length=100)
    contact_firstname = models.CharField(max_length=30)
    contact_lastname = models.CharField(max_length=30)
    contact_position = models.CharField(max_length=100)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    ROLE = (
        ('observer', 'Observer'),
        ('member', 'Member'),
    )

    society = models.ForeignKey(Society)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=20, choices=ROLE)
    contact_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Contact number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact_number = models.CharField(validators=[contact_regex], max_length=15)
    nominated_on = models.DateField()
    nominated_through = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'date_of_birth',
        'society',
        'first_name',
        'last_name',
        'position',
        'gender',
        'role',
        'contact_number',
        'nominated_on',
        'nominated_through',
    ]

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

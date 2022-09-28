from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='ایمیل',
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    username = models.CharField(max_length=100, verbose_name="نام کاربری",unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن",unique=True)
    image = models.FileField(upload_to="user/image", default="defult/index.jpg", blank=True, null=True,
                             verbose_name="تصویر پروفایل")
    is_teacher = models.BooleanField(default=False, verbose_name="مدرس هست یا خیر؟")
    is_active = models.BooleanField(default=True, verbose_name="کاربر فعال هست یا خیر؟")
    is_admin = models.BooleanField(default=False, verbose_name="کاربر ادمین هست یا خیر؟")
    full_name = models.CharField(max_length=50,null=True,blank=True, verbose_name="نام و نام خانوادگی")
    special_user = models.DateTimeField(default=timezone.now(), verbose_name="کاربر خاص تا زمان:")

    class Meta:
        verbose_name_plural = "حساب های کاربری"
        verbose_name = "حساب کاربری"

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number

    def is_specialuser(self):
        if self.special_user > timezone.now():
            return True
        return False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

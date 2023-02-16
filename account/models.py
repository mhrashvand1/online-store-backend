from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models
from common.models import UUIDBaseModel, BaseModel
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin, UUIDBaseModel):
    
    username = None
    email = None

    phone_number = PhoneNumberField(
        _("phone_number"),
        unique=True,
        db_index=True,   
    )   
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self) -> str:
        return str(self.phone_number)
    
    
class Address(BaseModel):
    user = models.OneToOneField(
        to='account.User', 
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='address',
        verbose_name=_('user')
    )
    state = models.CharField(_("state"), max_length=150, blank=True)
    city = models.CharField(_("city"), max_length=150, blank=True)
    full_address = models.CharField(_("full address"), max_length=1200, blank=True)
    
    class Meta:
        db_table = 'Address'
        verbose_name = _('address')
        verbose_name_plural = _('address')
          
    
class Location(BaseModel):
    user = models.OneToOneField(
        to='account.User', 
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='location',
        verbose_name=_('user')
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True, 
        verbose_name=_("latitude")
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True, 
        verbose_name=_("longitude")
    )
    
    class Meta:
        db_table = 'Location'
        verbose_name = _('location')
        verbose_name_plural = _('location')
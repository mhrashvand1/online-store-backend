from common.models import UUIDBaseModel
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

User = get_user_model()

class Wallet(UUIDBaseModel):
    user = models.OneToOneField(
        to=User, 
        db_index=True,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name=_('user')
    )
    balance = models.PositiveBigIntegerField(
        verbose_name=_('balance')
    )

    def __str__(self):
        return f"user: {self.user.phone_number}', wallet ({self.balance})"
    
    class Meta:
        db_table = 'Wallet'
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')


class Payment(UUIDBaseModel):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        db_index=True,
        related_name='payments',
        verbose_name=_('user')
    )
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'))
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES,
        default='success', 
        verbose_name=_('status')
    )
    error_code = models.CharField(max_length=10, blank=True, verbose_name=_('error_code'))
    error_message = models.CharField(max_length=255, blank=True, verbose_name=_('error_message'))

    def __str__(self):
        return f"user {self.user.phone_number} paid {self.amount} on {self.created_at} ({self.status})"


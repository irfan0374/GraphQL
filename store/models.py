from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, verbose_name=_("email address"))
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()


    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'User_models'


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        validators=[MinValueValidator(0)],
        default=0
    )
    currency = models.CharField(max_length=3)  
    
    def __str__(self):
        return f"{self.account_number} - {self.bank_name}"
    
    class Meta:
        db_table = 'user_accounts'


class Transaction(models.Model):
    TRANSACTION_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='sent_transactions'
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='received_transactions'
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_account} → {self.to_account}: {self.amount} {self.currency}"

    class Meta:
        db_table = 'account_transactions'
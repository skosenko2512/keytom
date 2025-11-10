"""All ORM models in single app."""
from __future__ import annotations
import uuid
from decimal import Decimal
from django.db import models
class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    keycloak_user_id = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "users_userprofile"
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=10, unique=True)
    owner_kc_id = models.CharField(max_length=64, db_index=True)
    currency = models.CharField(max_length=3, default="EUR")
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                          default=Decimal("2.50"))
    amount = models.DecimalField(max_digits=18, decimal_places=2,
                                 default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "acc_account"
class Transaction(models.Model):
    CREDIT = "CREDIT"; DEBIT = "DEBIT"
    TYPES = [(CREDIT,"CREDIT"),(DEBIT,"DEBIT")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                related_name="transactions")
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    type = models.CharField(max_length=6, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "acc_transaction"
        indexes = [models.Index(fields=["created_at"])]

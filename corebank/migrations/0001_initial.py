from django.db import migrations, models
import uuid
from decimal import Decimal
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('keycloak_user_id', models.CharField(max_length=64,
                                                      unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'users_userprofile'},
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        editable=False)),
                ('account_number', models.CharField(max_length=10, unique=True)),
                ('owner_kc_id', models.CharField(max_length=64, db_index=True)),
                ('currency', models.CharField(max_length=3, default='EUR')),
                ('commission_rate', models.DecimalField(max_digits=5,
                                                        decimal_places=2,
                                                        default=Decimal('2.50'))),
                ('amount', models.DecimalField(max_digits=18,
                                               decimal_places=2,
                                               default=Decimal('0.00'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'acc_account'},
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        editable=False)),
                ('amount', models.DecimalField(max_digits=18,
                                               decimal_places=2)),
                ('type', models.CharField(max_length=6,
                                          choices=[('CREDIT','CREDIT'),
                                                   ('DEBIT','DEBIT')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(
                    to='corebank.account',
                    on_delete=models.deletion.CASCADE,
                    related_name='transactions',
                )),
            ],
            options={'db_table': 'acc_transaction'},
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['created_at'], name='acc_txn_date'),
        ),
    ]

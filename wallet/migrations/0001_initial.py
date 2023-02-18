# Generated by Django 4.1.6 on 2023-02-18 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('balance', models.PositiveBigIntegerField(verbose_name='balance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'wallet',
                'verbose_name_plural': 'wallets',
                'db_table': 'Wallet',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('amount', models.PositiveBigIntegerField(verbose_name='amount')),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], default='success', max_length=10, verbose_name='status')),
                ('error_code', models.CharField(blank=True, max_length=10, verbose_name='error_code')),
                ('error_message', models.CharField(blank=True, max_length=255, verbose_name='error_message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

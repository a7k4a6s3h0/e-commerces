# Generated by Django 4.1 on 2023-11-09 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_user_referal_id_user_wallet_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OTP_digit', models.BigIntegerField(unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expiry_time', models.DateTimeField()),
                ('is_verified', models.BooleanField(default=False)),
                ('request_times', models.IntegerField(default=3)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reverse_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.2.23 on 2025-07-11 03:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8449a7f6-1079-4a66-a0a8-ee9b6036b76a'), primary_key=True, serialize=False, unique=True),
        ),
    ]

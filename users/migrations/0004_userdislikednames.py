# Generated by Django 3.2 on 2021-05-09 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_userlikednames'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDislikedNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_disliked_names', to='users.babynames')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_disliked_names', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.2 on 2021-05-07 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='likednames',
            name='matched',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='likednames',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usercouples',
            name='user_two',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='couple_user_two', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='gender',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='origin',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

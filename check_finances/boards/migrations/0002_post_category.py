# Generated by Django 4.1.4 on 2023-01-17 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null='none', on_delete=django.db.models.deletion.CASCADE, to='boards.category'),
            preserve_default='none',
        ),
    ]

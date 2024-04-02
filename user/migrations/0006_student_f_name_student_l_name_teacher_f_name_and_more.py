# Generated by Django 5.0 on 2024-03-29 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_company_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='f_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='l_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='f_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='l_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
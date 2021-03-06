# Generated by Django 2.0.13 on 2019-03-09 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='timestampedmodel_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='maincourante.TimeStampedModel'),
        ),
        migrations.AlterField(
            model_name='messagesuppression',
            name='timestampedmodel_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='maincourante.TimeStampedModel'),
        ),
        migrations.AlterField(
            model_name='messageversion',
            name='timestampedmodel_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='maincourante.TimeStampedModel'),
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-29 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arriendos', '0002_clientemanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
        migrations.DeleteModel(
            name='ClienteManager',
        ),
    ]

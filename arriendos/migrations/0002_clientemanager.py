# Generated by Django 3.2.5 on 2021-07-28 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arriendos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteManager',
            fields=[
                ('cliente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='arriendos.cliente')),
            ],
            bases=('arriendos.cliente',),
        ),
    ]

# Generated by Django 5.0.7 on 2024-11-13 01:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estadio', '0002_cancha_ancho_cancha_largo_cancha_ubicacion_x_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(max_length=500)),
                ('cupo_total', models.IntegerField()),
                ('cupo_disponible', models.IntegerField()),
                ('estado', models.CharField(choices=[('activa', 'Activa'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='activa', max_length=10)),
                ('clase_profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clase_profesor', to=settings.AUTH_USER_MODEL)),
                ('clase_usuarios', models.ManyToManyField(related_name='clase_usuarios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

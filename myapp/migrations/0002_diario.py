# Generated by Django 4.2.6 on 2023-12-17 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="diario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fech_reg", models.DateField(blank=True, null=True)),
                ("hora_in", models.TimeField(blank=True)),
                ("hora_out", models.TimeField(blank=True)),
                ("retraso", models.BooleanField(default=False)),
                ("salida", models.BooleanField(default=False)),
                (
                    "empleado",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
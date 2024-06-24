# Generated by Django 4.2.6 on 2024-06-23 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("myapp", "0007_comentario"),
    ]

    operations = [
        migrations.CreateModel(
            name="calificacion",
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
                ("rating_need", models.IntegerField(blank=True, null=True)),
                ("rating_situation", models.IntegerField(blank=True, null=True)),
                ("rating_experience", models.IntegerField(blank=True, null=True)),
                ("rating_satisfaction", models.IntegerField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
# Generated by Django 5.0.7 on 2024-07-22 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Configuration",
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
                ("stt_key", models.CharField(max_length=100)),
                ("tts_key", models.CharField(max_length=100)),
                ("llm_key", models.CharField(max_length=100)),
                ("system_prompt", models.TextField()),
            ],
        ),
    ]

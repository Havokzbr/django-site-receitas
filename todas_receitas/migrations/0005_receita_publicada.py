# Generated by Django 4.1.2 on 2022-10-07 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todas_receitas', '0004_receita_pessoa'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='publicada',
            field=models.BooleanField(default=False),
        ),
    ]
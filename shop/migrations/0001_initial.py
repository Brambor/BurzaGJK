# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 15:37
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('negotiable', models.BooleanField()),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Abstraktní nabídky',
                'verbose_name': 'Abstraktní nabídka',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISBN', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Knihy',
                'verbose_name': 'Kniha',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('visited_class', models.CharField(choices=[('1B', '1.B'), ('R6A', 'R6.A')], max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Uživatelé',
                'verbose_name': 'Uživatel',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('abstractoffer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.AbstractOffer')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Book')),
                ('buyer', models.ManyToManyField(blank=True, related_name='purchase', to='shop.User')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='shop.User')),
            ],
            options={
                'verbose_name_plural': 'Nabídky',
                'verbose_name': 'Nabídka',
            },
            bases=('shop.abstractoffer',),
        ),
    ]
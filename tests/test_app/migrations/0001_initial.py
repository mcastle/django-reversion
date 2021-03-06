# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-11 03:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('reversion', '0004_auto_20160611_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191)),
                ('revision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reversion.Revision')),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='v1', max_length=191)),
            ],
        ),
        migrations.CreateModel(
            name='TestModelGenericInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('inline_name', models.CharField(default='v1', max_length=191)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='TestModelInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inline_name', models.CharField(default='v1', max_length=191)),
            ],
        ),
        migrations.CreateModel(
            name='TestModelParent',
            fields=[
                ('testmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='test_app.TestModel')),
                ('parent_name', models.CharField(default='parent v1', max_length=191)),
            ],
            bases=('test_app.testmodel',),
        ),
        migrations.AddField(
            model_name='testmodelinline',
            name='test_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.TestModel'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='related_instances',
            field=models.ManyToManyField(blank=True, related_name='_testmodel_related_instances_+', to='test_app.TestModel'),
        ),
    ]

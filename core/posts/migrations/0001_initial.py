# Generated by Django 2.1.5 on 2019-02-17 06:14

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0002_author_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('published_time', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_type', models.CharField(default='text/markdown', max_length=30)),
                ('comment', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=30)),
                ('published_time', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('source_url', models.URLField()),
                ('origin_url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('unlisted', models.BooleanField(default=False)),
                ('visible_to', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FOAF', 'Friend of a Friend'), ('FRIENDS', 'Friends'), ('PRIVATE', 'Private'), ('SERVERONLY', 'Local Friend')], default='PUBLIC', max_length=10)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=None)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Posts'),
        ),
    ]

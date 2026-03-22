from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('nature', 'Nature'), ('science', 'Science'), ('history', 'History'), ('technology', 'Technology'), ('health', 'Health & Wellness'), ('culture', 'Culture'), ('mystery', 'Mystery'), ('space', 'Space')], default='nature', max_length=50)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='podcasts/audio/')),
                ('spotify_link', models.URLField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='podcasts/thumbnails/')),
                ('duration', models.CharField(blank=True, max_length=20)),
                ('episode_number', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SpotifyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_url', models.URLField()),
                ('show_name', models.CharField(max_length=200)),
                ('show_description', models.TextField()),
                ('followers', models.CharField(blank=True, max_length=50)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

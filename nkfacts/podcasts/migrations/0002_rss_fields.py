from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='audio_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='podcast',
            name='thumbnail_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='podcast',
            name='rss_guid',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='spotifyprofile',
            name='rss_feed_url',
            field=models.URLField(blank=True, help_text='Your podcast RSS feed URL from Spotify for Podcasters.'),
        ),
        migrations.AddField(
            model_name='spotifyprofile',
            name='last_synced',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

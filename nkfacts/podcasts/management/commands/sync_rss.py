"""
Usage:
  python manage.py sync_rss
  python manage.py sync_rss --auto   (silent, for cron/scheduler)
"""
from django.core.management.base import BaseCommand
from podcasts.models import SpotifyProfile
from podcasts.rss_sync import sync_rss_feed


class Command(BaseCommand):
    help = 'Sync podcast episodes from the RSS feed'

    def add_arguments(self, parser):
        parser.add_argument('--auto', action='store_true', help='Run silently (for scheduled jobs)')

    def handle(self, *args, **options):
        profile = SpotifyProfile.objects.first()
        if not profile:
            self.stdout.write(self.style.ERROR(
                'No Spotify profile found. Add one at /admin → Spotify Profiles.'
            ))
            return

        self.stdout.write(f'Syncing from: {profile.rss_feed_url}')
        created, updated, error = sync_rss_feed(profile)

        if error:
            self.stdout.write(self.style.ERROR(f'Error: {error}'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Done! {created} new episodes added, {updated} updated.'
            ))

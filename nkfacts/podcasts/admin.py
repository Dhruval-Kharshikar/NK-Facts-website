from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html, mark_safe
from .models import Category, Podcast, SpotifyProfile, Review
from .rss_sync import sync_rss_feed


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('icon', 'name', 'slug', 'episode_count', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

    fieldsets = (
        ('Category Info', {
            'fields': ('name', 'slug', 'icon', 'is_active', 'order'),
            'description': (
                '💡 Tip: The slug is auto-filled from the name. '
                'Use a simple emoji in the Icon field.'
            )
        }),
        ('Auto-Detection Keywords (RSS Sync)', {
            'fields': ('keywords',),
            'description': (
                'When syncing from Spotify RSS, episodes whose title or description '
                'contain these keywords will be automatically assigned to this category. '
                'Separate keywords with commas. Example: forest, ocean, animal, wildlife'
            )
        }),
    )

    def episode_count(self, obj):
        count = obj.podcasts.filter(is_published=True).count()
        return format_html(
            '<span style="background:var(--pink,#e8547a);color:#fff;'
            'padding:2px 10px;border-radius:99px;font-size:.8rem;font-weight:600;">'
            '{}</span>', count
        )
    episode_count.short_description = 'Episodes'


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'episode_number', 'duration', 'source_tag', 'is_published', 'created_at')
    list_filter   = ('category', 'is_published')
    search_fields = ('title', 'description')
    list_editable = ('is_published', 'category')
    list_per_page = 20
    readonly_fields = ('rss_guid', 'audio_url', 'thumbnail_url')

    fieldsets = (
        ('Episode Info', {
            'fields': ('title', 'description', 'category', 'episode_number', 'duration', 'is_published'),
            'description': '💡 Change the Category dropdown to move this episode to a different section.'
        }),
        ('Media — Upload manually', {
            'fields': ('audio_file', 'thumbnail'),
        }),
        ('RSS / Spotify — Auto-filled', {
            'fields': ('audio_url', 'thumbnail_url', 'spotify_link', 'rss_guid'),
            'classes': ('collapse',),
        }),
    )

    def source_tag(self, obj):
        if obj.rss_guid:
            return mark_safe('<span style="background:#e8f5e9;color:#27ae60;padding:2px 8px;border-radius:99px;font-size:.75rem;font-weight:600;">🔄 RSS</span>')
        return mark_safe('<span style="background:#e3f2fd;color:#1565c0;padding:2px 8px;border-radius:99px;font-size:.75rem;font-weight:600;">✋ Manual</span>')
    source_tag.short_description = 'Source'


@admin.register(SpotifyProfile)
class SpotifyProfileAdmin(admin.ModelAdmin):
    list_display  = ('show_name', 'rss_feed_url', 'last_synced', 'sync_button')
    readonly_fields = ('last_synced',)

    fieldsets = (
        ('Spotify Show', {
            'fields': ('show_name', 'show_url', 'show_description', 'followers'),
        }),
        ('RSS Auto-Sync', {
            'fields': ('rss_feed_url', 'last_synced'),
            'description': (
                '📋 Find your RSS URL: podcasters.spotify.com → Your Show → Settings → RSS Feed'
            )
        }),
    )

    def sync_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/podcasts/spotifyprofile/{}/sync/" '
            'style="background:#e8547a;color:#fff;padding:5px 14px;border-radius:6px;'
            'text-decoration:none;font-weight:600;font-size:.85rem;">🔄 Sync Now</a>',
            obj.pk
        )
    sync_button.short_description = 'Sync Episodes'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom = [
            path('<int:pk>/sync/', self.admin_site.admin_view(self.sync_view), name='spotifyprofile_sync'),
        ]
        return custom + urls

    def sync_view(self, request, pk):
        from django.shortcuts import redirect
        profile = SpotifyProfile.objects.get(pk=pk)
        created, updated, error = sync_rss_feed(profile)
        if error:
            self.message_user(request, f'❌ Sync error: {error}', level=messages.ERROR)
        else:
            self.message_user(
                request,
                f'✅ Sync complete! {created} new episodes added, {updated} updated. '
                f'Check categories and fix any wrong ones.',
                level=messages.SUCCESS
            )
        return redirect('/admin/podcasts/podcast/')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('name', 'podcast', 'star_display', 'email', 'created_at')
    list_filter   = ('rating', 'podcast__category')
    search_fields = ('name', 'email', 'message', 'podcast__title')
    readonly_fields = ('name', 'email', 'rating', 'message', 'podcast', 'created_at')
    list_per_page = 20

    def star_display(self, obj):
        return mark_safe(
            '<span style="color:#f5a623; font-size:1.1rem;">' +
            '★' * obj.rating + '☆' * (5 - obj.rating) +
            f'</span> <span style="color:#999;">({obj.rating}/5)</span>'
        )
    star_display.short_description = 'Rating'

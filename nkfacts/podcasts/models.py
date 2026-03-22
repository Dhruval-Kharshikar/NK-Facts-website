from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,
        help_text="Short lowercase ID, no spaces. E.g. 'nature', 'true-crime'. Auto-filled.")
    icon = models.CharField(max_length=10, default='🎙️',
        help_text="Paste an emoji. E.g. 🌿 🔬 📜 🌌 🔮 💚 🎭 💻")
    keywords = models.TextField(blank=True,
        help_text="Comma-separated keywords for auto-detection from RSS. "
                  "E.g: forest, ocean, animal, wildlife, bird")
    order = models.PositiveIntegerField(default=0,
        help_text="Display order on website. Lower = appears first.")
    is_active = models.BooleanField(default=True,
        help_text="Uncheck to hide this category from the website.")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.icon} {self.name}"

    def get_keywords_list(self):
        """Returns list of stripped lowercase keywords."""
        if not self.keywords:
            return []
        return [k.strip().lower() for k in self.keywords.split(',') if k.strip()]


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='podcasts'
    )
    audio_file = models.FileField(upload_to='podcasts/audio/', blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    spotify_link = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='podcasts/thumbnails/', blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True)
    episode_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    rss_guid = models.CharField(max_length=500, blank=True, unique=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ep {self.episode_number}: {self.title}"

    def get_audio(self):
        if self.audio_file:
            return self.audio_file.url
        return self.audio_url or None

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return self.thumbnail_url or None

    def get_icon(self):
        return self.category.icon if self.category else '🎙️'


class SpotifyProfile(models.Model):
    show_url = models.URLField()
    rss_feed_url = models.URLField(
        blank=True,
        help_text="Your podcast RSS feed URL from Spotify for Podcasters."
    )
    show_name = models.CharField(max_length=200)
    show_description = models.TextField()
    followers = models.CharField(max_length=50, blank=True)
    last_synced = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.show_name


class Review(models.Model):
    RATING_CHOICES = [(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]

    podcast    = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='reviews')
    name       = models.CharField(max_length=100)
    email      = models.EmailField(blank=True)
    rating     = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}⭐ on {self.podcast.title}"

    def get_stars(self):
        return '⭐' * self.rating + '☆' * (5 - self.rating)

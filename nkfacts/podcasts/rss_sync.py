"""
rss_sync.py
───────────
Fetches podcast episodes from Spotify RSS and saves to database.
Categories and their keywords are stored in the database —
manage them from Admin → Categories.
"""

import urllib.request
import xml.etree.ElementTree as ET
from django.utils import timezone
from django.utils.html import strip_tags


def detect_category(title: str, description: str):
    """
    Scan title + description against each Category's keywords in the database.
    Returns the best matching Category object, or the first category as default.
    """
    from .models import Category

    title_lower = title.lower()
    desc_lower  = description.lower()

    categories  = Category.objects.filter(is_active=True)
    best_cat    = None
    best_score  = 0

    for cat in categories:
        score = 0
        for kw in cat.get_keywords_list():
            if kw in title_lower:
                score += 3       # title match = stronger signal
            if kw in desc_lower:
                score += 1       # description match
        if score > best_score:
            best_score = score
            best_cat   = cat

    # fallback → first active category
    if best_cat is None:
        best_cat = Category.objects.filter(is_active=True).first()

    return best_cat


def sync_rss_feed(profile):
    """
    Fetch all episodes from RSS and upsert into Podcast table.
    - New episodes  → auto-detect category from keywords
    - Existing ones → category is NEVER overwritten (preserves manual edits)
    Returns (created_count, updated_count, error_message).
    """
    from .models import Podcast

    if not profile.rss_feed_url:
        return 0, 0, "No RSS feed URL set. Add it in Admin → Spotify Profiles."

    # ── Fetch ──────────────────────────────────────────────────────
    try:
        req = urllib.request.Request(
            profile.rss_feed_url,
            headers={"User-Agent": "NKFacts-RSSSync/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
    except Exception as e:
        return 0, 0, f"Could not fetch RSS feed: {e}"

    # ── Parse ──────────────────────────────────────────────────────
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return 0, 0, f"Invalid RSS XML: {e}"

    ns = {
        'itunes':  'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'content': 'http://purl.org/rss/1.0/modules/content/',
    }

    channel = root.find('channel')
    if channel is None:
        return 0, 0, "RSS feed has no <channel> element."

    items   = channel.findall('item')
    created = updated = 0

    for idx, item in enumerate(items, start=1):

        guid_el = item.find('guid')
        guid    = guid_el.text.strip() if guid_el is not None and guid_el.text else None

        title_el = item.find('title')
        title    = title_el.text.strip() if title_el is not None and title_el.text else f"Episode {idx}"

        desc_el = (
            item.find('content:encoded', ns) or
            item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}summary') or
            item.find('description')
        )
        description = strip_tags(desc_el.text).strip() if desc_el is not None and desc_el.text else ""

        enclosure = item.find('enclosure')
        audio_url = enclosure.get('url', '') if enclosure is not None else ''

        dur_el   = item.find('itunes:duration', ns)
        duration = dur_el.text.strip() if dur_el is not None and dur_el.text else ''

        ep_el = item.find('itunes:episode', ns)
        try:
            episode_number = int(ep_el.text.strip()) if ep_el is not None and ep_el.text else (len(items) - idx + 1)
        except ValueError:
            episode_number = len(items) - idx + 1

        img_el    = item.find('itunes:image', ns)
        thumb_url = img_el.get('href', '') if img_el is not None else ''
        if not thumb_url:
            ch_img = channel.find('itunes:image', ns)
            if ch_img is not None:
                thumb_url = ch_img.get('href', '')

        link_el      = item.find('link')
        spotify_link = link_el.text.strip() if link_el is not None and link_el.text else ''

        # Auto-detect category for NEW episodes only
        auto_category = detect_category(title, description)

        if guid:
            podcast, is_new = Podcast.objects.get_or_create(
                rss_guid=guid,
                defaults={
                    'title':          title,
                    'description':    description,
                    'audio_url':      audio_url,
                    'thumbnail_url':  thumb_url,
                    'duration':       duration,
                    'episode_number': episode_number,
                    'spotify_link':   spotify_link,
                    'category':       auto_category,
                    'is_published':   True,
                }
            )
            if not is_new:
                podcast.title         = title
                podcast.description   = description
                podcast.audio_url     = audio_url
                podcast.thumbnail_url = thumb_url
                podcast.duration      = duration
                podcast.spotify_link  = spotify_link
                # category intentionally NOT updated — preserves manual edits
                podcast.save()
                updated += 1
            else:
                created += 1
        else:
            if not Podcast.objects.filter(title=title).exists():
                Podcast.objects.create(
                    title=title,
                    description=description,
                    audio_url=audio_url,
                    thumbnail_url=thumb_url,
                    duration=duration,
                    episode_number=episode_number,
                    spotify_link=spotify_link,
                    category=auto_category,
                    is_published=True,
                )
                created += 1

    profile.last_synced = timezone.now()
    profile.save()

    return created, updated, None

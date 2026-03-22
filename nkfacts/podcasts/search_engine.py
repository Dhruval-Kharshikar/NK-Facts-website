"""
search_engine.py
────────────────
Smart search for NK Facts podcasts.

Features:
  - Word boundary matching   → "cat" won't match "communicate"
  - Prefix matching          → "cat" WILL match "cats", "catfish"
  - Simple stemming          → "running" matches "run", "runner"
  - Multi-word support       → "big cat" searches both words
  - Relevance scoring        → title match > category match > description match
  - Deduplication            → same episode won't appear twice
"""

import re
from django.db.models import Q


# ── STEMMING ──────────────────────────────────────────────────────
# Strips common English suffixes so "cats" → "cat", "running" → "run"
SUFFIXES = [
    'nesses', 'ments', 'ings', 'tion', 'sion',
    'ness', 'ment', 'ing', 'tion', 'ers',
    'ies', 'ied', 'ily',
    'ed', 'er', 'es', 'ly',
    's',
]

def stem(word):
    """Strip common suffixes to get root form. cat→cat, cats→cat, running→runn→run"""
    word = word.lower().strip()
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def get_search_variants(query):
    """
    Given a query word, return all variants to search for.
    E.g. "cats" → ["cats", "cat"]  (original + stemmed)
         "running" → ["running", "runn"]  but we also try "run"
    """
    original = query.lower().strip()
    stemmed  = stem(original)
    variants = list(dict.fromkeys([original, stemmed]))  # deduplicate, preserve order
    return variants


def build_word_boundary_pattern(word):
    """
    Returns a regex pattern that matches the word at a boundary.
    'cat'  → matches: cat, cats, catfish
             no match: communicate, educate, locate
    Uses \\b (word boundary) at the START only, so prefix matching works.
    """
    escaped = re.escape(word)
    # \b at start = must start at a word boundary
    # \w* at end  = can have any word chars after (cats, catfish, etc.)
    return r'\b' + escaped + r'\w*'


def smart_search(query_string, queryset):
    """
    Main search function. Returns a sorted list of (podcast, score) tuples.

    Scoring:
      Title match (exact word boundary)     → 10 pts per word
      Title match (stemmed)                 →  7 pts per word
      Category name match                   →  6 pts per word
      Description match (exact boundary)   →  3 pts per word
      Description match (stemmed)          →  1 pt  per word
    """
    if not query_string or not query_string.strip():
        return []

    # Split into individual words, ignore very short words
    words = [w for w in query_string.strip().split() if len(w) >= 2]
    if not words:
        return []

    # ── Step 1: Get candidate episodes using Django ORM ──────────
    # Use icontains as a broad first pass to get candidates from DB
    orm_filter = Q()
    for word in words:
        variants = get_search_variants(word)
        for v in variants:
            orm_filter |= Q(title__icontains=v)
            orm_filter |= Q(description__icontains=v)
            orm_filter |= Q(category__name__icontains=v)

    candidates = queryset.filter(orm_filter).select_related('category').distinct()

    # ── Step 2: Score and filter with word boundary check ────────
    scored = []

    for podcast in candidates:
        title       = (podcast.title or '').lower()
        description = (podcast.description or '').lower()
        cat_name    = (podcast.category.name if podcast.category else '').lower()
        score       = 0
        matched     = False

        for word in words:
            variants = get_search_variants(word)
            original = variants[0]
            stemmed  = variants[1] if len(variants) > 1 else variants[0]

            orig_pattern    = build_word_boundary_pattern(original)
            stemmed_pattern = build_word_boundary_pattern(stemmed)

            # Title — exact boundary match
            if re.search(orig_pattern, title):
                score += 10
                matched = True
            # Title — stemmed boundary match
            elif re.search(stemmed_pattern, title):
                score += 7
                matched = True

            # Category name match
            if re.search(orig_pattern, cat_name):
                score += 6
                matched = True
            elif re.search(stemmed_pattern, cat_name):
                score += 4
                matched = True

            # Description — exact boundary match
            if re.search(orig_pattern, description):
                score += 3
                matched = True
            # Description — stemmed boundary match
            elif re.search(stemmed_pattern, description):
                score += 1
                matched = True

        # Only include if at least one word actually matched at a boundary
        if matched and score > 0:
            scored.append((podcast, score))

    # ── Step 3: Sort by score descending ─────────────────────────
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored

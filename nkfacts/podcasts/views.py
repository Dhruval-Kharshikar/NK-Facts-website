from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Category, Podcast, SpotifyProfile, Review
from .rss_sync import sync_rss_feed
from .search_engine import smart_search


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def home(request):
    featured   = Podcast.objects.filter(is_published=True).select_related('category')[:6]
    categories = Category.objects.filter(is_active=True)
    # pass list of (cat, count) tuples so template can access both easily
    categories_with_counts = [
        (cat, cat.podcasts.filter(is_published=True).count())
        for cat in categories
    ]
    return render(request, 'podcasts/home.html', {
        'featured': featured,
        'categories': categories,
        'categories_with_counts': categories_with_counts,
    })


def about(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'podcasts/about.html', {'categories': categories})


def spotify_page(request):
    profile     = SpotifyProfile.objects.first()
    sync_result = None
    if request.method == 'POST' and 'sync' in request.POST:
        if not is_admin(request.user):
            return HttpResponseForbidden("Only admins can sync episodes.")
        if profile and profile.rss_feed_url:
            created, updated, error = sync_rss_feed(profile)
            if error:
                sync_result = {'type': 'error', 'msg': error}
            else:
                sync_result = {'type': 'success', 'msg': f'Synced! {created} new episodes added, {updated} updated.'}
        else:
            sync_result = {'type': 'error', 'msg': 'No RSS feed URL configured yet.'}
    return render(request, 'podcasts/spotify.html', {
        'profile': profile,
        'sync_result': sync_result,
    })


@login_required
def categories_page(request):
    all_categories = Category.objects.filter(is_active=True)
    selected_slug  = request.GET.get('cat', '')
    selected_cat   = None

    if selected_slug:
        selected_cat = get_object_or_404(Category, slug=selected_slug, is_active=True)
        qs           = Podcast.objects.filter(category=selected_cat, is_published=True).select_related('category')
        paginator    = Paginator(qs, 12)
        page         = request.GET.get('page', 1)
        podcasts     = paginator.get_page(page)
        podcasts_by_cat = {}
    else:
        podcasts = None
        podcasts_by_cat = {}
        for cat in all_categories:
            qs = Podcast.objects.filter(category=cat, is_published=True).select_related('category')
            if qs.exists():
                podcasts_by_cat[cat.slug] = {'cat': cat, 'episodes': qs[:6]}  # show 6 per cat in all-view

    return render(request, 'podcasts/categories.html', {
        'categories':      all_categories,
        'podcasts':        podcasts,
        'podcasts_by_cat': podcasts_by_cat,
        'selected':        selected_slug,
        'selected_cat':    selected_cat,
    })


@login_required
def search_view(request):
    query      = request.GET.get("q", "").strip()
    cat_filter = request.GET.get("cat", "").strip()
    categories = Category.objects.filter(is_active=True)
    results    = []
    count      = None

    if query or cat_filter:
        base_qs = Podcast.objects.filter(is_published=True)

        # Apply category filter first if set
        if cat_filter:
            base_qs = base_qs.filter(category__slug=cat_filter)

        if query:
            # Use smart search engine — word boundary + stemming + scoring
            scored  = smart_search(query, base_qs)
            results = [podcast for podcast, score in scored]
        else:
            # Category-only filter — no text query, just list all in category
            results = list(base_qs.select_related("category"))

        count = len(results)

    return render(request, "podcasts/search.html", {
        "query":      query,
        "cat_filter": cat_filter,
        "categories": categories,
        "results":    results,
        "count":      count,
    })


@login_required
def podcast_detail(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk, is_published=True)
    related = Podcast.objects.filter(category=podcast.category, is_published=True).exclude(pk=pk).select_related('category')[:4]
    return render(request, 'podcasts/detail.html', {'podcast': podcast, 'related': related})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 🌸')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'podcasts/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, email=email,
                password=password1, first_name=first_name, last_name=last_name
            )
            login(request, user)
            messages.success(request, f'Welcome to NK Facts, {first_name}! 🌸')
            return redirect('home')
    return render(request, 'podcasts/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out. See you soon! 💕')
    return redirect('home')


@login_required
def reviews_page(request):
    podcasts = Podcast.objects.filter(is_published=True).select_related('category')
    selected_podcast = None
    submitted = False

    podcast_id = request.GET.get('episode', '')
    if podcast_id:
        selected_podcast = get_object_or_404(Podcast, pk=podcast_id, is_published=True)

    if request.method == 'POST':
        from django.core.mail import send_mail
        from django.conf import settings

        name       = request.POST.get('name', '').strip()
        email      = request.POST.get('email', '').strip()
        rating     = request.POST.get('rating', '').strip()
        message    = request.POST.get('message', '').strip()
        podcast_id = request.POST.get('podcast_id', '').strip()

        errors = []
        if not name:       errors.append('Name is required.')
        if not rating:     errors.append('Please select a star rating.')
        if not message:    errors.append('Review message is required.')
        if not podcast_id: errors.append('Please select an episode.')

        if not errors:
            try:
                podcast = Podcast.objects.get(pk=podcast_id)
                rating_int = int(rating)
                stars = '⭐' * rating_int + '☆' * (5 - rating_int)

                # Save to database
                Review.objects.create(
                    podcast=podcast,
                    name=name,
                    email=email,
                    rating=rating_int,
                    message=message,
                )

                # Send email to NK Facts inbox
                subject = f'New Review: {stars} for "{podcast.title}"'
                body = f"""
🌸 New Review on NK Facts
{'─' * 40}

Episode:  {podcast.title}
Rating:   {stars} ({rating_int}/5)
From:     {name}
Email:    {email if email else 'Not provided'}
Date:     {__import__('datetime').datetime.now().strftime('%d %b %Y, %I:%M %p')}

Review:
{message}

{'─' * 40}
Sent from NK Facts Website
                """.strip()

                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.REVIEW_RECIPIENT],
                    fail_silently=False,
                )

                submitted = True
                selected_podcast = podcast

            except Exception as e:
                errors.append(f'Could not send review: {str(e)}')

        if errors:
            messages.error(request, ' '.join(errors))

    return render(request, 'podcasts/reviews.html', {
        'podcasts':         podcasts,
        'selected_podcast': selected_podcast,
        'submitted':        submitted,
        'rating_range':          range(1, 6),
        'rating_range_reversed': [5, 4, 3, 2, 1],
    })


def custom_404(request, exception=None):
    categories = Category.objects.filter(is_active=True)
    return render(request, '404.html', {'categories': categories}, status=404)

def custom_500(request):
    return render(request, '500.html', {}, status=500)


def create_superuser_view(request):
    """
    Temporary view to create superuser on Render free tier.
    Visit: /setup-admin-nkfacts-2026/
    DELETE this view and URL after creating your superuser!
    """
    from django.http import HttpResponse
    from django.contrib.auth.models import User

    # Change these before deploying!
    USERNAME = 'nkadmin'
    EMAIL    = 'nkfacts.podcast@gmail.com'
    PASSWORD = 'NKFacts@2026!'

    if User.objects.filter(username=USERNAME).exists():
        return HttpResponse(f'✅ Superuser "{USERNAME}" already exists! Go to /admin to login.')

    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    return HttpResponse(
        f'✅ Superuser created!<br><br>'
        f'Username: {USERNAME}<br>'
        f'Password: {PASSWORD}<br><br>'
        f'<a href="/admin">Go to Admin Panel</a><br><br>'
        f'⚠️ DELETE this URL from urls.py after logging in!'
    )


def create_superuser_view(request):
    """
    TEMPORARY view to create superuser on Render free tier.
    DELETE this URL from urls.py after use!
    Visit: /setup-nkfacts-admin-2026/
    """
    from django.http import HttpResponse
    from django.contrib.auth.models import User

    # ── CHANGE THESE BEFORE DEPLOYING ──
    USERNAME = 'nkfacts_admin'
    EMAIL    = 'nkfacts.podcast@gmail.com'
    PASSWORD = 'NKFacts@2026!'
    # ────────────────────────────────────

    if User.objects.filter(username=USERNAME).exists():
        return HttpResponse(f"""
            <h2>✅ Superuser already exists!</h2>
            <p>Username: <strong>{USERNAME}</strong></p>
            <p>Password: <strong>{PASSWORD}</strong></p>
            <p><a href="/admin">Go to Admin Panel</a></p>
            <hr>
            <p style="color:red;">⚠️ Please delete this URL from urls.py now!</p>
        """)

    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    return HttpResponse(f"""
        <h2>🌸 Superuser created successfully!</h2>
        <p>Username: <strong>{USERNAME}</strong></p>
        <p>Password: <strong>{PASSWORD}</strong></p>
        <p><a href="/admin">Go to Admin Panel →</a></p>
        <hr>
        <p style="color:red;">⚠️ IMPORTANT: Delete this URL from urls.py immediately!</p>
    """)

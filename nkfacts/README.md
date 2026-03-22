# 🌸 NK Facts – Django Podcast Website

A beautiful baby-pink & white themed podcast website built with Django.

---

## 📁 Project Structure

```
nkfacts/
├── manage.py
├── requirements.txt
├── setup.sh
├── nkfacts/               ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── podcasts/              ← Main app
│   ├── models.py          ← Podcast & SpotifyProfile models
│   ├── views.py           ← All page views
│   ├── urls.py            ← URL routing
│   ├── admin.py           ← Admin panel config
│   └── migrations/
├── templates/podcasts/    ← HTML templates
│   ├── base.html          ← Navbar + footer layout
│   ├── home.html          ← Homepage with hero + featured episodes
│   ├── about.html         ← About page
│   ├── spotify.html       ← Spotify link page
│   ├── categories.html    ← Filterable categories page
│   ├── detail.html        ← Single episode page with audio player
│   ├── login.html         ← Login page
│   └── signup.html        ← Sign up page
├── static/
│   ├── css/style.css      ← Full baby pink & white theme
│   └── js/main.js         ← Animations & interactions
└── media/                 ← Uploaded audio & thumbnails (auto-created)
```

---

## 🚀 Quick Setup

### 1. Install Python (3.10+)
Make sure Python is installed: `python --version`

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create admin superuser
```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password).

### 6. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** 🎉

---

## 🎙️ Adding Podcasts

1. Go to **http://127.0.0.1:8000/admin**
2. Log in with your superuser credentials
3. Click **Podcasts → Add Podcast**
4. Fill in:
   - **Title** – Episode name
   - **Description** – Short description
   - **Category** – Nature / Science / History / etc.
   - **Audio file** – Upload your MP3/WAV file
   - **Thumbnail** – Episode cover image (optional)
   - **Spotify link** – Direct Spotify episode URL (optional)
   - **Duration** – e.g. `12 min`
   - **Episode number**
   - **Is published** ✅

---

## 🎵 Setting Up Your Spotify Profile

1. Go to admin → **Spotify Profiles → Add**
2. Enter your Spotify show URL, name, description
3. This appears on the `/spotify/` page

---

## 📄 Pages

| URL | Page | Auth Required |
|-----|------|--------------|
| `/` | Homepage | No |
| `/about/` | About NK Facts | No |
| `/spotify/` | Spotify link page | No |
| `/categories/` | Browse all categories | ✅ Yes |
| `/categories/?cat=nature` | Filter by category | ✅ Yes |
| `/podcast/<id>/` | Episode detail + audio | ✅ Yes |
| `/login/` | Login | No |
| `/signup/` | Sign Up | No |
| `/logout/` | Logout | No |
| `/admin/` | Django admin panel | Superuser |

---

## 🎨 Theme Customization

All colors are CSS variables in `static/css/style.css`:

```css
:root {
  --pink-300: #ff9dba;   /* light pink accents */
  --pink-400: #ff6b9d;   /* buttons, highlights */
  --pink-500: #e8547a;   /* primary brand color */
  --pink-600: #c73d63;   /* dark pink text */
  --white:    #ffffff;
  --off-white:#fdf6f9;   /* page background */
}
```

---

## 💡 Tips

- After adding audio files, they're served from `/media/` in development
- For production, use WhiteNoise or a CDN for static files
- Thumbnails are optional — category emoji icons show as fallback
- The `Pillow` library is required for image upload support

# Drainage Monitor (Mobile App)

Flutter mobile app for barangay personnel, part of a LoRa-based drainage clog monitoring system with automated multi-level alert escalation (capstone project).

The app shows the monitoring node's live status, notifies personnel when an alert fires, and lets them acknowledge, add remarks, and mark the problem cleared. If nobody responds in time, the alert escalates to the next level.

## Status

Early development. Done so far: theme system (light and dark), reusable components, and the privacy consent screens. Still to build: Login, Home, Alert Detail, History, Profile, and the data layer.

## Getting started

Requires Flutter 3.22 or newer.

```bash
git clone <your-repo-url>
cd <repo-folder>
flutter pub get
flutter run
```

## Public web dashboard

The resident-facing dashboard is a separate static page from the personnel Flutter app. To test it using Flutter's web server, run:

```bash
flutter run -d web-server --web-port 8080
```

Open `http://localhost:8080/public-dashboard.html`. The root URL (`http://localhost:8080/`) continues to show the Flutter app. The standalone page is `web/public-dashboard.html`; its original Drainage Monitor wordmark is an inline SVG that follows the dashboard theme. It starts in sample-data mode; connecting Supabase requires the public read-only views described in the dashboard configuration.

For static-only local serving, you can also run:

```bash
python -m http.server 8080 --directory web
```

Flutter's web build does not copy extra standalone HTML pages automatically. To include this dashboard beside the Flutter app in one deployment, run:

```bash
flutter build web
python tool/copy_public_dashboard.py
```

Then deploy the contents of `build/web/`. The dashboard will be available at `/public-dashboard.html`.

## Documentation

* [CODEBASE_GUIDE.md](guides/CODEBASE_GUIDE.md): how the project is organized, decisions already made, and team conventions. **Read this first.**
* [THEME_GUIDE.md](guides/THEME_GUIDE.md): how to change the color scheme from one file.

## Project structure

```text
lib/
  main.dart
  core/theme/    Colors, theme, status colors
  shared/        Reusable widgets
  features/      One folder per feature (privacy, and more to come)
```

## Notes

* Do not commit secrets or keys (for example `google-services.json` or API keys).
* Do not add real personal data of personnel or residents to the repository.

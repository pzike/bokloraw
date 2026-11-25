# Drainage Monitor Mobile App: Codebase Guide

Welcome. This guide explains what the app is for, how the code is organized, and the rules we follow so everyone's work fits together. Read it once top to bottom, then use it as a reference.

---

## 1. What we are building

A mobile app for barangay personnel that works with our LoRa-based drainage clog monitoring system.

- **Hardware side (not in this repo):** one node (ESP32-S3 with ultrasonic water-level sensor, rain sensor, LoRa) plus an ESP32-CAM for periodic photos, a Raspberry Pi gateway, and an MQTT-based server.
- **This repo:** the Flutter (Dart) mobile app. It shows the node's live status, notifies people when an alert fires, and lets them acknowledge, add remarks, and mark the problem cleared.
- **Residents** do not use this app. They use a separate public website.

### The system has exactly one node
Do not build node lists, maps, or per-node assignment screens. We keep a `node ID` in the data model so more nodes can be added later, but the UI is single-node.

---

## 2. Decisions that are already final

Please do not re-open these without a good reason and a team discussion.

| Topic | Decision |
|---|---|
| Framework | Flutter / Dart |
| Navigation | Three tabs: **Home, History, Profile**. Plus Login, Consent, and Alert Detail screens. |
| Roles | One app, role-based views. Level 1 = maintenance personnel, Level 2 = barangay officials, Level 3 = barangay captain. |
| Escalation | Alert goes to Level 1, then Level 2, then Level 3 if nobody acknowledges. Timeout is **15 minutes per level** (for now). |
| Rising water | If the water stage rises during an open alert, the current level is re-notified **without restarting the timer**. |
| Marking cleared | Anyone at Level 1 or above can mark an alert cleared. The node then confirms: water must read below stage 1, otherwise the alert **reopens automatically**. |
| Notifications | Push notifications first, SMS as a fallback for Level 2 and 3. |
| Accounts | Created by an admin only. No public sign-up. |
| Privacy | First-login consent screen (Data Privacy Act, RA 10173) and a Privacy section in Profile. |
| Branding | The app uses a color palette only. **Do not add the Pasig City or Barangay Maybunga logos anywhere in the app.** |
| Silence is not safety | If the node has not reported recently, show "No recent data. This is not an all-clear." |

### Still open (do not assume)
- Backend: the exact stack (MQTT broker, API, database) is not chosen yet. Firebase may be used for push only.
- Whether node photos show on the alert screen, and how they attach to alerts.
- Final wording of the privacy notice (needs review by our adviser or the barangay data protection officer).

---

## 3. Vocabulary

| Term | Meaning |
|---|---|
| **Stage 1, 2, 3** | The three water-level thresholds. 3 is the most severe (water over the curb). |
| **Level 1, 2, 3** | Escalation levels, meaning who gets notified. Not the same as stages. |
| **Acknowledge** | A person confirms they saw the alert and are responding. Stops the 15-minute timer. |
| **Cleared** | The person says the problem is fixed. The node must confirm by reading below stage 1. |
| **Stale** | The node has not reported recently, so its data cannot be trusted. |

---

## 4. Project structure

```
lib/
  main.dart                          App entry + temporary preview gallery
  core/
    theme/
      app_palette.dart               ALL hex colors live here (and only here)
      status_colors.dart             Alert status colors as a ThemeExtension
      app_theme.dart                 Builds light/dark ThemeData + context helpers
  shared/
    components.dart                  Reusable widgets (pill, alert banner, gauge, ...)
  features/
    privacy/
      privacy_screens.dart           ConsentScreen + PrivacySection
```

**Convention:** `core/` is app-wide plumbing (themes, later networking and auth). `shared/` is reusable widgets with no business logic. `features/<name>/` holds one feature each (home, alerts, history, profile, auth, privacy).

### What exists today vs. what is still to build

| Exists | To build |
|---|---|
| Theme system (light and dark) | Login screen |
| Reusable components | Home screen with live data |
| Consent screen and Privacy section | Alert Detail screen |
| Preview gallery (`main.dart`) | History and Profile screens |
| | Data layer (talking to the backend) |
| | Push notifications and SMS fallback |
| | Auth and role handling |

---

## 5. Setup and running

This repo contains only the `lib/` folder and docs. To run it:

1. Install Flutter **3.22 or newer** (the code uses `surfaceContainerHighest`).
2. Create a project: `flutter create drainage_app`
3. Replace the generated `lib/` folder with this repo's `lib/`.
4. Run `flutter pub get`, then `flutter run`.

No extra packages are needed yet. Everything uses Flutter's built-in Material library.

The preview gallery shows every component. Use the slider to change the water stage and watch the colors change. Switch your phone or emulator between light and dark mode to check both themes.

---

## 6. The theme system (the most important part)

The goal: **anyone can change the color scheme by editing one file.**

### 6.1 `app_palette.dart`: the single source of truth

This is the only file with hex values. It has:

- `PaletteMode`: the list of color roles for one brightness (header, primary, background, status colors, and so on).
- `AppPalette`: a light + dark pair. It has two presets, `pasig` (navy/blue chrome) and `maybunga` (green chrome).
- `activePalette`: the one-line switch.

```dart
const AppPalette activePalette = AppPalette.pasig; // change to AppPalette.maybunga
```

### 6.2 `app_theme.dart`: turns the palette into a Flutter theme

`AppTheme.light` and `AppTheme.dark` build a `ThemeData` from the active palette (color scheme, app bar, buttons, bottom navigation). It contains **no hex values**.

`main.dart` uses `themeMode: ThemeMode.system`, so the app follows the phone's light/dark setting.

### 6.3 `status_colors.dart`: alert colors

Flutter's built-in color scheme has no concept of "water stage 2", so we added a `ThemeExtension` called `StatusColors` with `normal`, `stage1`, `stage2`, `stage3`, and `stale`.

- `forStage(int)` returns the right color: 0 = normal, 1 to 3 = stage colors.
- `StatusColors.on(color)` returns white or dark text, whichever is readable on that background.

### 6.4 How to read colors in a widget

```dart
import '../core/theme/app_theme.dart';

// Brand and surface colors
context.colors.primary
context.colors.surface
context.colors.outline
context.colors.onSurfaceVariant   // secondary text

// Alert and water status colors
context.status.stage2
context.status.forStage(stage)
StatusColors.on(someBackground)   // readable text on that background
```

### 6.5 The color rules

1. **Never** write `Color(0xFF...)`, `Colors.red`, or any literal color in a screen or widget.
2. Need a new color role? Add a field to `PaletteMode` and fill it in **every** preset (light and dark).
3. Status colors must stay distinct from each other in both themes. Green, amber, and red carry meaning. Do not reuse them decoratively.
4. After editing the palette, use **hot restart**, not hot reload (the values are constants).

---

## 7. Shared components (`shared/components.dart`)

| Widget | Use it for |
|---|---|
| `StatusPill(label, color)` | Small badges such as "Online" or "Cleared" |
| `AlertBanner(stage, title, countdownText, onOpen)` | Big block at the top of Home when an alert is active. Color follows the stage. |
| `WaterLevelGauge(currentStage)` | Three bars for stages 1 to 3, filled up to the current stage |
| `EscalationTimeline(steps)` | Who was notified and when. Filled dot = happened, hollow = upcoming. |
| `StaleDataBanner(lastSeenText)` | Gray "No recent data" warning |

Example:

```dart
AlertBanner(
  stage: 2,
  title: 'Stage 2, clog detected',
  countdownText: 'Level 2 in 11:42',
  onOpen: () { /* navigate to Alert Detail */ },
)
```

Components take plain values and callbacks. They do **not** fetch data or know about the backend. Keep it that way so they stay reusable and testable.

---

## 8. Privacy screens (`features/privacy/privacy_screens.dart`)

- `ConsentScreen(onAccepted, onReadFullNotice)`: shown on first login. The checkbox **always starts unticked** and the Accept button stays disabled until it is ticked. Consent has to be an explicit action. The account should stay inactive until `onAccepted` fires.
- `PrivacySection(onViewNotice, onWithdrawConsent, onRequestData)`: drop into the Profile screen.

Privacy reminders for everyone:
- Collect only what we need (name, contact number, response records).
- The public resident website must never show personnel names or phone numbers.
- Node photos may capture passersby. Treat images as personal data.

---

## 9. How the app should behave (so you build the right thing)

### The alert loop
1. The node reports a water stage or clog. The server creates the alert and notifies **Level 1** (push). A 15-minute timer starts.
2. **Acknowledge** stops the timer and the alert becomes "In progress".
3. No acknowledgment in 15 minutes means **Level 2** is notified (push, then SMS fallback). Another 15 minutes means **Level 3** (the captain). If it is still ignored, the captain is re-alerted and the alert is flagged "Critical, unacknowledged".
4. Level 2 and above can **Reassign** an alert to a specific person.
5. Anyone at Level 1 or above can **Mark cleared**. The node must confirm the water is below stage 1, or the alert reopens.

### Screens
- **Home:** node status (water level, rain, power, last seen), the active alert block (or "All normal"), latest photo, small water trend.
- **Alert Detail:** **Acknowledge** is the main action (reachable within two taps from a notification), escalation timeline, photo or "image pending", remarks, Add remark, Mark cleared, Reassign (Level 2+).
- **History:** past incidents with filters. Level 1 sees their own responses. Level 2 and the captain see everyone's.
- **Profile:** account info, notification settings (push, SMS fallback, alert sound), Privacy section, logout.

### UX rules
- Acknowledging must always be quick: two taps from a notification or the Home screen.
- Show a visible "last seen" time. Stale data turns the status gray with a warning.
- Use words as well as colors ("All normal", "Stage 2") so nothing depends on color alone.
- Big touch targets and high contrast. Users are outdoors, in a hurry, on modest phones.

---

## 10. How to add a new screen

1. Create `lib/features/<feature>/<feature>_screen.dart`.
2. Build it with `Scaffold` and `AppBar` (the theme styles them automatically).
3. Use `context.colors` and `context.status` for every color.
4. Reuse widgets from `shared/components.dart` where you can. If you build something two screens need, move it into `shared/`.
5. Pass data in through constructor parameters. Do not hard-code values in the widget.

Skeleton:

```dart
import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('History')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: const [/* incident cards */],
      ),
    );
  }
}
```

---

## 11. Team conventions

- **Branches and commits:** small, focused changes. One feature per branch.
- **Formatting:** run `dart format .` before committing and keep `flutter analyze` clean.
- **Naming:** files in `snake_case.dart`, classes in `PascalCase`.
- **No color literals** (see section 6.5).
- **Test in both themes** (light and dark) and with the water stage slider before opening a pull request.
- **Ask before changing a final decision** (section 2).

---

## 12. Quick reference: "where do I change...?"

| I want to... | Go to |
|---|---|
| Change a color or switch palette | `core/theme/app_palette.dart` |
| Add a new color role | `PaletteMode` in `app_palette.dart`, then fill every preset |
| Change button or app bar styling | `core/theme/app_theme.dart` |
| Change the look of the alert banner or gauge | `shared/components.dart` |
| Change consent or privacy wording | `features/privacy/privacy_screens.dart` |
| Preview components | `main.dart` (`ComponentGallery`) |

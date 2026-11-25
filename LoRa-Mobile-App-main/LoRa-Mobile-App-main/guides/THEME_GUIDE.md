# Theme guide

## Where colors live
All hex values are in `lib/core/theme/app_palette.dart`. Nothing else in the app contains a color literal.

## Common changes
- **Switch the whole scheme:** in `app_palette.dart`, change
  `const AppPalette activePalette = AppPalette.pasig;` to `AppPalette.maybunga`.
- **Tweak one color:** edit it inside the preset (for example `stage2` for the amber).
- **Add a new scheme:** copy a preset, rename it, and point `activePalette` at it.
- Use hot restart (not hot reload) after editing a `const` palette.

## How widgets read colors
- Brand and surfaces: `context.colors.primary`, `.surface`, `.outline`, `.onSurfaceVariant`
- Alert status: `context.status.normal`, `.stage1`, `.stage2`, `.stage3`, `.stale`
- Text on a colored fill: `StatusColors.on(backgroundColor)` picks white or dark automatically.

## Rules to keep it easy to change
1. Never write `Color(0x...)` or `Colors.red` in a screen or widget.
2. Add a new token to `PaletteMode` if a new color role is needed, then fill it in every preset.
3. Status colors (green, amber, red, gray) must stay visually distinct from each other in both light and dark modes.

## Files
- `core/theme/app_palette.dart`: raw colors, presets, `activePalette`
- `core/theme/status_colors.dart`: alert status colors as a ThemeExtension
- `core/theme/app_theme.dart`: builds light and dark ThemeData, `context.colors` and `context.status` helpers
- `shared/components.dart`: StatusPill, AlertBanner, WaterLevelGauge, EscalationTimeline, StaleDataBanner
- `features/privacy/privacy_screens.dart`: ConsentScreen and PrivacySection
- `main.dart`: preview gallery (delete when real screens exist)

Requires Flutter 3.22 or newer (uses `surfaceContainerHighest`).
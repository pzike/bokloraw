"""Copy the standalone public dashboard into Flutter's built web output."""

from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
BUILD_WEB = ROOT / "build" / "web"
SOURCE_PAGE = ROOT / "web" / "public-dashboard.html"


def main() -> int:
    if not (BUILD_WEB / "index.html").is_file():
        print("Run `flutter build web` before copying the public dashboard.", file=sys.stderr)
        return 1

    if not SOURCE_PAGE.is_file():
        print("The public dashboard page is missing.", file=sys.stderr)
        return 1

    shutil.copy2(SOURCE_PAGE, BUILD_WEB / SOURCE_PAGE.name)
    print("Copied the public dashboard into build/web/public-dashboard.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

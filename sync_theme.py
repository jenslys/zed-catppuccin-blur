#!/usr/bin/env python3
import json
import requests
import os
import re
import sys
import time
import hashlib
from theme_overrides import THEME_OVERRIDES, VARIANT_MAP, BLUR_LEVELS, BASE_THEME_OVERRIDES

try:
    import jsonschema
except ImportError:
    print("jsonschema package not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])
    import jsonschema

# ANSI color codes
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# URLs
THEME_URL = "https://raw.githubusercontent.com/catppuccin/zed/main/themes/catppuccin-mauve.json"
SCHEMA_URL = "https://zed.dev/schema/themes/v0.2.0.json"
SCHEMA_CACHE_FILE = ".theme_schema_cache.json"

def print_header():
    print(f"\n{Colors.PURPLE}╭{'─' * 48}╮{Colors.RESET}")
    print(f"{Colors.PURPLE}│{Colors.RESET} {Colors.BOLD}🎨 Catppuccin Blur Theme Sync{Colors.RESET}{'  ' * 9}{Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}╰{'─' * 48}╯{Colors.RESET}\n")

def print_step(step: str, status: str = "info"):
    icons = {
        "info": f"{Colors.BLUE}ℹ{Colors.RESET}",
        "success": f"{Colors.GREEN}✓{Colors.RESET}",
        "error": f"{Colors.RED}✗{Colors.RESET}",
        "warning": f"{Colors.YELLOW}⚠{Colors.RESET}",
        "processing": f"{Colors.CYAN}◆{Colors.RESET}"
    }
    print(f"{icons.get(status, icons['info'])} {step}")

def progress_bar(current: int, total: int, prefix: str = "", width: int = 30):
    percent = current / total
    filled = int(width * percent)
    bar = f"{'█' * filled}{'░' * (width - filled)}"

    sys.stdout.write(f"\r{prefix} {Colors.CYAN}[{bar}]{Colors.RESET} {percent:.0%}")
    sys.stdout.flush()

    if current == total:
        print()  # New line when complete

def get_file_hash(filepath: str) -> str:
    """Calculate SHA256 hash of a file."""
    if not os.path.exists(filepath):
        return ""

    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_content_hash(content: str) -> str:
    """Calculate SHA256 hash of string content."""
    return hashlib.sha256(content.encode()).hexdigest()

def fetch_schema() -> dict:
    """
    Fetch and cache the Zed theme schema.
    Cache expires after 7 days to ensure we stay up-to-date.
    Falls back to cached version if network request fails.
    """
    if os.path.exists(SCHEMA_CACHE_FILE):
        cache_age = time.time() - os.path.getmtime(SCHEMA_CACHE_FILE)
        if cache_age < 7 * 24 * 60 * 60:
            print_step("Using cached theme schema", "info")
            with open(SCHEMA_CACHE_FILE, 'r') as f:
                return json.load(f)

    print_step("Fetching theme schema...", "processing")
    try:
        response = requests.get(SCHEMA_URL)
        response.raise_for_status()
        schema = response.json()

        with open(SCHEMA_CACHE_FILE, 'w') as f:
            json.dump(schema, f, indent=2)

        print_step("Theme schema fetched and cached", "success")
        return schema
    except Exception as e:
        print_step(f"Failed to fetch schema: {str(e)}", "warning")
        if os.path.exists(SCHEMA_CACHE_FILE):
            print_step("Falling back to cached schema", "info")
            with open(SCHEMA_CACHE_FILE, 'r') as f:
                return json.load(f)
        return None

def validate_theme(theme: dict, schema: dict) -> bool:
    """Validate theme against the Zed schema."""
    if not schema:
        print_step("Skipping validation - no schema available", "warning")
        return True

    try:
        jsonschema.validate(instance=theme, schema=schema)
        print_step("Theme validation passed", "success")
        return True
    except jsonschema.ValidationError as e:
        print_step(f"Theme validation failed: {e.message}", "error")
        print(f"{Colors.DIM}  Path: {'.'.join(str(p) for p in e.path)}{Colors.RESET}")
        return False
    except Exception as e:
        print_step(f"Validation error: {str(e)}", "error")
        return False

def fix_json(json_str):
    """
    Fix common JSON syntax errors in theme files.
    Removes trailing commas before closing brackets/braces.
    """
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    return json_str

def remove_alpha(color):
    """
    Remove alpha channel from hex colors.
    #RRGGBBAA -> #RRGGBB
    """
    if isinstance(color, str) and color.startswith('#'):
        if len(color) == 9:
            return color[:-2]
        elif len(color) == 6:
            return color
    return color

def fetch_theme():
    """
    Download the upstream Catppuccin theme from GitHub.
    Shows animated spinner during download with file size progress.
    """
    print_step("Fetching theme from upstream...", "processing")

    try:
        response = requests.get(THEME_URL, stream=True)
        response.raise_for_status()

        block_size = 8192
        downloaded = 0
        content = []

        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        spinner_idx = 0

        for data in response.iter_content(block_size):
            content.append(data)
            downloaded += len(data)

            sys.stdout.write(f"\r  {Colors.CYAN}{spinner[spinner_idx]}{Colors.RESET} Downloading... ({downloaded / 1024:.1f} KB)")
            sys.stdout.flush()
            spinner_idx = (spinner_idx + 1) % len(spinner)

        print()

        full_content = b''.join(content).decode('utf-8')

        print_step(f"Download complete! ({downloaded / 1024:.1f} KB)", "success")
        print_step("Parsing theme data...", "processing")

        fixed_json = fix_json(full_content)
        theme_data = json.loads(fixed_json)

        print_step("Theme data parsed successfully", "success")
        return theme_data

    except requests.RequestException as e:
        print_step(f"Failed to fetch theme: {str(e)}", "error")
        raise
    except json.JSONDecodeError as e:
        print_step(f"Failed to parse theme JSON: {str(e)}", "error")
        raise

def apply_blur(theme, generate_all_levels=False):
    """
    Apply blur modifications to the Catppuccin theme.
    Creates Espresso variants and applies custom overrides to all variants.

    Args:
        theme: The theme data to modify
        generate_all_levels: If True, generates all blur level variants
    """
    print_step("Applying blur modifications...", "processing")

    # Store original themes to create variants from
    original_themes = theme["themes"].copy()
    new_themes = []

    print_step("Creating Espresso variants...", "processing")
    macchiato_theme = None
    for theme_variant in original_themes:
        if "macchiato" in theme_variant["name"].lower():
            macchiato_theme = theme_variant.copy()
            break

    if macchiato_theme:
        # Add Espresso to base overrides for all blur levels
        for level_name, level_config in BLUR_LEVELS.items():
            espresso_theme = macchiato_theme.copy()
            espresso_theme["name"] = f"Catppuccin Espresso"
            espresso_theme["appearance"] = "dark"

            espresso_style = macchiato_theme["style"].copy()
            espresso_overrides = BASE_THEME_OVERRIDES["espresso"].copy()

            # Apply blur level to espresso overrides
            from theme_overrides import generate_theme_overrides_for_level
            level_overrides = generate_theme_overrides_for_level(espresso_overrides, level_config)

            for k, v in level_overrides.items():
                espresso_style[k] = v

            espresso_theme["style"] = espresso_style

            if level_name == "medium":
                # Use original name for medium blur
                espresso_theme["name"] = "Catppuccin Espresso (Blur)"
            else:
                # Use bracketed name for light/heavy
                espresso_theme["name"] = f"Catppuccin Espresso (Blur) [{level_name.capitalize()}]"

            new_themes.append(espresso_theme)

        print_step("Espresso variants created", "success")

    print(f"\n{Colors.BOLD}Generating all blur level variants:{Colors.RESET}")

    # Create variants for each blur level
    for level_name, level_config in BLUR_LEVELS.items():
        print(f"\n  {Colors.PURPLE}◆{Colors.RESET} Creating {Colors.BOLD}{level_name.capitalize()}{Colors.RESET} blur variants...")

        for original_theme in original_themes:
            variant_name = original_theme["name"].lower()

            # Find matching base variant
            for name, key_prefix in VARIANT_MAP.items():
                base_key = key_prefix.replace("_medium", "")  # Remove _medium suffix
                if name in variant_name:
                    new_theme = original_theme.copy()

                    # Original name for medium blur, bracketed names for others
                    if level_name == "medium":
                        new_theme["name"] = f"{original_theme['name']} (Blur)"
                    else:
                        new_theme["name"] = f"{original_theme['name']} (Blur) [{level_name.capitalize()}]"

                    style = new_theme["style"].copy()
                    override_key = f"{base_key}_{level_name}"

                    if override_key in THEME_OVERRIDES:
                        overrides = THEME_OVERRIDES[override_key]
                        for k, v in overrides.items():
                            style[k] = v

                        new_theme["style"] = style
                        new_themes.append(new_theme)
                        print(f"    {Colors.GREEN}✓{Colors.RESET} {original_theme['name']} ({level_name})")
                    break

    # Replace theme variants with new ones
    theme["themes"] = new_themes

    print(f"\n{Colors.GREEN}✓{Colors.RESET} All blur modifications applied successfully!")
    return theme

def main():
    print_header()

    start_time = time.time()

    output_path = "themes/catppuccin-blur.json"

    # Create themes directory
    os.makedirs("themes", exist_ok=True)
    print_step("Initialized themes directory", "success")

    # Get hash of existing file
    existing_hash = get_file_hash(output_path)

    try:
        print()
        schema = fetch_schema()

        print()
        theme = fetch_theme()
        print()
        theme = apply_blur(theme, True)

        print(f"\n{Colors.BOLD}Finalizing theme:{Colors.RESET}")
        print_step("Updating theme metadata...", "processing")

        theme["name"] = "Catppuccin Blur"
        theme["author"] = "Jens Lystad <jens@lystad.io>"
        theme["$schema"] = SCHEMA_URL
        variant_count = len(theme["themes"])

        print_step(f"Updated {variant_count} variant names", "success")

        # Validate theme before saving
        print(f"\n{Colors.BOLD}Validating theme:{Colors.RESET}")
        if not validate_theme(theme, schema):
            print_step("Theme validation failed - aborting", "error")
            sys.exit(1)

        # Generate new content
        new_content = json.dumps(theme, indent=2)
        new_hash = get_content_hash(new_content)

        # Check if content has changed
        if existing_hash == new_hash:
            print_step("No changes detected - theme is already up to date!", "info")

            # Summary for no changes
            elapsed = time.time() - start_time
            print(f"\n{Colors.BLUE}{'═' * 50}{Colors.RESET}")
            print(f"{Colors.BLUE}ℹ Theme is already up to date{Colors.RESET}")
            print(f"{Colors.DIM}   • No changes required{Colors.RESET}")
            print(f"{Colors.DIM}   • Time: {elapsed:.2f}s{Colors.RESET}")
            print(f"{Colors.DIM}   • Output: {output_path}{Colors.RESET}")
            print(f"{Colors.BLUE}{'═' * 50}{Colors.RESET}\n")
            return

        # Save theme if changes detected
        print_step("Changes detected - updating theme file...", "processing")

        with open(output_path, "w") as f:
            f.write(new_content)

        # Calculate file size
        file_size = os.path.getsize(output_path) / 1024  # KB
        print_step(f"Theme saved to {Colors.BOLD}{output_path}{Colors.RESET} ({file_size:.1f} KB)", "success")

        # Summary
        elapsed = time.time() - start_time
        print(f"\n{Colors.GREEN}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.GREEN}✨ Theme synchronization complete!{Colors.RESET}")
        print(f"{Colors.DIM}   • Variants: {variant_count}{Colors.RESET}")
        print(f"{Colors.DIM}   • Time: {elapsed:.2f}s{Colors.RESET}")
        print(f"{Colors.DIM}   • Output: {output_path}{Colors.RESET}")
        print(f"{Colors.GREEN}{'═' * 50}{Colors.RESET}\n")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠{Colors.RESET}  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}✗ Failed to update theme:{Colors.RESET} {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

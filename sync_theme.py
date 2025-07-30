#!/usr/bin/env python3
import json
import requests
import os
import re
import sys
import time
import hashlib
from typing import Dict, Any

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

# URL for Catppuccin theme
THEME_URL = "https://raw.githubusercontent.com/catppuccin/zed/main/themes/catppuccin-mauve.json"

# Theme-specific overrides
THEME_OVERRIDES = {
    "latte": {
        "background.appearance": "blurred",
        "background": "#f9fafcd7",
        "status_bar.background": "#f9fafcd7",
        "title_bar.background": "#f9fafcd7",
        "elevated_surface.background": "#f9fafc",
        "surface.background": "#f9fafcd0",
        "border": "#90909000",
        "hint.background": "#e8e8e8c0",
        "editor.background": "#00000000",
        "editor.line_number": "#00000020",
        "editor.active_line_number": "#0079ff90",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#007aff12",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#f9fafc",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#007aff12",
        "ghost_element.hover": "#007aff08",
        "ghost_element.active": "#007aff12",
        "ghost_element.selected": "#007aff12",
        "drop_target.background": "#007aff18",
        "editor.highlighted_line.background": "#007aff12",
        "error.background": "#ffd7d9",
        "warning.background": "#ffe5c0",
        "info.background": "#cce9f3",
        "success.background": "#d4eecf"
    },
    "frappe": {
        "background.appearance": "blurred",
        "background": "#303446d7",
        "status_bar.background": "#303446d7",
        "title_bar.background": "#303446d7",
        "elevated_surface.background": "#292c3c",
        "surface.background": "#303446d0",
        "border": "#00000000",
        "hint.background": "#414559c0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#ca9ee690",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#ca9ee612",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#303446",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#ca9ee612",
        "ghost_element.hover": "#ca9ee608",
        "ghost_element.active": "#ca9ee612",
        "ghost_element.selected": "#ca9ee612",
        "drop_target.background": "#ca9ee618",
        "editor.highlighted_line.background": "#ca9ee612",
        "error.background": "#3f2325",
        "warning.background": "#382d20",
        "info.background": "#1f3137",
        "success.background": "#243427"
    },
    "macchiato": {
        "background.appearance": "blurred",
        "background": "#24273ad7",
        "status_bar.background": "#24273ad7",
        "title_bar.background": "#24273ad7",
        "elevated_surface.background": "#1e2030",
        "surface.background": "#24273ad0",
        "border": "#00000000",
        "hint.background": "#363a4fc0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#f4dbd690",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#f4dbd612",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#24273a",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#f4dbd612",
        "ghost_element.hover": "#f4dbd608",
        "ghost_element.active": "#f4dbd612",
        "ghost_element.selected": "#f4dbd612",
        "drop_target.background": "#f4dbd618",
        "editor.highlighted_line.background": "#f4dbd612",
        "error.background": "#3d2224",
        "warning.background": "#362c1f",
        "info.background": "#1e2f35",
        "success.background": "#233225"
    },
    "mocha": {
        "background.appearance": "blurred",
        "background": "#1e1e2ed7",
        "status_bar.background": "#1e1e2ed7",
        "title_bar.background": "#1e1e2ed7",
        "elevated_surface.background": "#181825",
        "surface.background": "#1e1e2ed0",
        "border": "#00000000",
        "hint.background": "#313244c0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#f5e0dc90",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#f5e0dc12",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#1e1e2e",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#f5e0dc12",
        "ghost_element.hover": "#f5e0dc08",
        "ghost_element.active": "#f5e0dc12",
        "ghost_element.selected": "#f5e0dc12",
        "drop_target.background": "#f5e0dc18",
        "editor.highlighted_line.background": "#f5e0dc12",
        "error.background": "#3b2022",
        "warning.background": "#342a1e",
        "info.background": "#1c2d33",
        "success.background": "#213023"
    },
    "espresso": {
        "background.appearance": "blurred",
        "background": "#000000d7",
        "status_bar.background": "#000000d7",
        "title_bar.background": "#000000d7",
        "elevated_surface.background": "#0a0a0a",
        "surface.background": "#000000d0",
        "border": "#00000000",
        "hint.background": "#1a1a1ac0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#f4dbd690",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#f4dbd612",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#1a1a1a",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#f4dbd612",
        "ghost_element.hover": "#f4dbd608",
        "ghost_element.active": "#f4dbd612",
        "ghost_element.selected": "#f4dbd612",
        "drop_target.background": "#f4dbd618",
        "editor.highlighted_line.background": "#f4dbd612",
        "error.background": "#391e20",
        "warning.background": "#32281d",
        "info.background": "#1a2b31",
        "success.background": "#1f2e21"
    }
}

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

def fix_json(json_str):
    # Fix trailing commas
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    return json_str

def remove_alpha(color):
    # Check if color is in hex format and has alpha
    if isinstance(color, str) and color.startswith('#'):
        if len(color) == 9:  # #RRGGBBAA format
            return color[:-2]  # Remove alpha
        elif len(color) == 6:  # #RRGGBB format
            return color
    return color

def fetch_theme():
    print_step("Fetching theme from upstream...", "processing")
    
    try:
        # For GitHub raw URLs, just use a spinner as content-length is unreliable
        response = requests.get(THEME_URL, stream=True)
        response.raise_for_status()
        
        block_size = 8192
        downloaded = 0
        content = []
        
        # Animated spinner
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        spinner_idx = 0
        
        for data in response.iter_content(block_size):
            content.append(data)
            downloaded += len(data)
            
            # Show spinner with size info
            sys.stdout.write(f"\r  {Colors.CYAN}{spinner[spinner_idx]}{Colors.RESET} Downloading... ({downloaded / 1024:.1f} KB)")
            sys.stdout.flush()
            spinner_idx = (spinner_idx + 1) % len(spinner)
        
        print()  # New line after spinner
        
        # Join all chunks
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

def apply_blur(theme):
    print_step("Applying blur modifications...", "processing")
    
    # Map variant names to our override keys
    VARIANT_MAP = {
        "latte": "latte",
        "frappé": "frappe",  # Handle the é character
        "frappe": "frappe",  # Handle plain e version
        "macchiato": "macchiato",
        "mocha": "mocha"
    }
    
    # Add Espresso variant by cloning and modifying Macchiato
    print_step("Creating Espresso variant...", "processing")
    macchiato_theme = None
    for theme_variant in theme["themes"]:
        if "macchiato" in theme_variant["name"].lower():
            macchiato_theme = theme_variant.copy()
            break
    
    if macchiato_theme:
        espresso_theme = macchiato_theme.copy()
        espresso_theme["name"] = "Catppuccin Espresso"
        espresso_theme["appearance"] = "dark"
        
        # Keep Macchiato's syntax colors but apply our UI overrides
        espresso_style = macchiato_theme["style"].copy()
        for k, v in THEME_OVERRIDES["espresso"].items():
            espresso_style[k] = v
        
        espresso_theme["style"] = espresso_style
        theme["themes"].append(espresso_theme)
        print_step("Espresso variant created", "success")
    
    # Apply overrides to all variants
    print(f"\n{Colors.BOLD}Applying blur effects to variants:{Colors.RESET}")
    
    total_variants = len(theme["themes"])
    current = 0
    
    for theme_variant in theme["themes"]:
        current += 1
        variant_name = theme_variant["name"].lower()
        
        # Find the matching variant
        for name, key in VARIANT_MAP.items():
            if name in variant_name:
                # Apply the variant-specific overrides
                style = theme_variant["style"]
                overrides = THEME_OVERRIDES[key]
                
                # Show progress for current variant
                print(f"\n  {Colors.CYAN}◆{Colors.RESET} Processing {Colors.BOLD}{name.capitalize()}{Colors.RESET} variant...")
                
                # Apply our overrides with mini progress
                total_overrides = len(overrides.items())
                for idx, (k, v) in enumerate(overrides.items()):
                    style[k] = v
                    progress_bar(idx + 1, total_overrides, "    Applying styles", width=20)
                
                time.sleep(0.1)  # Small delay for visual effect
                print(f"    {Colors.GREEN}✓{Colors.RESET} {name.capitalize()} variant complete")
                break
    
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
        # Fetch and modify theme
        print()  # Add spacing
        theme = fetch_theme()
        print()  # Add spacing
        theme = apply_blur(theme)
        
        # Update theme metadata
        print(f"\n{Colors.BOLD}Finalizing theme:{Colors.RESET}")
        print_step("Updating theme metadata...", "processing")
        
        theme["name"] = "Catppuccin Blur"
        theme["author"] = "Jens Lystad <jens@lystad.io>"
        
        # Update variant names
        variant_count = 0
        for variant in theme["themes"]:
            if "espresso" not in variant["name"].lower():
                variant["name"] = f"{variant['name']} (Blur)"
            else:
                variant["name"] = f"{variant['name']} (Blur)"
            variant_count += 1
        
        print_step(f"Updated {variant_count} variant names", "success")
        
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
#!/usr/bin/env python3
import json
import requests
import os
import re

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
        "editor.highlighted_line.background": "#007aff12"
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
        "editor.highlighted_line.background": "#ca9ee612"
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
        "editor.highlighted_line.background": "#f4dbd612"
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
        "editor.highlighted_line.background": "#f5e0dc12"
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
        "editor.highlighted_line.background": "#f4dbd612"
    }
}

def fix_json(json_str):
    # Fix trailing commas
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    return json_str

def fetch_theme():
    response = requests.get(THEME_URL)
    response.raise_for_status()
    fixed_json = fix_json(response.text)
    return json.loads(fixed_json)

def apply_blur(theme):
    # Map variant names to our override keys
    VARIANT_MAP = {
        "latte": "latte",
        "frappé": "frappe",  # Handle the é character
        "frappe": "frappe",  # Handle plain e version
        "macchiato": "macchiato",
        "mocha": "mocha"
    }
    
    # Add Espresso variant by cloning and modifying Macchiato
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
    
    # Apply overrides to all variants
    for theme_variant in theme["themes"]:
        variant_name = theme_variant["name"].lower()
        
        # Find the matching variant
        for name, key in VARIANT_MAP.items():
            if name in variant_name:
                # Apply the variant-specific overrides
                style = theme_variant["style"]
                overrides = THEME_OVERRIDES[key]
                for k, v in overrides.items():
                    style[k] = v
                print(f"Applied overrides for {name}")
                break
    
    return theme

def main():
    os.makedirs("themes", exist_ok=True)
    
    try:
        # Fetch and modify theme
        theme = fetch_theme()
        theme = apply_blur(theme)
        
        # Update theme name and metadata
        theme["name"] = "Catppuccin Blur"
        theme["author"] = "Jens Lystad <jens@lystad.io>"
        
        # Update variant names
        for variant in theme["themes"]:
            if "espresso" not in variant["name"].lower():
                variant["name"] = f"{variant['name']} (Blur)"
            else:
                variant["name"] = f"{variant['name']} (Blur)"
        
        # Save theme
        output_path = "themes/catppuccin-blur.json"
        with open(output_path, "w") as f:
            json.dump(theme, f, indent=2)
            
        print(f"✓ Updated {output_path}")
        
    except Exception as e:
        print(f"✗ Failed to update theme: {str(e)}")

if __name__ == "__main__":
    main() 
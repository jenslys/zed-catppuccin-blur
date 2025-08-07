#!/usr/bin/env python3
"""
Theme override definitions for Catppuccin Blur variants.

Each variant has specific color and transparency overrides to create
the blur effect while maintaining Catppuccin's color scheme.
"""

# Blur intensity levels - higher values = less transparency/more opaque
BLUR_LEVELS = {
    "light": {"main": "99", "surface": "8c", "elements": "04", "active": "06"},  # 60% opacity
    "medium": {"main": "d7", "surface": "d0", "elements": "12", "active": "18"},  # 85% opacity (current)
    "heavy": {"main": "e0", "surface": "db", "elements": "1e", "active": "24"},   # 88% opacity
}

def generate_theme_overrides_for_level(base_overrides, level_config):
    """Generate theme overrides for a specific blur level."""
    overrides = base_overrides.copy()

    # Update transparency values based on blur level
    for key, value in overrides.items():
        if isinstance(value, str) and len(value) == 9 and value.startswith('#'):
            # Extract base color and replace alpha channel
            base_color = value[:7]
            if "background" in key and ("status_bar" in key or "title_bar" in key or key == "background"):
                overrides[key] = base_color + level_config["main"]
            elif "surface" in key:
                overrides[key] = base_color + level_config["surface"]
            elif any(elem in key for elem in ["ghost_element", "drop_target", "tab.active"]):
                overrides[key] = base_color + level_config["active"]
            elif any(elem in key for elem in ["thumb", "hover", "selected"]):
                overrides[key] = base_color + level_config["elements"]

    return overrides

# Base theme overrides (will be used to generate variants)
BASE_THEME_OVERRIDES = {
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

# Generate all theme overrides for all blur levels
THEME_OVERRIDES = {}
for level_name, level_config in BLUR_LEVELS.items():
    for variant_name, base_overrides in BASE_THEME_OVERRIDES.items():
        key = f"{variant_name}_{level_name}"
        THEME_OVERRIDES[key] = generate_theme_overrides_for_level(base_overrides, level_config)

"""
Map variant names from upstream to our override keys.
Handles both accented and plain versions of Frappé.
Maps to medium blur level (85% opacity) - this is the default blur level
used for original theme names like "Catppuccin Latte (Blur)".
"""
VARIANT_MAP = {
    "latte": "latte_medium",
    "frappé": "frappe_medium",
    "frappe": "frappe_medium",
    "macchiato": "macchiato_medium",
    "mocha": "mocha_medium"
}

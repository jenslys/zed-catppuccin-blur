#!/usr/bin/env python3
"""
Theme override definitions for Catppuccin Blur variants.

Each variant has specific color and transparency overrides to create
the blur effect while maintaining Catppuccin's color scheme.
"""

# Blur intensity levels - higher values = less transparency/more opaque
BLUR_LEVELS = {
    "light": {"main": "99", "surface": "8c", "elements": "80", "active": "90"},  # 60% opacity for main, solid for buttons
    "medium": {"main": "d7", "surface": "d0", "elements": "a0", "active": "b0"},  # 85% opacity for main, solid for buttons
    "heavy": {"main": "e0", "surface": "db", "elements": "c0", "active": "d0"},   # 88% opacity for main, solid for buttons
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
            elif any(elem in key for elem in ["drop_target", "tab.active"]):
                overrides[key] = base_color + level_config["active"]
            elif any(elem in key for elem in ["thumb", "hover", "selected"]) and "ghost_element" not in key:
                overrides[key] = base_color + level_config["elements"]
            # Note: ghost_element colors are kept as-is for solid buttons

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
        "border": "#ccd0da15",
        "hint.background": "#e8e8e8c0",
        "editor.background": "#00000000",
        "editor.line_number": "#00000020",
        "editor.active_line_number": "#0079ff90",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#f9fafc60",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#f9fafc",
        "pane_group.border": "#ccd0da15",
        "pane.focused_border": "#ccd0da10",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#8c8fa130",
        "ghost_element.background": "#f9fafc60",
        "ghost_element.hover": "#f9fafc90",
        "ghost_element.active": "#8839ef30",
        "ghost_element.selected": "#8839ef50",
        "drop_target.background": "#8839ef20",
        "editor.highlighted_line.background": "#007aff12",
        "error.background": "#ffd7d9",
        "warning.background": "#ffe5c0",
        "info.background": "#cce9f3",
        "success.background": "#d4eecf"
    },
    "iced_latte": {
        "background.appearance": "blurred",
        "background": "#e8f4ffd7",
        "status_bar.background": "#e8f4ffd7",
        "title_bar.background": "#e8f4ffd7",
        "elevated_surface.background": "#ddeeff",
        "surface.background": "#e8f4ffd0",
        "border": "#ccd0da15",
        "hint.background": "#d0e8ffc0",
        "editor.background": "#00000000",
        "editor.line_number": "#0066cc25",
        "editor.active_line_number": "#0077ee90",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#ddeeff60",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#ddeeff",
        "pane_group.border": "#ccd0da15",
        "pane.focused_border": "#ccd0da10",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#8cb4ff40",
        "ghost_element.background": "#ddeeff60",
        "ghost_element.hover": "#ddeeff90",
        "ghost_element.active": "#7287fd30",
        "ghost_element.selected": "#7287fd50",
        "drop_target.background": "#7287fd30",
        "editor.highlighted_line.background": "#0077ee15",
        "error.background": "#ffcad5",
        "warning.background": "#ffd8b8",
        "info.background": "#c0e0ff",
        "success.background": "#c8e8c0",
        "text": "#1a3855",
        "text.muted": "#3a5575",
        "text.accent": "#0066dd",
        "icon": "#1a3855",
        "icon.accent": "#0066dd",
        "element.hover": "#d0e8ffa0",
        "element.selected": "#7287fd40"
    },
    "frappe": {
        "background.appearance": "blurred",
        "background": "#303446d7",
        "status_bar.background": "#303446d7",
        "title_bar.background": "#303446d7",
        "elevated_surface.background": "#292c3c",
        "surface.background": "#303446d0",
        "border": "#41455915",
        "hint.background": "#414559c0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#ca9ee690",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#292c3c60",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#303446",
        "pane_group.border": "#41455915",
        "pane.focused_border": "#41455910",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#62688030",
        "ghost_element.background": "#292c3c60",
        "ghost_element.hover": "#292c3c90",
        "ghost_element.active": "#ca9ee630",
        "ghost_element.selected": "#ca9ee650",
        "drop_target.background": "#ca9ee630",
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
        "border": "#363a4f15",
        "hint.background": "#363a4fc0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#f4dbd690",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#1e203060",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#24273a",
        "pane_group.border": "#363a4f15",
        "pane.focused_border": "#363a4f10",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#8087a230",
        "ghost_element.background": "#1e203060",
        "ghost_element.hover": "#1e203090",
        "ghost_element.active": "#c6a0f630",
        "ghost_element.selected": "#c6a0f650",
        "drop_target.background": "#c6a0f620",
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
        "border": "#31324415",
        "hint.background": "#313244c0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#f5e0dc90",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#18182560",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#1e1e2e",
        "pane_group.border": "#31324415",
        "pane.focused_border": "#31324410",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#7f849c30",
        "ghost_element.background": "#18182560",
        "ghost_element.hover": "#18182590",
        "ghost_element.active": "#cba6f730",
        "ghost_element.selected": "#cba6f750",
        "drop_target.background": "#cba6f720",
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
        "border": "#363a4f15",
        "hint.background": "#1a1a1ac0",
        "editor.background": "#00000000",
        "editor.line_number": "#ffffff20",
        "editor.active_line_number": "#f4dbd690",
        "editor.gutter.background": "#00000000",
        "tab_bar.background": "#00000000",
        "terminal.background": "#00000000",
        "toolbar.background": "#00000000",
        "tab.active_background": "#0a0a0a60",
        "tab.inactive_background": "#00000000",
        "panel.background": "#00000000",
        "panel.focused_border": "00000000",
        "panel.overlay_background": "#1a1a1a",
        "pane_group.border": "#363a4f15",
        "pane.focused_border": "#363a4f10",
        "element.active": "#00000000",
        "border.variant": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.active_line.background": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.thumb.background": "#8087a230",
        "ghost_element.background": "#0a0a0a60",
        "ghost_element.hover": "#0a0a0a90",
        "ghost_element.active": "#c6a0f630",
        "ghost_element.selected": "#c6a0f650",
        "drop_target.background": "#c6a0f620",
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

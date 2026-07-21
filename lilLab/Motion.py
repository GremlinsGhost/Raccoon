class MotionProfile:
    def __init__(self, drag, scroll, resize, smoothness, inertia, easing):
        self.drag = drag
        self.scroll = scroll
        self.resize = resize
        self.smoothness = smoothness
        self.inertia = inertia
        self.easing = easing


def load_motion_settings(db):
    """
    Load motion settings from SQL into a MotionProfile.
    Raccoon-compatible version (no UI dependencies).
    """

    row = db.query("""
        SELECT
            drag_sensitivity,
            scroll_sensitivity,
            resize_sensitivity,
            slider_smoothness,
            inertia_strength,
            easing_curve
        FROM settings_input_motion
        ORDER BY id DESC
        LIMIT 1;
    """).fetchone()

    return MotionProfile(
        drag=row["drag_sensitivity"],
        scroll=row["scroll_sensitivity"],
        resize=row["resize_sensitivity"],
        smoothness=row["slider_smoothness"],
        inertia=row["inertia_strength"],
        easing=row["easing_curve"]
    )

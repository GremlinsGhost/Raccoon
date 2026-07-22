class MotionProfile:


    def __init__(self, drag=1.0, scroll=1.0, resize=1.0,
                 smoothness=0.85, inertia=0.15, easing="easeOutCubic"):

        self.drag = drag
        self.scroll = scroll
        self.resize = resize
        self.smoothness = smoothness
        self.inertia = inertia
        self.easing = easing


def default_motion():

    return MotionProfile(
        drag=1.0,
        scroll=1.0,
        resize=1.0,
        smoothness=0.85,
        inertia=0.15,
        easing="easeOutCubic"
    )

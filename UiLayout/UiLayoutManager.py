from .LayoutCompute import compute_layout
from .PanelRect import PanelRect
from .MotionProfile import MotionProfile


class UiLayoutManager:
    def __init__(self, width, height, layout_rows, motion=None):

        # Motion profile (ei SQL:ää)
        self.motion = motion or MotionProfile(
            drag=1.0,
            scroll=1.0,
            resize=1.0,
            smoothness=0.85,
            inertia=0.15,
            easing="easeOutCubic"
        )

        # Perusdata
        self.width = width
        self.height = height
        self.layout_rows = layout_rows

        # Paneelien rectit
        self.rects = {}
        self._init_rects()

        # Layout-tilat
        self.left_width = width // 2
        self.stage_height_ratio = 0.6
        self.tools_height_ratio = 0.6

        # Resize state
        self.active_resize = None

        # Stage itemit
        self.stage_items = []

        # Ensimmäinen layout
        self.update()


    # RECTIEN ALUSTUS
    def _init_rects(self):
        self.rects["root"] = PanelRect("root")
        self.rects["left"] = PanelRect("left")
        self.rects["right"] = PanelRect("right")
        self.rects["topbar"] = PanelRect("topbar")
        self.rects["bottombar"] = PanelRect("bottombar")

        for row in self.layout_rows:
            name = row["content_type"].lower()
            if name not in ("topbar", "bottombar"):
                self.rects[name] = PanelRect(name)


    # LAYOUT-PÄIVITYS
    def update(self):
        compute_layout(
            self.rects,
            self.layout_rows,
            self.left_width,
            self.stage_height_ratio,
            self.tools_height_ratio
        )


    # ROOT-RESIZE
    def resize(self, width, height):
        self.rects["root"].w = width
        self.rects["root"].h = height
        self.update()


    # RESIZE START
    def start_resize(self, panel, edge, mouse_pos):
        self.active_resize = {
            "panel": panel,
            "edge": edge,
            "start_mouse": mouse_pos,
            "start_rect": self.rects[panel].copy(),
        }


    # EASING
    def ease(self, current, target):
        return current + (target - current) * self.motion.smoothness


    # DRAG-RESIZE
    def drag_resize(self, mouse_pos):
        if not self.active_resize:
            return

        dx = mouse_pos[0] - self.active_resize["start_mouse"][0]
        dy = mouse_pos[1] - self.active_resize["start_mouse"][1]

        panel = self.active_resize["panel"]
        edge = self.active_resize["edge"]
        start_rect = self.active_resize["start_rect"]

        # LEFT / RIGHT SPLIT
        if panel == "left" and edge == "right":
            new_width = max(120, start_rect.w + dx * self.motion.resize)
            self.left_width = self.ease(self.left_width, new_width)

        # STAGE / LOG SPLIT
        elif panel == "stage" and edge == "bottom":
            total_h = self.rects["left"].h
            new_h = max(80, start_rect.h + dy * self.motion.resize)
            ratio = new_h / total_h
            self.stage_height_ratio = self.ease(
                self.stage_height_ratio,
                max(0.1, min(0.9, ratio))
            )

        # PROPERTIES / TOOLS SPLIT
        elif panel in ("properties", "tools") and edge == "bottom":
            total_h = self.rects["right"].h
            new_h = max(80, start_rect.h + dy * self.motion.resize)
            ratio = new_h / total_h
            self.tools_height_ratio = self.ease(
                self.tools_height_ratio,
                max(0.1, min(0.9, ratio))
            )


    # STAGE ITEMIT
    def set_stage_items(self, items):
        self.stage_items = items

    def get_stage_item(self, comp_id):
        for item in self.stage_items:
            if item["id"] == comp_id:
                return item
        return None

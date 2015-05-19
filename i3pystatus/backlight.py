from i3pystatus.file import File
from i3pystatus import Module
from i3pystatus.core.command import run_through_shell
import shutil


class Backlight(File):
    """
    Screen backlight info

    - Requires `xbacklight` to change the backlight brightness with the scollwheel.

    .. rubric:: Available formatters

    * `{brightness}` — current brightness relative to max_brightness
    * `{max_brightness}` — maximum brightness value
    * `{percentage}` — current brightness in percent
    """

    settings = (
        ("format", "format string, formatters: brightness, max_brightness, percentage"),
        ("backlight", "backlight, see `/sys/class/backlight/`"),
        "color",
    )
    required = ()

    backlight = "acpi_video0"
    format = "{brightness}/{max_brightness}"

    base_path = "/sys/class/backlight/{backlight}/"
    components = {
        "brightness": (int, "brightness"),
        "max_brightness": (int, "max_brightness"),
    }
    transforms = {
        "percentage": lambda cdict: round((cdict["brightness"] / cdict["max_brightness"]) * 100),
    }
    on_upscroll = "lighter"
    on_downscroll = "darker"

    def init(self):
        self.base_path = self.base_path.format(backlight=self.backlight)
        self.has_xbacklight = shutil.which("xbacklight") is not None
        super().init()

    def lighter(self):
        if self.has_xbacklight:
            run_through_shell(["xbacklight", "+5"])

    def darker(self):
        if self.has_xbacklight:
            run_through_shell(["xbacklight", "-5"])

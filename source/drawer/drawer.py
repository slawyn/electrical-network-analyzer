import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import traceback

from source.helpers import log
from .placer import Placer

# Constants


class Wire:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2


class NetworkDrawer:
    CANVAS_SIZE = (1920, 1080)
    UNIT = 10
    FONT_SIZE = 12

    # Colors
    COLOR = {
        "text": (255, 255, 255),
        "text_bg": (255, 0, 0),
        "wire": (0xFF, 0x88, 0x88),
        "node": (0xFF, 0x60, 0),
        "component": (0, 0, 0),
        "background": (100, 100, 100)
    }

    # 🔓 Public Methods
    def __init__(self, output_dir):
        self.map = {}
        self.output_dir = output_dir
        self.cftilesize = 60
        self.componentsize = 60 * 3
        self.x, self.y = 0, 0
        self.cfblockscntx = (self.CANVAS_SIZE[0] / self.cftilesize)
        self.cfblockscnty = (self.CANVAS_SIZE[1] / self.cftilesize)
        self.cfycenter = self.CANVAS_SIZE[1] / 2

    def draw_network(self, network):
        self.imagename = f"{network.get_name()}.png"

        placer = Placer(self.cftilesize, self.componentsize, self.cfblockscntx, self.cfblockscnty)
        for _ in range(1):
            self._init_canvas()
            elements = placer.place(network)
            self._draw_final_map(elements)
            self._draw_grid()
            self._draw_map()
            self._show()

    def _save_image(self):
        self.image.save(os.path.join(self.output_dir, self.imagename))

    def _clear_map(self):
        self.map.clear()

    def _add_to_map(self, element):
        start = element.getStart()
        self.map.setdefault(f"{start[0]}-{start[1]}", []).append(element)

    def _init_canvas(self):
        self.image = Image.new("RGB", self.CANVAS_SIZE, color=self.COLOR["background"])
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("arial.ttf", self.FONT_SIZE)

    def _draw_final_map(self, elements):
        self._clear_map()
        for e in elements:
            self._add_to_map(e)

    def _show(self):
        root = tk.Toplevel()
        root.title(self.imagename)
        self.tkImage = ImageTk.PhotoImage(self.image)
        label = tk.Label(root, image=self.tkImage)
        label.pack(side='top')
        self._save_image()
        # root.mainloop()

    def _draw_grid(self):
        for x in range(0, self.CANVAS_SIZE[0], self.cftilesize):
            for y in range(0, self.CANVAS_SIZE[1], self.cftilesize):
                self.draw.polygon([
                    (x, y),
                    (x + self.cftilesize, y),
                    (x + self.cftilesize, y + self.cftilesize),
                    (x, y + self.cftilesize)
                ], outline=self.COLOR["component"])

    def _draw_map(self):
        log("Elements:")
        categorized = {"W": [], "N": [], "C": [], "L": [], "R": []}
        for elements in self.map.values():
            for e in elements:
                log(f"[{e.get_type()}] {e.getStart()}")
                categorized.setdefault(e.get_type(), []).append(e)

        for group in ["W", "N", "C", "L", "R"]:
            for e in categorized.get(group, []):
                self._draw_element(e)

    def _draw_rotated_text(self, text, angle, position):
        bbox = self.draw.textbbox((0, 0), text, font=self.font)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        padding = 5
        img = Image.new('RGBA', (width + 2 * padding, height + 2 * padding), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, img.width, img.height), fill=self.COLOR["text_bg"])
        draw.text((padding, padding), text, font=self.font, fill=self.COLOR["text"])
        rotated = img.rotate(angle, expand=True, resample=Image.BICUBIC)
        self.image.paste(rotated, position, rotated)

    def _draw_element(self, e):
        for shape in e.getPolygons():
            fill = None
            outline = None
            t = e.get_type()
            if t == "W":
                fill = self.COLOR["wire"]
            elif t == "N":
                fill = self.COLOR["node"]
            elif t in {"L", "C"}:
                fill = self.COLOR["component"]
            elif t == "R":
                outline = self.COLOR["component"]

            self.draw.polygon(shape, fill=fill, outline=outline)

        if e.get_name():
            x, y = e.getStart()
            self._draw_rotated_text(e.get_name(), e.getAngle(), (int(x + 20), int(y)))

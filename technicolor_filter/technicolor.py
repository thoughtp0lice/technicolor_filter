from PIL import Image
import numpy as np


CYAN_SHADES = {
    "Process cyan": (0, 183, 235),
    "Cyan": (0, 255, 255),
    "Blue-green": (13, 152, 186),
    "Cerulean": (0, 123, 167),
    "Green-blue": (17, 100, 180),
    "Moonstone": (58, 168, 193),
    "Robin egg blue": (0, 204, 204),
    "Turquoise": (64, 224, 208),
}

MAGENTA_SHADES = {
    "Magenta dye": (202, 31, 123),
    "Process magenta": (255, 0, 144),
    "Magenta": (255, 0, 255),
    "Amaranth purple": (171, 39, 79),
    "Crayola": (246, 83, 166),
    "Razzle dazzle rose": (255, 51, 204),
    "Hot Magenta": (255, 29, 206),
    "Shocking Pink": (252, 15, 192),
    "Telemagenta": (207, 52, 118),
    "Quinacridone Magenta": (154, 17, 79),
}

YELLOW_SHADES = {
    "Yellow": (255, 255, 0),
    "Process yellow": (255, 239, 0),
    "Xanthic": (238, 237, 9),
    "Psychological primary yellow": (255, 211, 0),
    "Pantone yellow": (254, 223, 0),
    "Munsell yellow": (239, 204, 0),
    "Maximum Yellow": (250, 250, 55),
    "Royal Yellow": (250, 218, 94),
    "Cyber Yellow": (255, 211, 0),
}

RED_SHADES = {"Red": (255, 0, 0), "Orange red": (255, 69, 0)}


class Technicolor:
    def __init__(self, img):
        # Basic settings
        img = np.array(img)
        self._img = img.astype(int)
        self._cyan = CYAN_SHADES["Cyan"]
        self._magenta = MAGENTA_SHADES["Magenta"]
        self._yellow = YELLOW_SHADES["Yellow"]
        self._key_level = 0.0
        self._channels = {"r": None, "g": None, "b": None}
        self._layers = {"cyan": None, "magenta": None, "yellow": None, "key": None}

        # get rgb layers
        r = np.zeros_like(img)
        r[:, :, 0] = r[:, :, 1] = r[:, :, 2] = img[:, :, 0]
        self._channels["r"] = r
        g = np.zeros_like(img)
        g[:, :, 0] = g[:, :, 1] = g[:, :, 2] = img[:, :, 1]
        self._channels["g"] = g
        b = np.zeros_like(img)
        b[:, :, 0] = b[:, :, 1] = b[:, :, 2] = img[:, :, 2]
        self._channels["b"] = b

    def process(self):
        """
        dying each channel of the image
        and produce the technicolor output
        """
        self._layers["cyan"] = np.zeros_like(self._img)
        self._layers["cyan"][:, :, :] = self._cyan
        self._layers["magenta"] = np.zeros_like(self._img)
        self._layers["magenta"][:, :, :] = self._magenta
        self._layers["yellow"] = np.zeros_like(self._img)
        self._layers["yellow"][:, :, :] = self._yellow

        # dying each layers
        self._layers["cyan"] = (
            self._layers["cyan"] * 255
            + self._channels["r"] * (255 - self._layers["cyan"])
        ) // 255
        self._layers["magenta"] = (
            self._layers["magenta"] * 255
            + self._channels["g"] * (255 - self._layers["magenta"])
        ) // 255
        self._layers["yellow"] = (
            self._layers["yellow"] * 255
            + self._channels["b"] * (255 - self._layers["yellow"])
        ) // 255

        self._layers["key"] = (
            self._channels["g"] + (1 - self._key_level) * (255 - self._channels["g"])
        ).astype(int)

        self._technicolor_img = (
            self._layers["cyan"]
            * self._layers["magenta"]
            * self._layers["yellow"]
            * self._layers["key"]
            // (255 ** 3)
        )

    def show(self, img="technicolor", color_layer=None):
        """
        show the processed technicolor image
        when @img is set to original show the original image
        when @color_layer is not none
        show the @color_layer of the technicolor img
        @color must be cyan, magenta, yellow or key
        """
        self.process()

        if color_layer is not None:
            try:
                out_image = self._layers[color_layer]
            except KeyError:
                raise KeyError(
                    "Can only show cyan, magenta, yellow or key layer. %s is not one of them"
                    % color_layer
                )
        else:
            if img == "technicolor":
                out_image = self._technicolor_img
            elif img == "original":
                out_image = self._img
            else:
                raise ValueError(
                    "img can only be set to 'technicolor' or 'original'. %s is not one of them"
                    % img
                )

        out = Image.fromarray(out_image.astype(np.uint8), "RGB")
        out.show()

    def set_color(self, color, shade):
        """
        set one @color of cyan, magenta, yellow to @shade
        @shade can be a string of inculded shades or a tuple of rgb color
        """
        if isinstance(shade, str):
            try:
                if color == "cyan":
                    self._cyan = CYAN_SHADES[shade]
                elif color == "magenta":
                    self._magenta = MAGENTA_SHADES[shade]
                elif color == "yellow":
                    self._yellow = YELLOW_SHADES[shade]
                else:
                    raise ValueError("%s is not one of the editable colors" % color)
            except KeyError:
                raise KeyError(
                    "%s is not one of the supported shades of %s" % (shade, color)
                )
        elif len(shade) == 3:
            if color == "cyan":
                self._cyan = (int(shade[0]), int(shade[1]), int(shade[2]))
            elif color == "magenta":
                self._magenta = (int(shade[0]), int(shade[1]), int(shade[2]))
            elif color == "yellow":
                self._yellow = (int(shade[0]), int(shade[1]), int(shade[2]))
        else:
            raise ValueError("%s is not a supported type of shade")

    def set_all_color(self, shades):
        """
        @shades: list of shades colors in order of cyan, magenta, yellow
        if there is a 4-th value it will be interpreted as key level
        """
        colors = ["cyan", "magenta", "yellow"]

        if len(shades) == 4:
            self.set_key_level(shades[3])
            shades = shades[:3]

        for color, shade in zip(colors, shades):
            self.set_color(color, shade)

    def to_two_color(self, cyan="Cyan", red="Red"):
        """
        change the color mode to two color technicolor mode
        set the cyan color to @cyan and red to @red
        @cyan and @red can be shade name or rgb values
        """
        self.set_color("cyan", cyan)
        self.set_color("yellow", (255, 255, 255))
        try:
            self.set_color("magenta", RED_SHADES[red])
        except ValueError:
            raise ValueError("%s is not one of the supported shades of red" % shade)

    def to_default(self):
        """
        change the colors back to default
        """
        self.set_all_color(["Cyan", "Magenta", "Yellow", 0.0])

    def save(self, filename, img="technicolor", color_layer=None, save_format=None):
        """
        save the processed technicolor image to @filename
        when @img is set to original save the original image
        when @color_layer is not none
        save the @color_layer of the technicolor img
        @color must be cyan, magenta, yellow or key
        """
        self.process()

        if color_layer is not None:
            try:
                out_image = self._layers[color]
            except KeyError:
                raise KeyError(
                    "Can only show cyan, magenta, yellow or key layer. %s is not one of them"
                    % color_layer
                )
        else:
            if img == "technicolor":
                out_image = self._technicolor_img
            elif img == "original":
                out_image = self._img
            else:
                raise ValueError(
                    "img can only be set to 'technicolor' or 'original'. %s is not one of them"
                    % img
                )

        out = Image.fromarray(out_image.astype(np.uint8), "RGB")
        out.save(filename, format=save_format)

    def set_key_level(self, key_level):
        """
        @key_level when set to 0 means no key
        when set to 1.0 means a full layer of key is added 
        """
        self._key_level = key_level

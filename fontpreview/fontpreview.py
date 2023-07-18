#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# edited and updted by: Parijat Das @ https://t.me/parijatsoftwares
# fontpreview -- fontpreview
#
#     Copyright (C) 2020 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from PIL import Image, ImageDraw, ImageFont

CALC_POSITION = {
    'center': lambda ixy, fxy: ((ixy[0] - fxy[0]) // 2, (ixy[1] - fxy[1]) // 2),
    'top': lambda ixy, fxy: ((ixy[0] - fxy[0]) // 2, 20),
    'below': lambda ixy, fxy: ((ixy[0] - fxy[0]) // 2, (ixy[1] - fxy[1]) - 20),
    'rcenter': lambda ixy, fxy: ((ixy[0] - fxy[0]), (ixy[1] - fxy[1]) // 2),
    'rtop': lambda ixy, fxy: ((ixy[0] - fxy[0]), 20),
    'rbelow': lambda ixy, fxy: ((ixy[0] - fxy[0]), (ixy[1] - fxy[1]) - 20),
    'lcenter': lambda ixy, fxy: (20, (ixy[1] - fxy[1]) // 2),
    'ltop': lambda ixy, fxy: (20, 20),
    'lbelow': lambda ixy, fxy: (20, (ixy[1] - fxy[1]) - 20),
}


class FontPreview:
    def __init__(self, font, font_size=64, font_text='a b c d e f', color_system='RGB',
                 bg_color='white', fg_color='black', dimension=(700, 327)):
        self.image = None
        self.font_size = font_size
        self.font_text = font_text
        self.font = ImageFont.truetype(font=font, size=self.font_size)
        self.color_system = color_system
        self.bg_image = None
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.dimension = dimension
        self.font_position = CALC_POSITION['center'](self.dimension, self.font.getsize(self.font_text))
        self.reposition = "center"
        self.draw()

    def __str__(self):
        return "font_name:{font},font_size:{size},text:{text},text_position:{position},dimension:{dimension}".format(
            font=self.font.getname(), size=self.font_size, text=self.font_text,
            position=self.font_position, dimension=self.dimension
        )

    def __resize(self):
        img = ImageDraw.Draw(self.image)
        text_size = img.multiline_textsize(self.font_text, self.font)
        while text_size > self.dimension:
            self.font_size = self.font_size - 2
            self.font = ImageFont.truetype(font=self.font.path, size=self.font_size)
            text_size = img.multiline_textsize(self.font_text, self.font)

    def save(self, path=os.path.join(os.path.abspath(os.getcwd()), 'fontpreview.png')):
        self.image.save(path)

    def draw(self):
        if self.reposition in ['center', 'lcenter', 'rcenter']:
            if self.bg_image:
                self.image = Image.open(self.bg_image)
            else:
                self.image = Image.new(self.color_system, self.dimension, color=self.bg_color)
            draw = ImageDraw.Draw(self.image)
            text_width, text_height = draw.textsize(self.font_text, font=self.font)
            y = (self.dimension[1] - text_height) // 2
            if self.reposition == 'center':
                x = (self.dimension[0] - text_width) // 2
            elif self.reposition == 'lcenter':
                x = 20  # Adjust the x position for lcenter alignment
            elif self.reposition == 'rcenter':
                x = self.dimension[0] - text_width - 20  # Adjust the x position for rcenter alignment
            draw.text((x, y), self.font_text, fill=self.fg_color, font=self.font, align='left')
        else:
            if self.bg_image:
                self.image = Image.open(self.bg_image)
            else:
                self.image = Image.new(self.color_system, self.dimension, color=self.bg_color)
            draw = ImageDraw.Draw(self.image)
            draw.text(self.font_position, self.font_text, fill=self.fg_color, font=self.font, align='left')

    def show(self):
        self.image.show()

    def set_font_size(self, size):
        self.font_size = size
        self.font = ImageFont.truetype(font=self.font.path, size=self.font_size)
        self.__resize()
        self.draw()

    def set_text_position(self, position):
        self.reposition = position
        img = ImageDraw.Draw(self.image)
        if isinstance(position, tuple):
            self.font_position = position
        else:
            self.font_position = CALC_POSITION.get(position, CALC_POSITION['center'])(
                self.dimension, img.multiline_textsize(self.font_text, self.font)
            )
        self.draw()

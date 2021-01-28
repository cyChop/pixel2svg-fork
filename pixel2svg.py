#!/usr/bin/env python

"""pixel2svg - Convert pixel art to SVG

   Copyright 2011 Florian Berger <fberger@florian-berger.de>
   Copyright 2015 Cyrille Chopelet
   Copyright 2020 Ale Rimoldi <ale@graphicslab.org>
"""

# pixel2svg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pixel2svg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pixel2svg.  If not, see <http://www.gnu.org/licenses/>.

import argparse

import os.path
import PIL.Image
import svgwrite

VERSION = "0.5.0"

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="Convert pixel art to SVG")

    argument_parser.add_argument("imagefile",
                                 help="The image file to convert")

    argument_parser.add_argument("--overlap",
                                 action="store_true",
                                 help="If given, overlap vector squares by 1px")

    argument_parser.add_argument("--version",
                                 action="version",
                                 version=VERSION,
                                 help="Display the program version")

    argument_parser.add_argument("--squaresize",
                                 type=int,
                                 default=40,
                                 help="Width and height of vector squares in pixels, default: 40")


    arguments = argument_parser.parse_args()

    print("pixel2svg {0}".format(VERSION))
    print("Reading image file '{0}'".format(arguments.imagefile))

    image = PIL.Image.open(arguments.imagefile)

    print("Converting image to RGBA")

    image = image.convert("RGBA")

    (width, height) = image.size

    print("Image is {0}x{1}".format(width, height))

    rgb_values = list(image.getdata())

    print("Read {0} pixels".format(len(rgb_values)))

    svgdoc = svgwrite.Drawing(filename=os.path.splitext(arguments.imagefile)[0] + ".svg",
                              size=("{0}px".format(width * arguments.squaresize),
                                    "{0}px".format(height * arguments.squaresize)))

    # If --overlap is given, use a slight overlap to prevent inaccurate SVG rendering
    rectangle_size = ("{0}px".format(arguments.squaresize + arguments.overlap),
                      "{0}px".format(arguments.squaresize + arguments.overlap))

    rowcount = 0

    print("Will use an square overlap of {0}px".format(arguments.overlap))

    while rowcount < height:

        print("Processing pixel row {0} of {1}".format(rowcount + 1, height))

        colcount = 0

        while colcount < width:

            rgb_tuple = rgb_values.pop(0)

            # Omit transparent pixels
            if rgb_tuple[3] > 0:

                rectangle_posn = ("{0}px".format(colcount * arguments.squaresize),
                                  "{0}px".format(rowcount * arguments.squaresize))
                rectangle_fill = svgwrite.rgb(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

                alpha = rgb_tuple[3];
                if alpha == 255:
                    svgdoc.add(svgdoc.rect(insert=rectangle_posn,
                                           size=rectangle_size,
                                           fill=rectangle_fill))
                else:
                    svgdoc.add(svgdoc.rect(insert=rectangle_posn,
                                           size=rectangle_size,
                                           fill=rectangle_fill,
                                           opacity=alpha/float(255)))

            colcount = colcount + 1

        rowcount = rowcount + 1

    print("Saving SVG to '{0}'".format(svgdoc.filename))

    svgdoc.save()

    print("Operation finished. Have fun with your SVG.")

#!/usr/bin/env python3

from PIL import Image
import argparse
import sys

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file',
                        help='input image file')

    # Height and width arguments
    # Note: currently, only one can (and must) be specified, as an option
    # to not maintain scale has not yet been implemented
    dimensions = parser.add_mutually_exclusive_group(required=True)
    dimensions.add_argument('--height',
                            default=None,
                            help='desired output height (inches)')
    dimensions.add_argument('--width',
                            default=None,
                            help='desired output width (inches)')
    
    parser.add_argument('--dpi',
                        default=None,
                        type=float,
                        help='desired output DPI')
    parser.add_argument('--margin',
                        default=0.5,
                        type=float,
                        help='page margin size, in inches')
    parser.add_argument('--page_height',
                        default=11.0,
                        type=float,
                        help='page size, in inches')
    parser.add_argument('--page_width',
                        default=8.5,
                        type=float,
                        help='page width, in inches')

    args = parser.parse_args()

    input_image = open_image(args.input_file)
    input_height, input_width = input_image.size
    print('Loaded image {}:'.format(args.input_file),
            input_image.format,
            "{}x{}".format(input_height, input_width),
            input_image.mode)

    # Determine output height, in inches
    if args.height:
        # Height specified via argument
        output_height_inches = float(args.height)
    else:
        # Set height based on width and image scale
        output_height_inches = float(args.width) * input_height/input_width

    # Determine output width, in inches
    if args.width:
        output_width_inches = float(args.width)
    else:
        output_width_inches = float(args.height) * input_width/input_height

    print('Output image size will be {:.1f}" high and {:.1f}" wide'.format(
            output_height_inches, output_width_inches))

    # Determine output pixel size
    if args.dpi:
        output_dpi = float(args.dpi)
        output_height_px = int(output_height_inches * output_dpi)
        output_width_px = int(output_width_inches * output_dpi)

        print('Resizing output image to {}x{}px'.format(
                output_height_px, output_width_px))

        output_image = input_image.resize( (output_height_px, output_width_px) )
    else:
        output_image = input_image

    

def open_image(filename):
    try:
        return Image.open(filename)
    except IOError:
        print('Error loading input file "{}", please make sure it exists and is in a supported image format'.format(filename))
        sys.exit(1)

if __name__ == "__main__":
    main()

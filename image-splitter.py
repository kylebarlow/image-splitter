#!/usr/bin/env python3

from PIL import Image
import argparse
import sys
import math

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
                            help='desired output height (arbitrary units)')
    dimensions.add_argument('--width',
                            default=None,
                            help='desired output width (arbitrary units)')
    
    parser.add_argument('--margin',
                        default=0.5,
                        type=float,
                        help='page margin size (arbitrary units)')
    parser.add_argument('--page_height',
                        default=11.0,
                        type=float,
                        help='page size (arbitrary units)')
    parser.add_argument('--page_width',
                        default=8.5,
                        type=float,
                        help='page width (arbitrary units)')

    args = parser.parse_args()

    page_width = args.page_width
    page_height = args.page_height
    
    available_page_width = page_width - args.margin
    available_page_height = page_height - args.margin

    input_image = open_image(args.input_file)
    input_width_px, input_height_px = input_image.size
    print('Loaded image {}:'.format(args.input_file),
            input_image.format,
            "{}x{}".format(input_height_px, input_width_px),
            input_image.mode)

    if input_image.mode != 'RGB':
        print('Converting image to RGB mode')
        input_image = input_image.convert('RGB')

    # Determine output height, in inches
    if args.height:
        # Height specified via argument
        output_height_inches = float(args.height)
    else:
        # Set height based on width and image scale
        output_height_inches = float(args.width) * input_height_px/input_width_px

    # Determine output width, in inches
    if args.width:
        output_width_inches = float(args.width)
    else:
        output_width_inches = float(args.height) * input_width_px/input_height_px

    print('Output image size will be {:.1f}" high and {:.1f}" wide'.format(
            output_height_inches, output_width_inches))

    # Figure out how many pages are needed for printing
    pages_wide = math.ceil(output_width_inches / available_page_width)
    pages_high = math.ceil(output_height_inches / available_page_height)

    # Iterate through all pages that need to be made
    for num_wide_page in range(1, pages_wide+1):
        for num_high_page in range(1, pages_high+1):
            pass

    print('Saving output')
    #input_image.save('out.pdf', resolution=output_dpi)

def open_image(filename):
    try:
        return Image.open(filename)
    except IOError:
        print('Error loading input file "{}", please make sure it exists and is in a supported image format'.format(filename))
        sys.exit(1)

if __name__ == "__main__":
    main()

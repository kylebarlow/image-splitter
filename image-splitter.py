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
    
    available_page_width = page_width - 2*args.margin
    available_page_height = page_height - 2*args.margin

    input_image = open_image(args.input_file)
    input_width_px, input_height_px = input_image.size
    print('Loaded image {}:'.format(args.input_file),
            input_image.format,
            "{}x{}".format(input_height_px, input_width_px),
            input_image.mode)

    if input_image.mode != 'RGB':
        print('Converting image to RGB mode')
        input_image = input_image.convert('RGB')

    # Determine output height, in units
    if args.height:
        # Height specified via argument
        output_height = float(args.height)
    else:
        # Set height based on width and image scale
        output_height = float(args.width) * input_height_px/input_width_px

    # Determine output width, in units
    if args.width:
        output_width = float(args.width)
    else:
        output_width = float(args.height) * input_width_px/input_height_px

    print('Output image size will be {:.1f}u high and {:.1f}u wide'.format(
            output_height, output_width))

    # Create master output page image, into which the cropped parts of the original
    #  images will be pasted.
    pixels_per_units= (input_height_px / output_height) # Since we maintain scale, this
                                                        # calculation could also use width
    margin_size_px = int(args.margin * pixels_per_units)
    page_width_px = int(page_width * pixels_per_units)
    page_height_px = int(page_height * pixels_per_units)
    blank_page = Image.new('RGB', (page_width_px, page_height_px), color=(255,255,255))

    # Figure out how many pages are needed for printing
    pages_wide = math.ceil(output_width / available_page_width)
    pages_high = math.ceil(output_height / available_page_height)
    total_pages = pages_wide * pages_high

    # Iterate through all pages that need to be made
    page_count = 1
    for num_wide_page in range(1, pages_wide+1):
        # Positions in units
        unit_left_pos = (num_wide_page - 1) * available_page_width
        unit_right_pos = min(num_wide_page * available_page_width, output_width)

        # Positions as percentage of entire image
        percent_left_pos = unit_left_pos / output_width
        percent_right_pos = unit_right_pos / output_width
        
        for num_high_page in range(1, pages_high+1):
            # Positions in units
            unit_top_pos = (num_high_page - 1) * available_page_height
            unit_bottom_pos = min(num_high_page * available_page_height, output_height)

            # Positions as percentage of entire image
            percent_top_pos = unit_top_pos / output_height
            percent_bottom_pos = unit_bottom_pos / output_height

            print('Creating page {} of {}: {:.2f}%-{:.2f}% of image width by {:.2f}%-{:.2f}% of image height'.format(
                    page_count, total_pages,
                    percent_left_pos*100, percent_right_pos*100,
                    percent_top_pos*100, percent_bottom_pos*100))

            ### Crop out this page's portion of image ###
            ## Calculate region to crop, in pixels ##
            px_left = int(percent_left_pos * input_width_px)
            px_upper = int(percent_top_pos * input_height_px)
            px_right = int(percent_right_pos * input_width_px)
            px_lower = int(percent_bottom_pos * input_height_px)

            # Check to see if left matches right or top matches bottom
            # Seems like this would only happen in cases where you would put a 1-pixel wide
            # or tall image on a page, which we are avoiding
            if (px_left == px_right) or (px_upper == px_lower):
                print('\nParameters are creating too few pixels per page - use a larger image or smaller output size')
                sys.exit(1)

            box = (px_left, px_upper, px_right, px_lower)

            # Paste cropped image section into new page image
            page = blank_page.copy()
            region = input_image.crop(box)
            paste_box = (margin_size_px, margin_size_px,
                         margin_size_px + px_right - px_left,
                         margin_size_px + px_lower - px_upper)
            page.paste(region, paste_box)

            page.save('pageout_{}.pdf'.format(page_count))

            page_count += 1

def open_image(filename):
    try:
        return Image.open(filename)
    except IOError:
        print('Error loading input file "{}", please make sure it exists and is in a supported image format'.format(filename))
        sys.exit(1)

if __name__ == "__main__":
    main()

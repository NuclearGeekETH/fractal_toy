import argparse
import json

from colors.rgba_range import RGBARange
from fractal_lib import FractalLib

from colors.simple import Simple
from colors.black_and_white import BlackAndWhite
from colors.hue_range import HueRange
from colors.hue_cyclic import HueCyclic
from colors.rgba_cyclic import RGBACyclic

from animations.first_hue_rotation import FirstHueRotation
from animations.second_hue_rotation import SecondHueRotation
from animations.hue_cycle import HueCycle
from animations.random_julia import RandomJulia
from animations.random_cubic_julia import RandomCubicJulia
from animations.random_phoenix_julia import RandomPhoenixJulia
from animations.random_quartic_julia import RandomQuarticJulia
from animations.random_walk_julia import RandomWalkJulia
from animations.julia_searching_walk import JuliaSearchingWalk


def setup_fractal(args):
    class_name = FractalLib.fractal_mapping[args.fractal_algorithm]
    module = __import__("fractals.{alg}".format(alg=args.fractal_algorithm), fromlist=[class_name])
    class_ = getattr(module, class_name)
    instance = class_()
    return instance


def setup_fractal_color_scheme(fractal, args):
    color = None
    if args.color_algorithm == "simple":
        color = Simple()
        fractal.set_color_algorithm_name(args.color_algorithm)
    elif args.color_algorithm == "black_and_white":
        color = BlackAndWhite()
        fractal.set_color_algorithm_name(args.color_algorithm)
    elif args.color_algorithm == "hue_range":
        color = HueRange()
        if args.hue_start_degree is not None:
            color.set_start_degree(args.hue_start_degree)
        if args.hue_end_degree is not None:
            color.set_end_degree(args.hue_end_degree)
        fractal.set_color_algorithm_name("{}-{}-{}".format(args.color_algorithm, color.start_degree, color.end_degree))
    elif args.color_algorithm == "hue_cyclic":
        color = HueCyclic()
        if args.hue_start_degree is not None:
            color.set_start_degree(args.hue_start_degree)
        if args.hue_step_shift:
            color.set_color_step_shift(args.hue_step_shift)
        if args.color_count:
            color.set_color_count(args.color_count)

        fractal.set_color_algorithm_name("{}-{}-{}-{}".format(
            args.color_algorithm, color.start_degree, color.color_step_shift, color.color_count))
    elif args.color_algorithm == "rgba_range":
        color = RGBARange()
        if args.rgba_start_color is not None:
            color.set_start_color(args.rgba_start_color)
        if args.rgba_end_color is not None:
            color.set_end_color(args.rgba_end_color)
        if args.color_count:
            color.set_color_count(args.color_count)
        fractal.set_color_algorithm_name("{}-{}-{}-{}".format(args.color_algorithm, color.start_color, color.end_color, color.color_count))
    elif args.color_algorithm == "rgba_cyclic":
        color = RGBACyclic()
        if args.rgba_start_color is not None:
            color.set_start_color(args.rgba_start_color)
        if args.rgba_color_step_shift:
            color.set_color_step_shift(args.rgba_color_step_shift)

        if args.color_count:
            color.set_color_count(args.color_count)

        fractal.set_color_algorithm_name("{}-{}-{}-{}".format(
            args.color_algorithm, color.start_color, color.color_step_shift, color.color_count))
    fractal.set_color_algorithm(color)
    return fractal


def setup_fractal_viewport(fractal, args):
    if args.viewport_left is not None:
        fractal.set_viewport_left(args.viewport_left)
    if args.viewport_right is not None:
        fractal.set_viewport_right(args.viewport_right)
    if args.viewport_top is not None:
        fractal.set_viewport_top(args.viewport_top)
    if args.viewport_bottom is not None:
        fractal.set_viewport_bottom(args.viewport_bottom)
    return fractal


def setup_fractal_animation(fractal, args):
    animation = None
    if args.fractal_animation == "first_hue_rotation" or args.fractal_animation == "second_hue_rotation":
        if args.fractal_animation == "first_hue_rotation":
            if args.color_algorithm != "hue_range":
                raise Exception('only hue_range should be used for this animation')
            animation = FirstHueRotation()

        elif args.fractal_animation == "second_hue_rotation":
            if args.color_algorithm != "hue_range":
                raise Exception('only hue_range should be used for this animation')
            animation = SecondHueRotation()
    elif args.fractal_animation == "hue_cycle":
        if args.color_algorithm != "hue_cyclic":
            raise Exception('only hue_cyclic should be used for this animation')
        animation = HueCycle()

    elif args.fractal_animation == "random_julia":
        animation = RandomJulia()
    elif args.fractal_animation == "random_cubic_julia":
        animation = RandomCubicJulia()
    elif args.fractal_animation == "random_phoenix_julia":
        animation = RandomPhoenixJulia()
    elif args.fractal_animation == "random_quartic_julia":
        animation = RandomQuarticJulia()
    elif args.fractal_animation == "random_walk_julia":
        animation = RandomWalkJulia()
    elif args.fractal_animation == "julia_searching_walk":
        animation = JuliaSearchingWalk()
    else:
        fractal.set_show_progress_bar(False)

    if args.increments:
        animation.set_increments(args.increments)

    if args.frames_per_second:
        animation.set_frames_per_second(args.frames_per_second)

    if args.file_type:
        animation.set_file_type(args.file_type)

    # if it is an animation then set the filename for the output animation
    if args.filename is not None:
        animation.set_filename(args.filename)
    if args.animation_directory is not None:
        animation.set_directory(args.animation_directory)

    animation.set_fractal(fractal)
    return animation


def main(args):
    fractal = setup_fractal(args)
    fractal = setup_fractal_viewport(fractal, args)

    if args.width is not None:
        fractal.set_width(args.width)
    if args.height is not None:
        fractal.set_height(args.height)
    if args.real_constant is not None:
        fractal.set_real_constant(args.real_constant)
    if args.imaginary_constant is not None:
        fractal.set_imaginary_constant(args.imaginary_constant)
    if args.precision is not None:
        fractal.set_precision(args.precision)
    if args.image_filtering is not None:
        fractal.set_image_filtering(args.image_filtering)

    # needs to be done after the setting of precision so the precision can be used in color calculations
    fractal = setup_fractal_color_scheme(fractal, args)

    if args.fractal_animation is not None:
        animation = setup_fractal_animation(fractal, args)
        animation.animate()
    else:
        # if we are just generating an image then set the filename for the output image
        if args.filename is not None:
            fractal.set_filename(args.filename)
        fractal.render()


def add_arguments_to_parser(parser):
    parser.add_argument('-f', '--filename', type=str, help='do not include file extension')
    parser.add_argument('-a', '--fractal_algorithm', default="mandelbrot", type=str,
                        choices=['mandelbrot', 'julia', 'burning_ship', 'star', 'newton', 'phoenix_mandelbrot',
                                 'phoenix_julia', 'cubic_mandelbrot', 'quartic_mandelbrot', 'cubic_julia',
                                 'experimental_cubic_julia', 'quartic_julia', 'buddhabrot', 'buddhabrot_julia'])
    parser.add_argument('-c', '--color_algorithm', default="simple", type=str,
                        choices=['simple', 'black_and_white', 'hue_range', 'hue_cyclic', 'rgba_cyclic', 'rgba_range'])
    parser.add_argument('-W', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-vl', '--viewport_left', type=float,
                        help='coordinate of left edge of view port')
    parser.add_argument('-vr', '--viewport_right', type=float,
                        help='coordinate of right edge of view port')
    parser.add_argument('-vt', '--viewport_top', type=float,
                        help='coordinate of top edge of view port')
    parser.add_argument('-vb', '--viewport_bottom', type=float,
                        help='coordinate of bottom edge of view port')
    parser.add_argument('-cr', '--real_constant', type=float,
                        help='only useful for julia set based fractals')
    parser.add_argument('-ci', '--imaginary_constant', type=float,
                        help='only useful for julia set based fractals')
    parser.add_argument('-p', '--precision', type=int)
    parser.add_argument('-hs', '--hue_start_degree', type=int,
                        help='use to define hue range for hue_range amd hue_cyclic color algorithms')
    parser.add_argument('-he', '--hue_end_degree', type=int,
                        help='use to define hue range for hue_range color algorithm')
    parser.add_argument('-hss', '--hue_step_shift', type=int,
                        help='use to define hue steps to take in the cyclic hue color algorithm')

    parser.add_argument('-rgbas', '--rgba_start_color', type=json.loads,
                        help='use to define starting RGBA color for the rbga_cyclic and rgba_range color algorithms, expects json in format \'{"red": 6, "green": 190, "blue": 78, "alpha": 255}\'')
    parser.add_argument('-rgbae', '--rgba_end_color', type=json.loads,
                        help='use to define hue range for rgba_range color algorithm, expects json dict in format \'{"red": 6, "green": 190, "blue": 78, "alpha": 255}\'')
    parser.add_argument('-rgbass', '--rgba_color_step_shift', type=json.loads,
                        help='use to define hue steps to take in the cyclic RGBA color algorithm, expects json in format \'{"red": 6, "green": 190, "blue": 78, "alpha": 255}\'')

    parser.add_argument('-cc', '--color_count', type=int,
                        help='use to define the number of colors to cycle through in the cyclic color algorithms')

    # image filtering
    parser.add_argument('-if', '--image_filtering', default="none", type=str,
                        choices=['none', 'basic', 'glow_takeover', 'additive_glow', 'blur'])

    # animation variables
    parser.add_argument('-A', '--fractal_animation', type=str, help='int to select animation',
                        choices=['first_hue_rotation', 'second_hue_rotation', 'hue_cycle', 'random_julia',
                                 'random_cubic_julia', 'random_phoenix_julia', 'random_quartic_julia',
                                 'random_walk_julia', 'julia_searching_walk'])
    parser.add_argument('-i', '--increments', default=40, type=int,
                        help='number of increments in the animation, this may end up being doubled in looping animations')
    parser.add_argument('-ft', '--file_type', default='gif', type=str, help="the file type of the animation output",
                        choices=['gif', 'avi'])
    parser.add_argument('-ad', '--animation_directory', type=str, help="the directory to use to store the images in the animation")
    parser.add_argument('-fps', '--frames_per_second', default=30, type=int,
                        help="frames per second for video output, defaults to 30")
    # parser.add_argument('-cl', '--constant_left', type=float)
    # parser.add_argument('-cr', '--constant_right', type=float)
    # parser.add_argument('-ct', '--constant_top', type=float)
    # parser.add_argument('-cb', '--constant_bottom', type=float)
    # parser.add_argument('-t', '--traversal', type=str,
    #                    choices=['diagonal', 'spiral'])
    return parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser = add_arguments_to_parser(parser)
    arguments = parser.parse_args()
    main(arguments)

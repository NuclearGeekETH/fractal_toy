from __future__ import division
from progressbar import ProgressBar
from imageio import mimsave, imread
from animations.animation import Animation
from fractals.cubic_julia import CubicJulia
from fractals.cubic_mandelbrot import CubicMandelbrot
import numpy as np
import copy
import random

__author__ = 'guydmann'


class RandomQuarticJulia(Animation):
    animation_name = "random_quartic_julia"

    def animate(self):
        self.preprocess()

        fractal_backup = copy.deepcopy(self.fractal)

        self.fractal = CubicMandelbrot()
        self.fractal.set_directory(fractal_backup.directory)
        self.fractal.set_color_algorithm_name(fractal_backup.color_algorithm_name)
        self.fractal.set_color_algorithm(fractal_backup.color_algorithm)

        self.fractal.set_width(fractal_backup.width)
        self.fractal.set_height(fractal_backup.height)
        self.fractal.set_precision(fractal_backup.precision)

        calc_pbar = ProgressBar(maxval=self.increments*2)
        print("Generating Quartic Mandelbrot Set")
        self.fractal.set_bypass_image_generation(True)
        self.render_fractal()

        random_x = random.randint(0, self.fractal.width-1)
        random_y = random.randint(0, self.fractal.height-1)
        print("Searching for Starting Point")
        while not (self.fractal.precision > self.fractal.fractal_array[random_x][random_y] > (self.fractal.precision * 0.98)):
            random_x = random.randint(0, self.fractal.width-1)
            random_y = random.randint(0, self.fractal.height-1)
        print("the Mandelbrot Value is {val}".format(val=self.fractal.fractal_array[random_x][random_y]))

        x = np.linspace(self.fractal.viewport['left_x'], self.fractal.viewport['right_x'], self.fractal.width)[random_x]
        y = np.linspace(self.fractal.viewport['bottom_y'], self.fractal.viewport['top_y'], self.fractal.height)[random_y]

        print("Creating Fractal Images")
        calc_pbar.start()
        results = []

        self.fractal = CubicJulia()
        self.fractal.set_directory(fractal_backup.directory)
        self.fractal.set_color_algorithm_name(fractal_backup.color_algorithm_name)
        self.fractal.set_color_algorithm(fractal_backup.color_algorithm)

        self.fractal.set_width(fractal_backup.width)
        self.fractal.set_height(fractal_backup.height)
        self.fractal.set_precision(fractal_backup.precision)

        self.fractal.set_real_constant(x)
        self.fractal.set_imaginary_constant(y)

        for k in range(self.increments):

            self.fractal.set_filename("{}{}_{}_forward".format(self.fractal.directory,
                                                             self.animation_name,
                                                             k))
            results.append(self.render_fractal())
            calc_pbar.update(k)
            self.fractal.set_real_constant(x - (k*((x/60)/self.increments)))
            self.fractal.set_imaginary_constant(y - (k*((y/60)/self.increments)))

        for k in range(self.increments):

            self.fractal.set_filename("{}{}_{}_backward".format(self.fractal.directory,
                                                             self.animation_name,
                                                             k))
            results.append(self.render_fractal())
            calc_pbar.update(self.increments+k)
            self.fractal.set_real_constant(x + (k*((x/60)/self.increments)) - (x/60))
            self.fractal.set_imaginary_constant(y + (k*((y/60)/self.increments)) - (y/60))

        calc_pbar.finish()

        for image_file in results:
            self.images.append(imread(image_file))

        mimsave("{}.gif".format(self.filename), self.images)
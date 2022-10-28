import datetime
import cv2
import numpy as np
from fractal_lib import FractalLib
from os import mkdir, path
from imageio import mimsave, imread


class Animation(object):
    fractal = None
    filename = None
    file_type = None
    animation_name = None
    increments = None
    directory = ""
    frames_per_second = 30
    file_type = 'gif'
    video_filters = ["bilateral_filter"]

    def animate(self):
        self.preprocess()
        image_file_list = self.generate_images()
        self.filename = self.save(image_file_list)

    def generate_images(self):
        raise NotImplemented

    def save(self, image_files):

        if self.file_type == "gif":
            images = []
            for image_file in image_files:
                images.append(imread(image_file))
            output_filename = "{}.gif".format(self.filename)
            mimsave(output_filename, images)
        elif self.file_type == "avi":

            frame = cv2.imread(image_files[0])
            output_filename = "{}.avi".format(self.filename)
            height, width, layers = frame.shape

            fourcc = cv2.VideoWriter_fourcc(*'H264') # 'm','p','4','v')
            video = cv2.VideoWriter(output_filename, fourcc, self.frames_per_second, (width, height))

            for image in image_files:
                original_image = cv2.imread(image)
                video.write(original_image)
            video.release()
            cv2.destroyAllWindows()
        return output_filename

    def set_fractal(self, new_fractal):
        self.fractal = new_fractal

    def set_directory(self, new_directory):
        self.directory = new_directory

    def set_filename(self, new_filename):
        self.filename = new_filename

    def set_increments(self, new_increments):
        self.increments = new_increments

    def set_frames_per_second(self, new_fps):
        self.frames_per_second = new_fps

    def set_file_type(self, new_file_type):
        self.file_type = new_file_type

    def set_color_multiplier(self, new_color_multiplier):
        raise NotImplemented

    def preprocess(self):
        if self.directory:
            self.fractal.directory = self.directory
        else:
            self.fractal.directory = self.animation_name
        if not self.fractal.preprocessed:
            self.fractal.preprocess()

        if self.filename is None:
            i = datetime.datetime.now()
            if self.fractal.directory is not None:
                self.directory = "{}/".format(self.fractal.directory)
            else:
                self.directory = ""
            self.set_filename("{}{}_{}_{}_h{}_w{}_{}".format(self.fractal.directory,
                                                                 self.animation_name,
                                                                 self.fractal.fractal_name,
                                                                 self.fractal.color_algorithm_name,
                                                                 self.fractal.height,
                                                                 self.fractal.width,
                                                                 i.isoformat().replace(":","")))

        FractalLib.empty_dir_and_remove("{}".format(self.fractal.directory))
        mkdir("{}".format(self.fractal.directory))
        self.verify_data_postprocessing()

    def verify_data_postprocessing(self):
        if self.fractal is None:
            raise Exception("fractal not set")
        if self.filename is None:
            raise Exception("filename not set")

    def render_fractal(self):
        return self.fractal.render()

from pathlib import Path
from time import sleep
from PIL import Image
from PIL.ImageStat import Stat
from pyscreenshot import grab
from json import JSONEncoder
from shrun import shrun
from subprocess import Popen, PIPE
import os
from re import compile, match
import time
class BBox:
    """Represents a bounding box on the screen
Holds pixel coordinates and the file path for the displayed image in the region within the coordinates
"""

    EMPTY_CLICK_COOR = (401, 9)
    EMPTY_CLICK_ENABLED = True

    SLEEP_VAL = 0.5
    """Sleep time elapsed while checking whether the image is displayed on the screen
Used by compare() method"""

    __SAVE_DIR = Path(os.getcwd())
    """Directory path for the directory that contains images and the pixel coordinates of images"""

    __COORDINATES_PATH = __SAVE_DIR.joinpath("bboxes.py")
    """File path for the file that contains pixel coordinates of images"""

    IMAGE_EXT = ".png"
    """Image extension for saved images"""

    def __init__(self, name, tl_point, br_point, click_point):
        self.name = name
        self.tl_point = (int(tl_point[0]), int(tl_point[1]))
        self.br_point = (int(br_point[0]), int(br_point[1]))
        self.click_point = (int(click_point[0]), int(click_point[1]))
        self.image = None

    @classmethod
    def set_save_dir(cls, path):
        cls.__SAVE_DIR = Path(path)
        cls.__COORDINATES_PATH = cls.__SAVE_DIR.joinpath("bboxes.py")

    @classmethod
    def get_save_dir(cls):
        return cls.__SAVE_DIR

    def __save(self, file):
        template_string = "{} = BBox('{}', ({}, {}), ({}, {}), ({}, {}))"
        print(template_string.format(
            self.name,
            self.name,
            self.tl_point[0],
            self.tl_point[1],
            self.br_point[0],
            self.br_point[1],
            self.click_point[0],
            self.click_point[1]), file=file)

    @classmethod
    def __read(cls, file):
        regex = "^(?P<name>\w+) = BBox\('\w+', \((?P<tl0>\d+), (?P<tl1>\d+)\), \((?P<br0>\d+), (?P<br1>\d+)\), \((?P<cp0>\d+), (?P<cp1>\d+)\)\)"
        line = file.readline()
        result = match(regex, line)
        if not result:
            return None
        else:
            return BBox(
                result.group('name'), (result.group('tl0'), result.group('tl1')),   \
                                        (result.group('br0'), result.group('br1')), \
                                        (result.group('cp0'), result.group('cp1')))

    def __generate_image_path(self):
        return self.__SAVE_DIR.joinpath(self.name + BBox.IMAGE_EXT)

    def add(self):
        file = open(self.__COORDINATES_PATH, mode='a')
        self.__save(file)

    @classmethod
    def remove(cls, name):
        os.remove(cls.__SAVE_DIR.joinpath(name + BBox.IMAGE_EXT))
        bboxes = BBox.readAll()
        for key in bboxes:
	        if bboxes[key].name == name:
		        bboxes.pop(key)
		        break
        BBox.writeAll(bboxes)

    @classmethod
    def writeAll(cls, bboxes):
        with open(cls.__COORDINATES_PATH, mode='w') as file:
            print('from bbox import BBox', file=file)
            for bbox in bboxes.values():
                bbox.__save(file)
        
    @classmethod
    def readAll(cls):
        loaded_objects = {}
        with open(cls.__COORDINATES_PATH) as coordinates_file:
        # read import line
            coordinates_file.readline()
            while True:
                bbox = BBox.__read(coordinates_file)
                if bbox:
                    loaded_objects[bbox.name] = bbox
                else:
                    return loaded_objects

    def capture(self):
        image = grab(bbox=(self.tl_point[0], self.tl_point[1], self.br_point[0], self.br_point[1]))
        image.save(self.__generate_image_path())
        self.add()

    def compare(self):
        ''' Compare the image in the sceen is the same as saved image'''
        # start_time = time.time()
        if not self.image:
            self.image = Image.open(self.__generate_image_path())
        current_image = grab(bbox=(self.tl_point[0], self.tl_point[1], self.br_point[0], self.br_point[1]))
        result = (Stat(current_image).sum == Stat(self.image).sum)
        # end_time = time.time()
        # print("comparing {} took {}".format(self.name, str(end_time - start_time)))
        self.empty_click()
        return result

    @classmethod
    def empty_click(cls):
        if cls.EMPTY_CLICK_ENABLED:
            shrun('xdotool mousemove --sync {} {}'.format(cls.EMPTY_CLICK_COOR[0], cls.EMPTY_CLICK_COOR[1]))
            shrun('xdotool click 1')
            shrun('xdotool mousemove --sync 0 0')

    def wait(self):
        ''' Wait until the image in the sceen is the same as saved image'''
        while True:
            if self.compare():
                print("{} appeared".format(self.name))
                return
            print("Waiting {} to appear".format(self.name))
            self.empty_click()
            sleep(self.SLEEP_VAL)

    def click(self):
        print("Clicking to {}".format(self.name))
        shrun('xdotool mousemove --sync {} {}'.format(self.click_point[0], self.click_point[1]))
        shrun('xdotool click 1')
        shrun('xdotool mousemove --sync 0 0')
        # sleep(self.SLEEP_VAL)

    def waitAndClick(self):
        self.wait()
        self.click()

    def compareAndClick(self):
        if self.compare():
            self.click()
from lxml import etree as ET
from xml.dom.minidom import parse
import cv2
from PIL import Image
import numpy as np


class Annotate:
    ### annotate an image based on pascal voc annotation xml
    def __init__(self, annotation_file, class_mapping={}, save_folder=None):
        self.annotation_file = annotation_file if isinstance(annotation_file, list) else [annotation_file]
        self.class_mapping=class_mapping
        self.n_classes = len(class_mapping.keys())
        self.save_folder=save_folder

    def get_objects(self, a_file):
        _doc = parse('{filename}'.format(filename=a_file))
        objects = _doc.getElementsByTagName("object")
        img_file = _doc.getElementsByTagName('path')[0].firstChild.nodeValue

        obj_key = {
                    'filename': img_file,
                    'labels':[]
                }
        for obj in objects:
            label = obj.getElementsByTagName('name')[0].firstChild.nodeValue
            if label in self.class_mapping:
                x_min = obj.getElementsByTagName('xmin')[0].firstChild.nodeValue
                y_min = obj.getElementsByTagName('ymin')[0].firstChild.nodeValue
                x_max = obj.getElementsByTagName('xmax')[0].firstChild.nodeValue
                y_max = obj.getElementsByTagName('ymax')[0].firstChild.nodeValue

                obj_key['labels'].append({'label':self.class_mapping[label],
                                            'x_min':int(x_min),
                                            'y_min':int(y_min),
                                            'x_max':int(x_max),
                                            'y_max':int(y_max),
                                            })
        return obj_key

    def __open_image(self, filename ):
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img

    def __label_pixles(self, img, labels, background_rgb=(255,255,255)):

        png_file = np.zeros((img.size[0],img.size[1],3)).astype('uint8')
        for lbl in labels:

            for x in range(lbl['x_min'], lbl['x_max']):
                for y in range(lbl['y_min'], lbl['y_max']):
                    r,g,b = img.getpixel((x, y))
                    if r==background_rgb[0] and g==background_rgb[1] and b==background_rgb[2]:
                        #set whitespace as background
                        png_file[x,y] = 0
                    else:
                        #nonwhite space as class_label
                        png_file[x,y] = lbl['label']
        return png_file

    def label_image(self, obj_key):
        img = self.__open_image(obj_key['filename'])
        png_file = self.__label_pixles(img, obj_key['labels'])

        if self.save_folder:
            print(obj_key['filename'])
            _filename = obj_key['filename'].replace('\\','/')
            filename = self.save_folder + _filename[_filename.rindex('/'):]


        filename = filename.replace('.jpg', '.png')
        cv2.imwrite(filename, png_file)

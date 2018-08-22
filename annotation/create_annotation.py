import argparse
import os
from annotate import Annotate
from construct_mapper import get_mapper

##create labeled image in .png format based on annotation xml that is in pascal VOC format
parser = argparse.ArgumentParser()
parser.add_argument("--classes_file", type = str , default = 'classes.yaml' )
parser.add_argument("--annotation_dir", type = str, default = None)
parser.add_argument("--output_dir", type = str, default = 'output/')
parser.add_argument("--image_file", type=str, default = None )

args = parser.parse_args()
classes_file=args.classes_file
annotation_dir=args.annotation_dir
output_dir = args.output_dir
image_file = args.image_file

mapper = get_mapper(classes_file)

files=[]
if image_file:
    files.append(image_file)
else:
    for f in os.listdir(annotation_dir):
        if annotation_dir[:-1] =='/':
            files.append(annotation_dir+f)
        else:
            files.append(annotation_dir + '/' + f)

if output_dir:
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

a = Annotate(files, mapper, save_folder=output_dir)

#annotation_file is always turned into a list
for f in a.annotation_file:
    obj_key = a.get_objects(f)
    # image labels generated
    a.label_image(obj_key)

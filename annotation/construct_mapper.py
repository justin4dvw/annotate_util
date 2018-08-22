from util4d import *
import yaml

def get_mapper(classes_file='classes.yaml'):
    mapping_file = load_mapping(classes_file)

    classes=1
    mapper= {}
    for each in mapping_file['classes']:
        mapper[each] = classes
        classes+=1

    return mapper

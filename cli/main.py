# %%
import os, os.path
import json
import shutil
from PIL import Image

# Local packages/modules
from utils.image import compose_focus_effect,save_animation, save_versions, save_image
from utils.data import load_json

from utils.runtime import start_counter, end_counter

STATIC_DIR = 'static'

STATIC_IMAGES_DIR = 'static/images'
INPUT_JSON_PATH = f'{STATIC_DIR}/output.json'

STATIC_OUTPUT_DIR = 'static/output_compressed'
STATIC_OUTPUT_DIR = f'{os.getcwd()}/static/output_compressed'

if os.path.exists(STATIC_OUTPUT_DIR):
	shutil.rmtree(STATIC_OUTPUT_DIR)
	os.makedirs(STATIC_OUTPUT_DIR)
else:
	os.makedirs(STATIC_OUTPUT_DIR)


# loop over input iamges and create compressed images

imgs = []
VALIDE_IMAGES = ['.jpg','.gif','.png','.tga']

for f in os.listdir(STATIC_IMAGES_DIR):
    ext = os.path.splitext(f)[1]

    if ext.lower() not in VALIDE_IMAGES:
        continue
    imgs.append(os.path.join(STATIC_IMAGES_DIR,f))



# linear searching slow but does the job for now
def find_image(images_data, filename):
	for image in images_data:
		if image['file'] == filename:
			return image

def split_xy_float_arr(data, flip=False):
	arr_x = []
	arr_y = []

	if flip:
		for index, coord in enumerate(data):
			if (index % 2 == 0):
				# print(index)
				arr_x.append(1 - coord)
			else:
				arr_y.append(coord)
				# arr_y.append(1 - coord)
	else:
		for index, coord in enumerate(data):
			if (index % 2 == 0):
				arr_x.append(coord)
			else:
				arr_y.append(coord)

	return [arr_x, arr_y]


def get_min_max(arr):
	return [min(arr), max(arr)]

# Original dimension (d_)
# Normalized [0, 1] of xy min max (_x, _y)
def get_norm_to_dimensions(d_width, d_height, n_x, n_y):
	BIGGER = 1.16
	SMALLER = 0.94

	d_x = [d_width * (n_x[0] * SMALLER), d_width * (n_x[1] * BIGGER)]
	d_y = [d_height * (n_y[0] * SMALLER), d_height * (n_y[1] * BIGGER)]
	box_width = d_x[1] - d_x[0]
	box_height = d_y[1] - d_y[0]


	return {
		# 'top': d_y[0],
		# 'bottom': d_y[1],
		# 'left': d_x[0],
		# 'right': d_x[1],
		# 'width': box_width,
		# 'height': box_height
		'top': d_y[0] * SMALLER,
		'bottom': d_y[1],
		'left': d_x[0] * SMALLER,
		'right': d_x[1],
		'width': box_width,
		'height': box_height
	}



# %%
def handle_compression():
	json_data = load_json(INPUT_JSON_PATH)
	
	for index, file_path in enumerate(imgs):
		filename = file_path.split('/')[2]

		img = Image.open(file_path)
		(width, height) = img.size

		current_image = find_image(json_data, filename)

		(x_arr, y_arr) = split_xy_float_arr(current_image['landmarks'], True)
		x_min_max_norm = get_min_max(x_arr)
		y_min_max_norm = get_min_max(y_arr)


		bbox = get_norm_to_dimensions(d_width=width, d_height=height, n_x=x_min_max_norm, n_y=y_min_max_norm)

		
		requiredBoxData = [
			bbox['left'],
			bbox['top'],
			bbox['width'],
			bbox['height']
		]

		# print(bbox)

		settings = {
			"final": False,
			"speeds": [1],
			"steps": 10,
			"distances": [1],
			"showBorders": False,
			"width": None,
			"boxes": [requiredBoxData],
		}

		destination = f'{STATIC_OUTPUT_DIR}'
		
		if not os.path.exists(destination):
			os.makedirs(destination)

		source, background, composition, frames = compose_focus_effect(img, settings)

		# save_animation(source, background, frames, f'{destination}/animated')
		# save_versions(source, composition, destination)
		save_image(filename, composition, destination)


start_counter(handle_compression)

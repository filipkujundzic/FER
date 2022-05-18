import argparse
from pathlib import Path
import re
from textwrap import dedent
import sys

import numpy as np

K1_TABLE = (
    (16, 11, 10, 16, 24, 40, 51, 61),
    (12, 12, 14, 19, 26, 58, 60, 55),
    (14, 13, 16, 24, 40, 57, 69, 56),
    (14, 17, 22, 29, 51, 87, 80, 62),
    (18, 22, 37, 56, 68, 109, 103, 77),
    (24, 35, 55, 64, 81, 104, 113, 92),
    (49, 64, 78, 87, 103, 121, 120, 101),
    (72, 92, 95, 98, 112, 100, 103, 99),
)

K2_TABLE = (
    (17, 18, 24, 47, 99, 99, 99, 99),
    (18, 21, 26, 66, 99, 99, 99, 99),
    (24, 26, 56, 99, 99, 99, 99, 99),
    (47, 66, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
)

def rgb_to_ycbcr(
	image_data,
	y_coef = (0.299, 0.587, 0.114),               #default y coefficients
	cb_coef = (-0.1687, -0.3313, 0.5),			 #default cb coefficients
	cr_coef = (0.5, -0.4187, -0.0813),			 #default cr coefficients
	y_addition = 0,									 #default y addition
	cb_addition = 128,								 #default cb addition
	cr_addition = 128,									 #default cr addition
):

	y_coef, cb_coef, cr_coef = (np.array(x) for x in (y_coef, cb_coef, cr_coef))


	return np.array(
		[
			[
				[
					y_coef @ pixel + y_addition,
					cb_coef @ pixel + cb_addition,
					cr_coef @ pixel + cr_addition,
				]
				for pixel in row	
			]
			for row in data
		]
	)

def shift_pixels(data: np.ndarray, constant = -128):
	return data + np.full(data.shape, constant)

def divide_to_blocks(data, width = 8, height = 8):
	result = list()
	for height_offset in range(0, data.shape[0] - height + 1, height):
		row = list()

		for width_offset in range(0, data.shape[1] - width + 1, width):
			row.append(data[height_offset : height_offset + height, width_offset : width_offset + width])

		result.append(row)

	return np.array(result)

def dct_2d(data) -> np.ndarray:
	result = list()

	for i in range(8):
		row = list()

		for j in range(8):
			coef = 0.5 if (i == 0 or j == 0) else 1
			coef /= 4
			i_coef = i * np.pi / 16
			j_coef = j * np.pi / 16
			current = np.zeros(data[0][0].shape, dtype = np.float64)

			for k, block_row in enumerate(data):
				for l, pixel in enumerate(block_row):
					current += (pixel * np.cos((2 * k + 1) * i_coef) * np.cos((2 * l + 1) * j_coef)) 

			row.append(coef * current)
		result.append(row)

	return np.array(result)

def get_quantization_const(y = K1_TABLE, cb = K2_TABLE, cr = K2_TABLE):
	return np.stack([y,cb,cr]).transpose((1, 2, 0))

def quantize_block(data, constant):
	return np.rint(data / constant).astype(int)

def zigzag_array(array_input):
	return np.concatenate(
		[
			np.diagonal(array_input[::-1, :],k)[:: (2 * (k * 2) - 1)]
			for k in range(1 - array_input.shape[0], array_input.shape[0])
		]
	)

picture = sys.argv[1]
block_index = sys.argv[2]
output_file = sys.argv[3]

# ucitaj sliku
with open(picture, mode = "rb") as f:
	fileType = f.readline().decode("utf8").strip()
	dimensions= f.readline().decode("utf8").strip()
	p = dimensions.split()
	width = int(p[0])
	height = int(p[1])
	
	value = int(f.readline().decode("utf8").strip())

	bytes_per_colour = 1 if value < 256 else 2
	bytes_per_pixel = 3 * bytes_per_colour

	read = f.read()
	rows = [
		read[i : i + (width * bytes_per_pixel)]
		for i in range(0, len(read), width * bytes_per_pixel)
	]

	pixels = [
		[
			[int(element) for element in row[i : i + bytes_per_pixel]]
			for i in range(0, len(row), bytes_per_pixel)
		]
		for row in rows
	]

	data = np.array(pixels, dtype = np.uint8 if bytes_per_colour == 1 else np.uint16)

#konverzija iz RGB u YCbCr
ycbcr_image = rgb_to_ycbcr(data)
#pomak
ycbcr_shifted = shift_pixels(ycbcr_image, -128)
#podijeli u blokove
blocks = divide_to_blocks(ycbcr_shifted)

wanted_block = blocks[int(block_index) // blocks.shape[0]][int(block_index) % blocks.shape[0]]

#2D-DCT
dct = dct_2d(wanted_block)

#kvantizacija
quantization_const = get_quantization_const()
quantized_block = quantize_block(dct, quantization_const)

block_print = quantized_block.transpose(2, 0, 1)

zigzag_block = np.array([zigzag_array(x) for x in block_print])

with open(output_file, mode = "w+", encoding = "ascii") as file:
	for i in range(0,3):
		for j in range(0,8):
			for k in range(0,8):
				file.write(str(block_print[i][j][k]) + " ")
			file.write("\n")
		file.write("\n")
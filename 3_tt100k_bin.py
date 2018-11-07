# this is the .py file used to generate the binary file in cifar10 format. 
# <1byte_label><3072bytes_RGB_data>, and the images RGB data should follow the R => G => B row-major order.
# Note that, we also need to single classification result, and the single_test_bin() function could help...

import pickle 
import os 
import cv2
import numpy as np

top_fre = 46        # the setting of tt100k..., it determines how many top_frequent classes we will use.

img_add = ""        # the path to find the image data.
lab_add = ""        # the path to find the label data.
training_bin = ""
testing_bin = ""
single_test_path = ""
# Note that the bin file don't need ".bin" suffix..

# For both Training&Testing sets generation
def bin_file(img_add = img_add, lab_add = lab_add, save_file = save_file):
	bin_file = open(save_file, 'wb')
	for num in range(0,leng):
		print "This is the {} round".format(num)
		bgr_jpg = cv2.imread(image_path + str(num) + ".jpg")
		# cv2.imshow('raw-major or column-major?', bgr_jpg)
		# cv2.waitKey(0)
		# print bgr_jpg
		# print type(bgr_jpg)   # ndarray
		# Convert the opencv image data as the required format.
		rgb_jpg = cv2.cvtColor(bgr_jpg, cv2.COLOR_BGR2RGB)
		r_data = np.uint8(np.reshape(rgb_jpg[:,:,0], [-1]))
		g_data = np.uint8(np.reshape(rgb_jpg[:,:,1], [-1]))
		b_data = np.uint8(np.reshape(rgb_jpg[:,:,2], [-1]))
		# make all the three kind of data together...
		txt = open(label_path + str(num) + ".txt", 'r').read()
		class_number = np.array(int(txt.split("_")[0]), np.uint8)
		print class_number
		# Try to write the required data with single piece of data.
		bin_file.write(class_number)
		for i in r_data:
			bin_file.write(i)
		for i in g_data:
			bin_file.write(i)
		for i in b_data:
			bin_file.write(i)
	bin_file.close()

# For single-class test...
# some commented lines for debug...
def generate_single_bin(top_fre, img_add = img_add, lab_add = lab_add, save_path = single_test_path):
	# get the class infos from the labels
	sample_num = len(os.listdir (lab_add)) # get the total file number...7706
	sample_pool = [str(i) for i in range(sample_num)] # ...7706

	for num in range(top_fre):
		# last_num = len(sample_pool)
		# print "the current sample number is {}".format(last_num)
		bin_file = open(single_test_path + str(num), 'wb')

		for item in sample_pool:
			sample_class = int(open(lab_add + item + ".txt").read().split("_")[0])
			if sample_class == num:
				rgb_jpg = cv2.cvtColor(cv2.imread(image_path + item + ".jpg"), cv2.COLOR_BGR2RGB)
				r_data = np.uint8(np.reshape(rgb_jpg[:,:,0], [-1]))
				g_data = np.uint8(np.reshape(rgb_jpg[:,:,1], [-1]))
				b_data = np.uint8(np.reshape(rgb_jpg[:,:,2], [-1]))

				bin_file.write(np.array(sample_class, dtype = np.uint8))   # write the 1st label byte
				for i in r_data:
					bin_file.write(i)
				for i in g_data:
					bin_file.write(i)
				for i in b_data:
					bin_file.write(i)
				sample_pool.remove(item)  
				# remove the item from the sample_pool in order to avoid computation resource waste

		bin_file.close()
		# current_num = len(sample_pool)
		# print "The number of cut samples is {}".format(last_num - current_num)
		# print "The current sample number is {}".format(current_num)




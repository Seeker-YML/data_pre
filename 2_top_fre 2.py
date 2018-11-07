# This .py file is used
# 1. to resize the image data
# 2. to extract the top-frequent training images&labels with their new label(new class number)
# 3. to extract the testing images&labels according to the training set...
# 4. to generate the templates of the training & testing set individually...
# Note that the items belong to the same class will be generated together (it means the they will appear one by one),
# So it's necesaary to use the shuffle machenisms during training !!! 

import os 
import cv2
import time 
import shutil

new_size = (32,32)        # Use tuple to present your ideal image size...
top_fre = 46              # Define the top_fre of the new generated data !!! 

img_add = "/Users/meiluyuan/Desktop/gt_cls_data/ori_imgs/"                  # for the original gt data
lab_add = "/Users/meiluyuan/Desktop/gt_cls_data/labels/"        
new_img_add = "/Users/meiluyuan/Desktop/gt_cls_data/re_imgs/"               # for the resized data
# new_lab_add = "/Users/meiluyuan/tt100k/labels1/"                          # whether we need a new label address ???? No  
top_fre_img_add = "/Users/meiluyuan/Desktop/gt_cls_data/top_fre/"           # addresses for the resorted top_fre img&lab data 
top_fre_lab_add = "/Users/meiluyuan/Desktop/gt_cls_data/top_fre/labels/"    # but I think I need a dir contains top_fre labels  
templates_path = "/Users/meiluyuan/Desktop/gt_cls_data/templates/"          # the dir to save the template data 
mode_list = ["train/", "test/", "other/"]


# resized imgaes and original gt images will share the label data ... 
def Resize_Img(mode_list = mode_list, img_add = img_add, lab_add = lab_add, new_img_add = new_img_add, new_size = new_size, method = cv2.INTER_CUBIC):

	if os.path.exists(new_img_add) == None:
		os.mkdir(new_img_add)

	for mode in mode_list:
		if os.path.exists(new_img_add + mode) == None:
			os.mkdir(new_img_add + mode)
		img_list = os.listdir(img_add + mode)
		for item in img_list:
			print "the current item is: ", item
			cur_img = cv2.imread(img_add + mode + item)
			print "This is the surrent image:", cur_img   # None ???
			new_img = cv2.resize(cur_img, new_size, interpolation = method)    # error here! 
			cv2.imwrite(new_img_add + mode + item, new_img)

	return 0


# Extract the top_fre resized items according to top_fre number and give them new image_ids ... 
# Generate the top_fre training&testing data at the same time ... 
# give all of them a new class label...
def top_fre(top_fre = None, least_num = None, img_add = new_img_add, top_fre_img_add = top_fre_img_add, top_fre_lab_add = top_fre_lab_add):

	
	print "============================ Train Data Collection ==========================="
	temp_add = lab_add + "train/"
	txt_list = os.listdir(temp_add)
	txt_list = sorted(txt_list, key = lambda x: int(x.split(".")[0]))
	lab_list = [ open(lab_add + "train/" + txt).read().split("_")[1] for txt in txt_list ]      # txt&label in order...
	lab_set = set(lab_list)
	print len(lab_set)
	print "The following section is the lab_set : \n", lab_set
	lab_con = [[i, lab_list.count(i)] for i in lab_set]
	sorted_lab = sorted(lab_con, key = lambda x : - x[1] )
	print "The following section is the lab_set : \n", sorted_lab

	top_fre_lab = sorted_lab
	if top_fre:
		top_fre_lab = sorted_lab[0 : top_fre]

	if least_num:
		index = 0
		while least_num <= sorted_lab[index][1] : index += 1 
		top_fre_lab = sorted_lab[0:index]

	print "The following contexts are top_fre labels : \n", top_fre_lab

	# Get the image&label at the same time.
	index = 0   # the sample index
	if os.path.exists(img_add + "train/") == None:
		os.mkdir(img_add + "train/")
	# TOP_FRE Data Collection ... 
	class_index = 0
	for one_class in top_fre_lab:
		print "The is the generation of class {} ".format(one_class)
		lab_index = 0
		for item in lab_list: 
			if item == one_class[0] :

				ori_img = img_add + "train/" + str(lab_index) + ".jpg" # the add od original img...
				des_img = top_fre_img_add + "train/" + str(index) + ".jpg" 
				shutil.copyfile(ori_img, des_img)    # copy the img file   # create the whole requirements before the execution.
				des_lab = top_fre_lab_add + "train/" + str(index) + ".txt"
				new_lab = open(des_lab,'w')
				new_lab.write(str(class_index) + "_" + item + "_" + str(lab_list.count(item)))
				new_lab.close()
				index += 1
			lab_index += 1

	class_index += 1

	print "============================ Test Data Collection ==============================="
	# regenerate the testing data ... 
	temp_add = lab_add + "test/"
	test_txt_list = os.listdir(temp_add)
	test_txt_list = sorted(test_txt_list, key = lambda x: int(x.split(".")[0]))
	print "this is the whole contexts of the test_txt_list", test_txt_list
	test_lab_list = [ open(lab_add + "test/" + txt, 'r').read().split("_")[1] for txt in test_txt_list ]   # read the label in certain order...

	index = 0
	if os.path.exists(img_add + "test/") == None:
		os.mkdir(img_add + "test/")
	class_index = 0
	for one_class in top_fre_lab:
		print "This is the generation of the class {} ".format(one_class)
		lab_index = 0 
		for item in test_lab_list:

			if item == one_class[0]:

				ori_img = img_add + "test/" + str(lab_index) + ".jpg"
				des_img = top_fre_img_add +"test/" + str(index) + ".jpg"
				shutil.copyfile(ori_img, des_img)

				des_lab = top_fre_lab_add + "test/" + str(index) + ".txt"
				new_lab = open(des_lab,'w')
				new_lab.write( str(class_index) + "_" + item + "_" + str(test_lab_list.count(item)) )
				new_lab.close()

				index += 1
			lab_index += 1
		class_index += 1

	return 0 



# Note that: the order of top_fre data for training and testing is different from each other... 
def lab_templates(top_fre = None, least_num = None, img_add = img_add, lab_add = lab_add, mode_list = mode_list, templates_path = templates_path):

	for mode in mode_list:
		print " This is the training set ... "
		temp_add = lab_add + mode
		txt_list = os.listdir(temp_add)
		txt_list = sorted(txt_list, key = lambda x: int(x.split(".")[0]))
		lab_list = [ open(lab_add + mode + txt, 'r').read().split("_")[1] for txt in txt_list ]      # txt&label in order...
		lab_set = set(lab_list)
		print len(lab_set)
		print "The following section is the lab_set : \n", lab_set
		lab_con = [[i, lab_list.count(i)] for i in lab_set]
		sorted_lab = sorted(lab_con, key = lambda x : - x[1] )
		print "The following section is the lab_set : \n", sorted_lab

		top_fre_lab = sorted_lab
		if top_fre:
			top_fre_lab = sorted_lab[0 : top_fre]

		if least_num:
			# Get the data which the times of disappearances is larger than least_num.
			index = 0
			while least_num <= sorted_lab[index][1] : index += 1 
			top_fre_lab = sorted_lab[0:index]
		print "The following contexts are top_fre labels : \n", top_fre_lab
	
		lab_1st_item = [ [i[0], str(lab_list.index(i[0]))] for i in top_fre_lab ]
		print "The following contexts are all top_fre lab_1st_item : \n", lab_1st_item
		# Maybe some errors happened in the top_fre = 45 data generation section is after the top_fre_lab extraction...

		class_index = 0
		print "Let's start the lab_1st_item: \n"
		for i in lab_1st_item:
			print i   
			ori_img = img_add + mode + i[1] + ".jpg"
			# /home/yuanmeilu/re_tt100k/images/train
			print ori_img
			des_img =  templates_path + mode + str(class_index) + "_" + i[0] + "_" + str(lab_list.count(i[0])) + ".jpg"
			print des_img
			shutil.copyfile(ori_img, des_img)    # error! ???
			class_index += 1

# Run those commonds below...
# Let's resize the image first and then use the whole process ... 
Resize_Img()    # resize all the images into a new dir ... 
lab_templates(mode_list = ["train/", "test/", "other/"], img_add = new_img_add, lab_add = lab_add)   # create the resized templates...
top_fre()



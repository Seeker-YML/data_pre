# the write_object_txt() function used to generate the kitti-like format txt files for every traffic-sign object in TT100K dataset 
# the txt_to_instance() function used to generate the corresponding ground-truth image for the every txt file.
# Note that tt100k also has three txt files contain the images ids for three set (train_ids.txt/test_ids.txt/other_ids.txt)

import json
import os
import cv2

# Take care! For automatic data generation, we need to write another script contains some terminal commands 99... 

json_add = "/Users/meiluyuan/tt100k/data/annotations.json"    # the address of annotations.json of tt100k
label_add = "/Users/meiluyuan/Desktop/gt_cls_data/labels/"            # the label address of the train/test/other set
mode_list = ["train/", "test/", "other/"]


# write_object_txt function works to extract necesaary infos from 
def write_object_txt(json_add = json_add, label_add = label_add, mode_list = mode_list):

	tt100k_json_file = json.loads(open(json_add).read())    # load all the contexts of tt100k annos.
	types_list = tt100k_json_file["types"]                  # all traffic-sign types in tt100k dataset
	print types_list
	
	for mode in mode_list:
		ids_txt = open(label_add + mode.split("/")[0] +"_ids.txt", 'r').readlines()
		print "the length of the {}_ids.txt is {}".format(mode, len(ids_txt))
		
		index = 0
		for item in ids_txt:
			temp = tt100k_json_file["imgs"][str(item).rstrip('\n')]   # Take care. There the image_id should be str(numbers).
			temp_path = temp["path"]
			temp_objects = temp["objects"]   # every image may contain several traffic-sign objects...
			object_id = 0
			for object_ in temp_objects:
				txt_file = open(label_add + mode + str(index) + ".txt", 'w')
				bbox = object_["bbox"]
				print bbox
				xmin, ymin, xmax, ymax = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
				txt_file.write(str(temp_path) + "_" + str(object_["category"]) + "_")
				txt_file.write( str(float(xmin)) + "_" + str(float(ymin)) + "_" + str(float(xmax)) + "_" + str(float(ymax)) )
				if object_["category"] in types_list:
					print object_["category"]
					label_id = types_list.index(object_["category"]) + 1
				else:
					label_id = 0  # take care...
				# If the trafficsign class is not in the basic types of tt100k, we should set it as the none-existed class.
				# But remember in the following sections, we will regenerate the classnumber for classification...
				txt_file.write("_" + str(label_id) + "\n")
				txt_file.close() 
				index += 1
				object_id += 1   # If we print this variable, we can get how many objects in the current image. 
				# print "the index is ", index
				# print "the object_id is ", object_id
				# print "\n"
		print index

src_add = "/Users/meiluyuan/tt100k/data/"     # the dir contains the source images of tt100k...
gt_add = "/Users/meiluyuan/Desktop/gt_cls_data/ori_imgs/"    # the dir to save the gt_image data...

def txt_to_instance( src_add = src_add, gt_add = gt_add, label_add = label_add, mode_list = mode_list):
	for mode in mode_list:
		index = 0
		txt_list = os.listdir(label_add + mode)    # list all the files in current dir without order...
		txt_list = sorted(txt_list, key = lambda x : int(x.split(".")[0]))   # sorted_list after os.listdir() is beneficial
		print "The txt_list is :", txt_list
		for txt in txt_list:
			f = open(label_add + mode + txt, 'r').read()
			contexts = f.split("_")
			current_img = cv2.imread(src_add + contexts[0])
			xmin,ymin,xmax,ymax = int(float(contexts[2])), int(float(contexts[3])), int(float(contexts[4])), int(float(contexts[5]))
			if xmin < 0: xmin = 0
			if ymin < 0: ymin = 0
			if xmax > 2048: xmax = 2048
			if ymax > 2048: ymax = 2048 
			# if the pixel index is beyond the min and max of current image, there won't be any reported error, 
			# but the written file will contain empty context...
			new_img = current_img[ymin:ymax,xmin:xmax]          # cv2 x axis & y axis is inverse from our common sense.
			new_img_name = gt_add + mode + str(index) + ".jpg"
			cv2.imwrite(new_img_name , new_img)
			index += 1
			print "The {} set, the item {}".format(mode, index)

write_object_txt()
txt_to_instance()

# You may need to wait a few minutes until all instances DONE!!!

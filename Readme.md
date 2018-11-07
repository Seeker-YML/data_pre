# This is Data Processing Section of TT100K dataset...
(A little complicated, but allow users acquire or modify any part...)

I've re-written these separated .py files in only three new .py files with some functions inside them. The instructions of them are shown below.

1.json_to_gt.py

1.1.From the TT100K annotations.json to kitti-like format num.txt;
collect and save the useful infos of single traffic-sign with txt format.
the contexts of txt file is like: 
Path/to/image_classname_bbox-xmin_bbox-ymin_bbox-xmax_bbox-ymax_objectid

1.2.Generate the ground-truth traffic-sign images with the 2048*2048 images && existed txt files.
with the txt files contain necesaary infos about traffis-sign ground-truth (1 txt for 1 ground truth), we use the cv2 lib to help us extract every gt-image and give each of them a new name (the generation order number of the gt-image).

2.top_fre.py

2.1.Extract the top-frequent items based on the txt labels (the top_fre number should be set by user)
We may need to use the most frequent items during our experiments (as presented in the TT100K paper)

2.2.Generate the templates of the training&testing sets individually 
(Important References)
The 

2.3.(Optimal)Resize the gt images to your ideal scale using your preferable way
In order to decrease the required computation&&make images adapted to different CNN architectures, you could choose to resize the images to the same size.

3.tt100k_bin.py

3.1 Generate the TT100K gt_cls bin file in cifar10 format
(<1byte_label><3072bytes_rgb_data>, the images data should be the RGB data in row-major)

3.2 



# for more detailed comments, PLEASE move to program's comments...
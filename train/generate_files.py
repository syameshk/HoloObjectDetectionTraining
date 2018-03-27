import sys
import os
import glob
import platform
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from generate_txt import write_txt

# global constants
class_id = 0
class_name = None
img = None
tl_list = []
br_list = []
object_list = []


# Image folder default name
image_folder = 'Images'
# If we pass the folder name in the argument, read it
if len(sys.argv) > 1:
	image_folder = sys.argv[1]

# default image extension
filter_ext = "*.jpg"
if len(sys.argv) == 3:
	filter_ext = sys.argv[2]

# Percentage of images to be used for the test set
percentage = 10;


def line_select_callback(clk, rls):
	global tl_list
	global br_list
	global object_list
	global class_name
	tl_list.append((int(clk.xdata), int(clk.ydata)))
	br_list.append((int(rls.xdata), int(rls.ydata)))
	object_list.append(class_name)


def onkeypress(event):
	global object_list
	global tl_list
	global br_list
	global img
	global class_id
	if event.key == 'q':
		print(object_list)
		write_txt(class_id, img, object_list, tl_list, br_list, os.path.dirname(img.path))
		tl_list = []
		br_list = []
		object_list = []
		img = None


def toggle_selector(event):
	toggle_selector.RS.set_active(True)


if __name__ == '__main__':

	print('Reading images from :'+image_folder +" of type :"+filter_ext)

	# Create .names file with the provided file name
	voc_names_file = open('voc.names', 'w+')

	# class_id to set -1
	class_id = -1
	
	# Get all the folders in the root folder
	for root, folders, files in os.walk(image_folder):
		# In each folder
		for folder in folders:

			# Set the class id, starts from 0
			class_id = class_id + 1
			# Name of the current class
			class_name = folder
			#Add the class name to the voc.names file
			voc_names_file.write(class_name + "\n")

			for n, image_file in enumerate(os.scandir(os.path.join(root, folder))):

				if image_file.name == '.DS_Store':
					continue
				if image_file.name.split('.')[-1] == 'txt':
					continue

				img = image_file
				print('File accesiing : '+img.path)
				
				fig, ax = plt.subplots(1, figsize=(10.5, 8))
				mngr = plt.get_current_fig_manager()
				#For some reason following line doesn't work on mac
				if platform.system() == 'Windows':
					mngr.window.setGeometry(250, 40, 800, 600)
				#Read the image file using opencv
				image = cv2.imread(image_file.path)
				#convert color: cv2 gives BGR and  matplotlib needs RGB
				image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				ax.imshow(image)

				toggle_selector.RS = RectangleSelector(
					ax, line_select_callback,
					drawtype='box', useblit=True,
					button=[1], minspanx=5, minspany=5,
					spancoords='pixels', interactive=True
				)
				bbox = plt.connect('key_press_event', toggle_selector)
				key = plt.connect('key_press_event', onkeypress)
				plt.tight_layout()
				plt.show()
				plt.close(fig)
		
	
	#Create train and test files
	file_train = open('train.txt', 'w+')  
	file_test = open('test.txt', 'w+')

	counter = 1
	index = round(100 / percentage)
	for root, folders, files in os.walk(image_folder):
		# In each folder
		for folder in folders:
			for filename in glob.glob(os.path.join(root, folder, filter_ext)):
				print (os.path.abspath(filename))
				if counter == index:
					counter = 1
					file_test.write(os.path.abspath(filename) + "\n")
				else:
					file_train.write(os.path.abspath(filename) + "\n")
					counter = counter + 1

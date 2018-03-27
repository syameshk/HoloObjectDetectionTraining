import os
import glob

# Image containing folder
image_folder = 'Images'
filter_ext = '*.jpg'

# Percentage of images to be used for the test set
percentage = 10;

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
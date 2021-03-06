import os
import platform
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from generate_xml import write_xml
from generate_txt import write_txt

# global constants
img = None
tl_list = []
br_list = []
object_list = []

# constants
image_folder = 'Images'
savedir = 'Annotations'
label_folder = 'labels'
obj = 'hdmi_male'


def line_select_callback(clk, rls):
	global tl_list
	global br_list
	global object_list
	tl_list.append((int(clk.xdata), int(clk.ydata)))
	br_list.append((int(rls.xdata), int(rls.ydata)))
	object_list.append(obj)


def onkeypress(event):
	global object_list
	global tl_list
	global br_list
	global img
	if event.key == 'q':
		print(object_list)
		write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
		write_txt(image_folder, img, object_list, tl_list, br_list, label_folder)
		tl_list = []
		br_list = []
		object_list = []
		img = None


def toggle_selector(event):
	toggle_selector.RS.set_active(True)


if __name__ == '__main__':
	#loop over images
	for n, image_file in enumerate(os.scandir(image_folder)):
		img = image_file
		fig, ax = plt.subplots(1, figsize=(10.5, 8))
		mngr = plt.get_current_fig_manager()
		#For some reason following line doesn't work on mac
		if platform.system() == 'Windows':
			mngr.window.setGeometry(250, 40, 800, 600)
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

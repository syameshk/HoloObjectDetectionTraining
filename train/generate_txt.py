import os
import cv2

def write_txt(folder, img, objects, tl, br, savedir):
	if not os.path.isdir(savedir):
		os.mkdir(savedir)
	image = cv2.imread(img.path)
	height, width, depth = image.shape
	#print(image.shape)
	cls_id = 0;

	save_path = os.path.join(savedir, img.name.replace('png', 'txt'))
	with open(save_path, 'w+') as temp_txt:
		for obj, topl, botr in zip(objects, tl, br):
			x,y,h,w = convert(topl,botr,height,width, depth)
			temp_txt.write(str(cls_id) + ' ' + str(x) + ' ' + str(y) + ' ' + str(h) + ' ' + str(w) +'\n')


#[category number] [object center in X] [object center in Y] [object width in X] [object width in Y]
def convert(topLeft, bottomRight, height, width, depth):
	
	#object width x-x
	x_width = bottomRight[0] - topLeft[0];
	#object height y-y
	y_width = bottomRight[1] - topLeft[1];

	#object center x and y
	x_center = topLeft[0] + (x_width / 2.0)
	y_center = topLeft[1] + (y_width / 2.0)

	return (x_center/width, y_center/height, x_width/width, y_width/height)

if __name__ == '__main__':
    """
    for testing
    """

    folder = 'Images'
    img = [im for im in os.scandir('Images') if '000001' in im.name][0]
    objects = ['hdmi_male']
    tl = [(10, 10)]
    br = [(100, 100)]
    savedir = 'Annotations'
    write_txt(folder, img, objects, tl, br, savedir)

     
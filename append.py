import platform
from PIL import Image
from os import listdir

if platform.python_version() != "2.7.12":
	print "warning: this script has been tested only on Python version 2.7.12, yours is different"

if Image.VERSION != "1.1.7":
	print "warning: this script has been tested only on PIL version 1.1.7, yours is different"


# read photo files
photo_names = sorted(listdir("photos"))
photos = []
for photo_name in photo_names:
	photos.append(Image.open("photos/"+photo_name))

# find the smallest height
height_min = 100000

for photo in photos:
	if photo.size[1] < height_min:
		height_min = photo.size[1]

# resize photos
resized_photos = []
width_total = 0

for photo in photos:
	width_curr = photo.size[0]
	height_curr = photo.size[1]
	ratio = float(height_min) / height_curr
	resized_photos.append(photo.resize((int(width_curr * ratio), int(height_curr * ratio)), Image.ANTIALIAS))
	width_total += int(width_curr * ratio)

# create the output image
print "creating image with width:", width_total
collage = Image.new('RGB', (width_total, height_min))

# append photos to the output image:
offset = 0

for photo in resized_photos:
	collage.paste(photo, (offset, 0))
	offset += photo.size[0]

collage.save("collage.jpg")

import platform
from PIL import Image, ImageFont, ImageDraw
from os import listdir
from datetime import datetime

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
collage = Image.new('RGBA', (width_total, height_min))

# append photos to the output image:
offset = 0

for photo in resized_photos:
	collage.paste(photo, (offset, 0))
	offset += photo.size[0]

# texts
offset = 0
i = 0
for photo in resized_photos:
	txt = Image.new('RGBA', (width_total, height_min), (255,255,255,0))
	fnt = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSansMono.ttf', 30)
	d = ImageDraw.Draw(txt)

	if i == 0:
		first_day = datetime.strptime(photo_names[i].split('_')[0], "%Y-%m-%d")
		first_weight = 0.1*int(photo_names[i].split('_')[1].split('.')[0])
	else:
		day = str(abs(first_day - datetime.strptime(photo_names[i].split('_')[0], "%Y-%m-%d")).days) + " days"
		d.text((offset+20, 10), day, font=fnt, fill=(255, 255, 255, 255))
		
		weight = 0.1*int(photo_names[i].split('_')[1].split('.')[0])

		if weight > first_weight:
			weight = "+" + str(weight - first_weight) + " kg"
			d.text((offset+20, 40), weight, font=fnt, fill=(255, 150, 150, 255))
		else:
			weight = "-" + str(first_weight - weight) + " kg"
			d.text((offset+20, 40), weight, font=fnt, fill=(150, 255, 150, 255))

	collage = Image.alpha_composite(collage, txt)
	offset += photo.size[0]
	i = i + 1

collage.save("collage.png")

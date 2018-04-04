import platform
from PIL import Image

if platform.python_version() != "2.7.12":
	print "warning: this script has been tested only on Python version 2.7.12, yours is different"

if Image.VERSION != "1.1.7":
	print "warning: this script has been tested only on PIL version 1.1.7, yours is different"


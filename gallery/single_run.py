from PIL import Image # type: ignore
from adafruit_epd.ssd1675 import Adafruit_SSD1675 # type: ignore
import board # type: ignore
import busio # type: ignore
import digitalio # type: ignore
import glob
import random
import time
import ast

start_time = time.time()
print("start: --- %s seconds ---" % (time.time() - start_time))

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
srcs = None
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# give them all to our driver
display = Adafruit_SSD1675(
    122, #     104,
    250, #     212,  # 2.13" Tri-color display
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=None,
    rst_pin=rst,
    busy_pin=busy,
)

display.rotation = 2

up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()

print("^^ e-ink prep: --- %s seconds ---" % (time.time() - start_time))

images_in = glob.glob("images/*.JPG")
seen_images = []
with open("seen_images") as f:
    seen_images = ast.literal_eval(f.read())
images = [img for img in images_in if img not in seen_images]
if not images:
    images = images_in
    seen_images = []
the_image = random.choice(images)
print("next image: %s" % the_image)
seen_images.append(the_image)
with open("seen_images", "w") as f:
    f.write(repr(seen_images))
image = Image.open(the_image)

# Scale the image to the smaller screen dimension
image_ratio = image.width / image.height
screen_ratio = display.width / display.height
if screen_ratio < image_ratio:
    scaled_width = image.width * display.height // image.height
    scaled_height = display.height
else:
    scaled_width = display.width
    scaled_height = image.height * display.width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - display.width // 2
y = scaled_height // 2 - display.height // 2
image = image.crop((x, y, x + display.width, y + display.height))

# Display image.
display.image(image)
display.display()
print("displaying image: %s" % img)

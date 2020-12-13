"""
Image resizing and drawing using the Pillow Library. For the image, check out the
associated Adafruit Learn guide at:
https://learn.adafruit.com/adafruit-eink-display-breakouts/python-code
Written by Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import busio
import board
import time
from PIL import Image
from adafruit_epd.il0373 import Adafruit_IL0373
from adafruit_epd.il91874 import Adafruit_IL91874  # pylint: disable=unused-import
from adafruit_epd.il0398 import Adafruit_IL0398  # pylint: disable=unused-import
from adafruit_epd.ssd1608 import Adafruit_SSD1608  # pylint: disable=unused-import
from adafruit_epd.ssd1675 import Adafruit_SSD1675  # pylint: disable=unused-import
from picamera import PiCamera

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
# display = Adafruit_SSD1608(200, 200,        # 1.54" HD mono display
# display = Adafruit_SSD1675(122, 250,        # 2.13" HD mono display
# display = Adafruit_IL91874(176, 264,        # 2.7" Tri-color display
# display = Adafruit_IL0373(152, 152,         # 1.54" Tri-color display
# display = Adafruit_IL0373(128, 296,         # 2.9" Tri-color display
# display = Adafruit_IL0398(400, 300,         # 4.2" Tri-color display
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

display.rotation = 0

up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()

print("^^ e-ink prep: --- %s seconds ---" % (time.time() - start_time))

camera = PiCamera()     # initialize camera
camera.color_effects = (128,128) # turn camera to black and white
camera.resolution = (display.width, display.height)
camera.rotation = 180
# camera.exposure_mode = 'night'
# effects = ['none' , 'negative' , 'solarize' , 'sketch' , 'denoise' , 'emboss' , 'oilpaint' , 'hatch' , 'gpen' , 'pastel' , 'watercolor' , 'film' , 'blur' , 'saturation' , 'colorswap' , 'washedout' , 'posterise' , 'colorpoint' , 'colorbalance' , 'cartoon' , 'deinterlace1' , 'deinterlace2']
camera.image_effect = 'hatch'
camera.contrast = 75
camera.start_preview()
# Camera warm-up time
time.sleep(0.5)
print("^^ camera prep: --- %s seconds ---" % (time.time() - start_time))



idx = 0
while True:
    if not up_button.value:
        print("Up Button Pushed")
        image_name = "images/image%s.jpg" % idx
        camera.capture(image_name)

        # camera.capture(image_name)     # take a shot
        print("^^ camera capture: --- %s seconds ---" % (time.time() - start_time))

        image = Image.open(image_name)

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
        print("^^ PIL: --- %s seconds ---" % (time.time() - start_time))

        # Display image.
        display.image(image)
        display.display()
        print("^^ display: --- %s seconds ---" % (time.time() - start_time))
        idx = idx + 1
    time.sleep(0.5)

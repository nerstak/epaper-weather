import os
import time

from PIL import Image

# from lib.waveshare_epd import epd2in13_V3

# epd = epd2in13_V3.EPD()

# screenWidth = epd.height
screenWidth = 250
# screenHeight = epd.width
screenHeight = 122

def clear_screen():
    """
    Clear the screen
    """
    # epd.init()
    # epd.Clear()
    # time.sleep(2)
    # epd.sleep()


def draw_image_on_hardware(img: Image):
    """
    Draw given image to hardware e-ink
    Does not close img
    :param img: Image
    """
    img.show()
    # epd.init()
    # img.save(os.path.join("/tmp", "image.png"))
    #
    # screen_output_file = Image.open(os.path.join("/tmp", "image.png"))
    # epd.display(epd.getbuffer(screen_output_file))
    # time.sleep(2)
    # epd.sleep()

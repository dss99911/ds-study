# convert image to text
from pytesseract import image_to_string

# take screenshot
from PIL import ImageGrab, Image


def take_image_from_clipboard():
    """take a screen shot, convert it to text"""
    # grab the screen
    img = ImageGrab.grabclipboard()
    # save the screen
    # img.save('screenshot.png')
    # convert the screen to text
    text = image_to_string(img)
    return text



def take_text():
    """take a screen shot, convert it to text"""
    # grab the screen
    img = ImageGrab.grab()
    # save the screen
    img.save('screenshot.png')
    # convert the screen to text
    text = image_to_string(Image.open('screenshot.png'))
    return text

result = take_image_from_clipboard()
print(result)

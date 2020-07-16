# import pyautogui
# pyautogui.click(100, 100)

# from pynput import mouse, keyboard
# from pynput.mouse import Button, Controller
#
# mouse = Controller()
# mouse.position = (x_dim/2, y_dim/2 + 100)
# mouse.click(Button.left, 1)

# from PIL import ImageGrab
# from Pillow import ImageGrab
#
# # while True:
# screen=ImageGrab.grab(bbox=(613,296,614,297))
# px = screen.load()
# m=px[0,0]
# print(m,screen.size)
import pyscreeze
from pynput.mouse import Button, Controller
from PIL import Image
import time

COLOR_THRESHOLD = 10

# popescoX = 1100
popescoX = 1600
popescoY = 350
popescoWidth = 700
popescoHeight = 900


mole1_color = (103, 51, 52, 255)
mole2_color = (103, 12, 14, 255)

mouse = Controller()

image_index = 0

def get_pixels():
  global image_index
  print 'Fetching pixels...'

  image = pyscreeze.screenshot(region=(popescoX, popescoY, popescoWidth, popescoHeight))
  # image_index += 1
  # image.save("ss" + str(image_index) + '.png', "PNG")
  # image.show()

  pixels = image.load()

  return pixels

def pixel_is_specific_mole(pixel, mole_color):
  for d in range(3):
    if abs(pixel[d] - mole_color[d]) > COLOR_THRESHOLD:
      return False
  return True

def pixel_is_mole(pixel):
  return pixel_is_specific_mole(pixel, mole1_color) or pixel_is_specific_mole(pixel, mole2_color)

# real mole center (pixel ratio conversion)
def convert_screenshot_pixels(x, y):
  rx = (x + popescoX) / 2
  ry = (y + popescoY) / 2
  return rx, ry

def find_mole_pixel(pixels):
  big_mole_step = 10
  for x in range(0, popescoWidth, big_mole_step):
    for y in range(0, popescoHeight, big_mole_step):
      pixel = pixels[x, y]
      if pixel_is_mole(pixel):
        return x, y
  return -1, -1

def find_mole_center(pixels, mole_x, mole_y):
  small_mole_step = 5
  search_radius = 50
  sum_x = 0
  sum_y = 0
  count = 0

  for x in range(max(0, mole_x - search_radius / 2), min(popescoWidth, mole_x + search_radius), small_mole_step):
    for y in range(max(0, mole_y - search_radius / 2), min(popescoHeight, mole_y + search_radius), small_mole_step):
      pixel = pixels[x, y]
      if pixel_is_mole(pixel):
        sum_x += x
        sum_y += y
        count += 1

  cx = sum_x / count
  cy = sum_y / count

  return cx, cy

def get_mole_in_image(pixels):
  print 'Finding mole...'

  x, y = find_mole_pixel(pixels)
  if x == -1 and y == -1:
    print 'No mole found!'
    return -1, -1

  cx, cy = find_mole_center(pixels, x, y)

  return convert_screenshot_pixels(cx, cy)

def click_pixel(target_x, target_y):
  if target_x == -1 or target_y == -1:
    return

  print 'Clicking mole at', target_x, target_y, '!'

  # Animate mouse movement
  # animate_mouse_move_to(target_x, target_y)

  mouse.position = (target_x, target_y)
  mouse.click(Button.left, 1)

def animate_mouse_move_to(target_x, target_y):
  steps_count = 50
  initial_mouse_position = mouse.position
  initial_x = initial_mouse_position[0]
  initial_y = initial_mouse_position[1]
  distance_x = target_x - initial_x
  distance_y = target_y - initial_y
  step_x = distance_x / steps_count
  step_y = distance_y / steps_count
  for step_index in range(1, steps_count + 1):
    mouse.position = (initial_x + step_x * step_index, initial_y + step_y * step_index)
    time.sleep(0.0005)

print 'Starting bot'
for i in range(1000):
  pixels = get_pixels()
  x, y = get_mole_in_image(pixels)
  click_pixel(x, y)

# image = Image.open('ss1.png')
# image.load()
# x, y = get_mole_in_image(image)
# click_pixel(x, y)

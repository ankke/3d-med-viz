from utils.callbacks import OpacityCallback
from utils.vtk_utils import *

path = '../data/mr_brainixA'
reader, image_data = read_dicom_images(path)

win_width = 750
win_center = 100

max_value = 1
min_value = 0
point = 180

mapper = volume_mapper(reader)
piecewise = piecewise_fun(((0, 0), (point, 1), (point + 1, 1), (255, 0)))
actor = volume_actor(mapper, piecewise)

renderer = renderer(actor, background=(.8, .8, .8))
win_renderer = window_renderer(renderer, 800, 600)
interactor = interactor(win_renderer)

callback = OpacityCallback(actor, win_renderer, point, piecewise)
add_slider((.1, .1), (.9, .1), min_value, max_value, 'transfer function', interactor, callback)

add_style(interactor)

start_render(interactor)

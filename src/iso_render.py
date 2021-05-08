from utils.callbacks import ContourCallback
from utils.vtk_utils import *

path = '../data/mr_brainixA'
_, image_data = read_dicom_images(path)

win_width = 750
win_center = 100

max_iso_value = 800
min_iso_value = 10

contour_filter = contour_filter(image_data, 150)
actor = vtk_actor(poly_data_mapper(contour_filter))

renderer = renderer(actor, background=(.8, .8, .8))
win_renderer = window_renderer(renderer, 800, 600)
interactor = interactor(win_renderer)

callback = ContourCallback(actor, win_renderer, contour_filter)
add_slider((.6, .1), (.9, .1), min_iso_value, max_iso_value, 'iso', interactor, callback)

add_style(interactor)

start_render(interactor)

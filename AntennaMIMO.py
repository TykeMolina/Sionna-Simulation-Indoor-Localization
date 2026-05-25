import numpy as np
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, PathSolver, RadioMapSolver

scene = load_scene("scene/final_scene_windows.xml",merge_shapes=False)
scene.frequency = 40e9 #Hz
scene.synthetic_array = True

scene.tx_array = PlanarArray(
    num_rows=8,
    num_cols=8,
    vertical_spacing=0.003747,
    horizontal_spacing=0.003747,
    pattern="tr38901",
    polarization="V")

scene.rx_array = PlanarArray(
    num_rows=1,
    num_cols=1,
    vertical_spacing=0.5,
    horizontal_spacing=0.5,
    pattern="dipole",
    polarization="V")

scene.tx_array.antenna_pattern.show()


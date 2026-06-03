import os
import sys

# 1. Ocultar la GPU para asegurar modo CPU puro
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["DRJIT_PLATFORM"] = "llvm"


# 2. Localizar dinámicamente LLVM-C.dll dentro de tu entorno activo de Conda
def buscar_llvm_dll():
    # Ruta base del entorno activo
    base_env = sys.prefix

    # Buscar en las rutas típicas de Windows
    rutas_busqueda = [
        os.path.join(base_env, "Lib", "site-packages", "drjit"),
        os.path.join(base_env, "Lib", "site-packages", "drjit", "lib"),
        os.path.join(base_env, "Library", "bin"),
        base_env
    ]

    for ruta in rutas_busqueda:
        posible_archivo = os.path.join(ruta, "LLVM-C.dll")
        if os.path.exists(posible_archivo):
            return posible_archivo
    return None


ruta_dll = buscar_llvm_dll()

if ruta_dll:
    # Registrar la ruta real encontrada para Dr.Jit
    os.environ["DRJIT_LIBLLVM_PATH"] = ruta_dll
    print(f"¡Librería LLVM vinculada con éxito en: {ruta_dll}!")
else:
    print("ADVERTENCIA: No se pudo localizar automáticamente LLVM-C.dll en el entorno.")

# 3. Ahora sí, importar Sionna y Dr.Jit de forma segura
import drjit as dr
import mitsuba as mi
import sionna as sn

print("¡Ecosistema Sionna inicializado correctamente en CPU!")

from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, RadioMapSolver, ITURadioMaterial, PathSolver
import mitsuba as mi
import numpy as np

#_____________________________________________________________________________
scene = load_scene("scenev3/final_scene_v3.xml",merge_shapes=False)
scene.frequency = 29.5e9 #Hz
scene.synthetic_array = True

tx_power_dbm = 31

#Create material and thickness
matAndThick = ITURadioMaterial(name="plasterboard",
                               itu_type="plasterboard",
                               thickness=0.09)#m

#See objects and materials from blender
for name, obj in scene.objects.items():
    if obj.radio_material.name == "itu_plasterboard":
        obj.radio_material = matAndThick #Applies thickness
#_____________________________________________________________________________

# Configure antennas arrays
scene.tx_array = PlanarArray( #Transmitter
    num_rows=1,
    num_cols=4,
    vertical_spacing=0.5,
    horizontal_spacing=0.5,
    pattern="iso",
    polarization = "V")

scene.rx_array = PlanarArray( #Receiver
    num_rows=1,
    num_cols=1,
    vertical_spacing=0.5,
    horizontal_spacing=0.5,
    pattern="dipole",
    polarization="V")

#Create transmitter and receiver
tx = Transmitter(name="tx",
                 position=mi.Point3f(-7, 0, 1),
                 orientation=mi.Point3f(0, 0, 0),
                 power_dbm= tx_power_dbm)
scene.add(tx)
tx.look_at([-6, 0, 2])
numreceptors = ["1", "2", "3", "4", "5", "6", "7", "7b", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "17b", "18", "19", "20"]
nReceptor = 22
positions = ( (-6.5 , 4),   #1
              (-4   , 3),   #2
              (-2   , 3),   #3
              (0    , 3),   #4
              (1    , 1.2), #5
              (-2   , 1.2), #6
              (-6   , 1.2), #7
              (-4.5 , 1.2), #7b
              (-5.3 , -0.5),#8
              (-2.5 , 0.2), #9
              (0.5  , 0.5), #10
              (2.5  , 1),   #11
              (3    , -1),  #12
              (1    , -2),  #13
              (-2   , -2),  #14
              (-5.3 , -2.5),#15
              (-7   , -2.5),#16
              (-5.7 , -4),  #17
              (-4   , -4),  #17b
              (-2   , -4),  #18
              (1    , -4),  #19
              (3    , -4))  #20
for i in range(nReceptor):
    posx = positions[i][0]
    posy = positions[i][1]
    posz = 1
    rx = Receiver(name=f"rx_{i}",
                 position=mi.Point3f(posx, posy, posz),
                 orientation=mi.Point3f(0.0, 0.0, 0.0))
    scene.add(rx)
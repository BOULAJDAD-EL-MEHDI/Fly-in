 This project has been created as part of the 42 curriculum by  eboulajd.

 ---
 # Description

 Fly-in is project that contain allot of consepts, the main goal of this project is to make engin to manipulate the trafc of multiple dornes, so the input comme from config.txt file that contain three parts first one is `nb_drones` parameter that should be at the begining of the file, if not the program should be stop and raise costom Error message.
 ```
 nb_drones: n => n is positive integer && it should be at the first line 
 ```
the second part is the parameters that contain three types: 
 ```
 coordinates/
 ├── start_hub:   start    (coordinates)  [Metadata]
 ├── hub:         name_1   (coordinates)  [Metadata]
 ├── hub:         name_2   (coordinates)  [Metadata]
 ├── ...          ...       ...           [Metadata]
 ├── hub:         name_n   (coordinates)  [Metadata]
 ├── end_hub:     goal     (coordinates)  [Metadata]
 ```
 so the type one is `start_hub` that contain the name of hub and the coordinates and also some Metadata, and it should be just one parameter named `start_hub` and if not the program must stop and raise costom message Error, the second type of parameters is `hub` so this is like a place that have name and coordinates and some metadata, this one is the zones that the drones may or may not pass throuit, the last type is like the first one, `end_hub` is parameter that contain also a name and coordinates and metadata and this one is the goal of all drones, so after starting from `start_hub`and pasing by all or some of `hub` zones the last station or the goal is `end_hub` zone.

 the last part is connection part:
 ```
 connection: hub+
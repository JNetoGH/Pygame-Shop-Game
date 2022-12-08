from game_objects.Test2 import Test2Obj
from game_objects.map import Map
from game_objects.player import Player
from game_objects.test_obj import TestObj
from JNetoProductions_pygame_game_engine.camera import Camara
from JNetoProductions_pygame_game_engine.game_loop import GameLoop
from JNetoProductions_pygame_game_engine.rendering_layer import RenderingLayer
from JNetoProductions_pygame_game_engine.scene import Scene


# needs to be the first thing instantiated
game_loop = GameLoop()

# rendering layer and the main Camera
rendering_layer_map = RenderingLayer()
rendering_layer_test = RenderingLayer()
rendering_layer_player = RenderingLayer()
main_camera = Camara(rendering_layer_map, rendering_layer_test, rendering_layer_player)

# the scene
shop_scene = Scene(main_camera)

# GameObjects
game_map = Map("map", shop_scene, rendering_layer_map)
player = Player("game_player", shop_scene, rendering_layer_player)
test_obj = TestObj("test_obj_1", shop_scene, rendering_layer_test)
test_obj2 = Test2Obj("test2", shop_scene, rendering_layer_test)

# sets the camera to follow the payer
main_camera.follow_game_object(player)

# GAME LOOP
game_loop.set_current_scene(shop_scene)
game_loop.run_game_loop()


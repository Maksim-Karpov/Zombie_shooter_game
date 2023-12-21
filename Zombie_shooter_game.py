#Для корректной работы, с свойствах проекта в обозревателе 
#решений, необходимо во вкладке "Отладка" указать путь к интерператотору Питона
#Его можно найти, прописав в cmd "where python"

#if it writes "not accessed" means it hasn't been used yet

#Pre-made modules from libraries
from ursina import *
from random import random, randint

#Self-made modules
from Environment import fence, tree, ground, fog
from gameGuns import pistolGun
from Zombies import zombie
from Player import survivor


#------main game section-----------------------------
app = Ursina()
window.title = "Lost among (us) UnDead"
#window.cog_button.disable()
#window.exit_button.disable()

#skybox_image = load_texture("snowsky")
#Sky(texture=skybox_image)

#-----------CREATING AN ENVIRONMENT-----------
plane = ground()

#--------------SUNLIGHT------------
#sun = DirectionalLight()
#sun.look_at(Vec3(0, 0, 0))

#------------MAKING VISIBLE BORDERS-----------
topFence = fence(position=(100, 1, 0), rotation=(0, 0, 0)) #ground.scale[0]/2, 1, 0), rotation=(0, 0, 0) 
leftFence = fence(position=(0, 1, 100), rotation=(0, 90, 0))
bottomFence = fence(position=(-100, 1, 0), rotation=(0, 0, 0))
rightFence = fence(position=(0, 1, -100), rotation=(0, 90, 0))


#-------ADDING PLAYER-----------
player = survivor(position=(0, 10, 0))

#-----RANDOM TREE SPAWN----
for i in range(-100, 100, 10):
    for j in range(-100, 100, 10):
        chance = random()
        if i == player.position[0] and j == player.position[2]:
            chance = 0
        if chance > 0.6:
            spawnTree = tree(position=(i+randint(2, 6), 0, j+randint(2, 6))) #small offset
            spawnTree.collider = BoxCollider(spawnTree, center=Vec3(0, 400, 0), size=Vec3(60, 60, 60)*10)
            

#making a sort of gun viewmodel doesnt work ofc
pistol = pistolGun()

#Zombie spawner
for i in range (-90, 90, 60):
    for j in range (-90, 90, 60):
        if i in range (-70, 70) and j in range (-70, 70):
            continue
        else: enemy = zombie(player, (i, 1, j)) #Переработать алогритм и позиции спавна + уменьшить кол-во зомбей


#----------COMPLEX FOG-----------
#adds fog but not the way its wanted
#scene.fog_density = (10, 40)
camera.clip_plane_far = 80

#Adding fog as images СДЕЛАТЬ ПОМЕНЬШЕ РАЗРЕШЕНИЕ ТЕКСТУРЫ ТУМАНА, 240p например

#CREATE FOG CLASS TO AVOID COPYINGS
fog_100 = fog(position = (0, 9, 25), texture="Assets/Fog_100", rotation=(-90, 0, 0), parent=player)
fog_75 = fog(position=(0, 9, 20), texture="Assets/Fog_75", rotation=(-90, 0, 0), parent=player)
fog_60 = fog(position=(0, 9, 14), texture="Assets/Fog_60", rotation=(-90, 0, 0), parent=player)
fog_above = fog(position=(0, 10.5, 0), texture="Assets/Fog_100", rotation=(0, 0, 0), parent=player)


editor_camera = EditorCamera(enabled=False, ignore_paused=True)

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play modela
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)


#-----RUNNING THE GAME----------
#if __name__ == "__main__":
app.run() #Shift + Q to close since the mouse is used for player

    
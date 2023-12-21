from ursina import *

#Attempting to add a fence for the boundaries
class fence(Entity): #наследование от Entity
    def __init__(this, position, rotation): 
        super().__init__(
        model="cube",
        scale=(0, 6, 200),
        texture="Assets/iron-fence",
        texture_scale=(8, 1),
        position=position,
        rotation=rotation,
        collider="box"
        )

class tree (Entity):
    def __init__(self, position):
        super().__init__(
            model="Assets/SimpleTree.fbx",
            texture="Assets/Treesnow.png",
            scale=0.007,
            position=position,
            double_sided=True,
            #collider=BoxCollider(spawnTree, center=position, size=Vec3(6, 10, 6))
        )

class ground(Entity):
    def __init__(self):
        super().__init__(
            model = "plane", #preloaded in-engine assets
            scale = (400, 1, 400),
            texture = "snowtexture", 
            texture_scale = (10, 10),
            collider = "box",
        )
        #---------------AUDIO------------
        self.envorinment_ambience = Audio('Assets/Music/winter_wind_ambience', loop=True, autoplay=True, volume=5) 

class fog(Entity):
    def __init__(self, position, texture, rotation, parent): #height
        super().__init__(
            model = "plane", 
            scale = (60, 0, 25),
            rotation = rotation,
            double_sided = True,
            position = position, # (Лево-право, верх-низ, вперёд-назад)
            texture = texture, 
            texture_scale = (1, 1),
            parent = parent
        )
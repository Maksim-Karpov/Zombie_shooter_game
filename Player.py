from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Screen_displays import player_health_display

#Creating a player controller with ready controlls
#To create your own parameters, you would use Entity and set own values

class survivor(FirstPersonController):
    def __init__(self, position, **kwargs): #dunno if that (**kwargs) works
        super().__init__(
        speed=6,
        postition = position,
        scale=Vec3(1, 1, 1),
        mouse_sensitivity=Vec2(110, 110),
        model="cube",
        color=color.green,
        visible_self=False,
        cursor = Entity(parent=camera.ui, model='plane', texture="Assets/Crosshair.png", texture_scale=(1, 1), scale=0.04, double_sided=True, rotation_x=90)
        )
        self.collider = BoxCollider(self, Vec3(0,1,0), Vec3(1,2,1))

        self.running_sound = Audio('Assets/SFX/running_snow_1', loop=True, volume=3, autoplay=False)
        self.walking_sound = Audio('Assets/SFX/walking_snow_1', loop=True, volume=3, autoplay=False)

        self.player_hp = 100 # ADD FUNCTIONALITY TO HP !!!
        self.curr_hp = self.player_hp
        self.health_display = player_health_display(self.curr_hp)
        
    def input(self, key):
        if key == Keys.left_shift:
            self.speed = 15
            self.running_sound.play()
        elif key == Keys.left_shift_up:
            self.speed = 6
            self.running_sound.stop()

    def healing(self): #add auto-healing when player is not attacked by zombies (like in cod)
        destroy(self.health_display)
        self.curr_hp += 0.5
        self.health_display = player_health_display(self.curr_hp)
    
    #def update(self):
    #    if self.curr_hp < self.player_hp:   # DOESNT WORK, PLAYER CANT MOVE AT ALL, OTHER FUNCS WORKS
    #        self.healing()
     

#class survivor(Entity):
#    def __init__(self, position):
#        super().__init__(
#            position=position,
#            speed = 8,
#            jump_height = 5,
#            visible_self = False
#        )
        
#        # player's camera
#        mouse.locked = True
#        camera.parent = self
#        camera.position = (0, 4, 0)
#        camera.rotation = (0, 0, 0)
#        camera.fov = 100
#        self.mouse_sensitivity=100,

#        #directional motion speed
#        #static default values for using on player.
#        #on x and z its zero since the character would stand
#        #y = -20 because of gravity.
#        #y = 0 would mean the player floating in air
#        self.motion = (0, -20, 0)
#        self.motion_x = self.motion[0]
#        self.motion_y = self.motion[1]
#        self.motion_z = self.motion[2]

#        #Character movement
#        self.movementX = 0
#        self.movementZ = 0
    
#    def jump(self):
#        self.isJumping = True
#        self.motion_y = self.jump_height


   






from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Screen_displays import player_health_display, death_display
from Game_settings import *

#Creating a player controller with ready controlls
#To create your own parameters, you would use Entity and set own values

class survivor(FirstPersonController):
    def __init__(self, position, **kwargs): #dunno if that (**kwargs) works
        super().__init__(
        speed=1,
        postition = position,
        scale=Vec3(1, 1, 1),
        mouse_sensitivity=Vec2(110, 110),
        model="cube",
        color=color.green,
        visible_self=False
        )
        self.collider = BoxCollider(self, Vec3(0,1,0), Vec3(1,2,1))
        self.hurt = Entity(parent=camera.ui, model='plane', texture="Assets/Hurt.png", texture_scale=(1,1), scale=(2,1), double_sided=True, rotation_x=-90, enabled=False)
        self.running_sound = Audio('Assets/SFX/running_snow_1', loop=True, volume=3, autoplay=False)
        self.walking_sound = Audio('Assets/SFX/walking_snow_1', loop=True, volume=3, autoplay=False)

        self.player_hp = 100 
        self.curr_hp = self.player_hp
        self.health_display = player_health_display(self.curr_hp)
        self.regen_cooldown_time = 1 #def - 0.5
        self.is_regen_cooldown = False

        self.cursor.visible = False
        
    def input(self, key):
        if key == Keys.left_shift:
            self.speed = PLAYER_RUN_SPEED
            self.running_sound.play()
        elif key == Keys.left_shift_up:
            self.speed = 1
            self.running_sound.stop()

    def regenerate_health(self): #add auto-healing when player is not attacked by zombies (like in cod) # DO IT with regen_cooldown!!!
        if not self.is_regen_cooldown:
            self.is_regen_cooldown = True
            destroy(self.health_display)
            self.curr_hp += 10 #10 def.
            self.health_display = player_health_display(self.curr_hp)
            invoke(setattr, self, 'is_regen_cooldown', False, delay=self.regen_cooldown_time)

            
    def check_health(self):
        if self.curr_hp <= 0:
            self.death_message = death_display()
        elif self.curr_hp < self.player_hp:
            self.regenerate_health()
        elif self.curr_hp == self.player_hp:
            return
        elif self.curr_hp > self.player_hp:
            self.curr_hp = self.player_hp
        else: return

    def get_damage(self, damage):
        destroy(self.health_display)
        self.curr_hp -= damage
        self.hurt.enabled = True
        invoke(self.hurt.disable, delay = 0.1)
        self.health_display = player_health_display(self.curr_hp)

    def move(self):
        if held_keys["w"]:
            self.position += self.forward * PLAYER_WALK_SPEED * time.dt * self.speed
        if held_keys["a"]:
            self.position += self.left * PLAYER_WALK_SPEED * time.dt * self.speed
        if held_keys["s"]:
             self.position += self.back * PLAYER_WALK_SPEED * time.dt * self.speed
        if held_keys["d"]:
             self.position += self.right * PLAYER_WALK_SPEED * time.dt * self.speed
    
    def mouse_movement(self):
        camera.rotation_x -= mouse.velocity[1] * MOUSE_SENSITIVITY   #LAST STOPPED HERE !!!
        #camera.rotation_y += mouse.velocity[0] * 120 
        self.rotation_y += mouse.velocity[0] * MOUSE_SENSITIVITY
    

    def update(self):
        self.check_health()
        self.move()
        self.mouse_movement()

     

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


   






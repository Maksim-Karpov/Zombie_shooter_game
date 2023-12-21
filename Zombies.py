from ursina import *
from Screen_displays import player_health_display

shootables_parent = Entity()
mouse.traverse_target = shootables_parent #allows player to shoot zombies, idk how it works tho.
                                          #w/o it, they are unkillable

class zombie(Entity):
    def __init__(self, player, start_position):
        super().__init__(
        parent=shootables_parent,
        model = "cube",
        scale_y = 2,
        position = start_position,
        collider = "box",
        double_sided = True,
        color=color.white)
        #texture = "Assets/snoot",
        #texture_scale = (1, 1))
            
        self.max_hp = 100
        self.hp = self.max_hp

        self.player = player

    def attack(self): #Add attack to draw health from player when zombie is near to him 
        destroy(self.player.health_display)
        self.player.curr_hp -= 1 * time.dt
        self.player.health_display = player_health_display(self.player.curr_hp)
        return

    def update(self):
        dist = distance(self.player.position, self.position)

        self.look_at_2d(self.player.position, 'y') #'y' means around which axis the enemy will rotate to look at player
        hit_info = raycast(self.position + Vec3(0, -0.1, 0), self.forward, distance=200, ignore=(self,), color=color.red, debug=False)#if true, it draws rays (they lower performance)

        if dist <= 2:
            self.attack()
            return

        if hit_info.entity == self.player:
            if dist > 2:
                self.position += self.forward * time.dt * 6
            
        if self.hp <= 0:
            destroy(self)
            return



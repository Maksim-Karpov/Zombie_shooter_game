from turtle import position
from ursina import *
from Ammo_screen_display import ammo_display

class pistolGun(Entity):
	def __init__(self):
		super().__init__(
			model="Assets/PistolGun.fbx",
		    parent=camera,
		    scale=0.0008,
		    position=Vec3(0.4, -0.5, 1), #(1, 1.6, 10)
		    rotation=(0, 90, 0),
		    double_sided = True,
			crosshair = Entity(parent=camera.ui, model='plane', texture="Assets/Crosshair.png", texture_scale=(1, 1), scale=0.04, double_sided=True, rotation_x=-90)
		)

		#viewmodel arrangement
		self.non_aim_pos = self.position
		self.aim_pos = Vec3(0, -0.387, 0.5) # (left-right(X), up-down(Y), forward-backward(Z)) (0, -0.385, 0.5) - perfect
		self.damage = 20

		#ammunition part
		self.clip_capacity = 80 #8
		self.full_ammo = 800 #40 
		self.left_ammo = self.full_ammo
		self.cur_bul_count = self.clip_capacity
		self.is_reloading = False
		self.reload_time = 1.2 #1.2
		self.can_shoot = True
		self.empty_click = False #----
		self.empty_cooldown = False
		self.ammo_display = ammo_display(self.cur_bul_count, self.left_ammo) 

		#shooting and gun sounds maintenance		
		self.gunshot = Audio('Assets/SFX/gunshots/pistol-shot.wav', loop=False, autoplay=False, volume=0.5)
		self.empty_gun = Audio('Assets/SFX/gunshots/empty_gun.wav', loop=False, autoplay=False, volume=0.5)
		self.pistol_reload = Audio("Assets/SFX/gunshots/pistol_reload.wav", loop=False, autoplay=False, volume=0.5)
		self.shoot_delay = 0.1 #0.3
		self.is_on_cooldown = False						  #(-430, 460, 30)
		self.muzzle_flash = Entity(model='plane', position=(-430, 460, 10), parent=self, world_scale=.2, texture="Assets/Pistol_flash.png", texture_scale=(1,1), enabled=False, rotation_z=90, rotation_x=90)
	

		#self.empty_click = True
		#	if self.empty_click:
		#		self.empty_gun.play()
		#		invoke(setattr, self, 'empty_click', False, delay=0.5)


	#class functions for functionality
	def shoot(self):
		if self.cur_bul_count == 0 or (self.cur_bul_count == 0 and self.left_ammo == 0):
			self.can_shoot = False
			self.empty_click = True
			#return
		
			#this part is used to play empty click and not make it overlay infifnitely
		if self.empty_click and not self.empty_cooldown:
			self.empty_cooldown = True
			self.empty_gun.play()
			invoke(setattr, self, 'empty_cooldown', False, delay=0.3)
			self.empty_click = False

		if not self.is_on_cooldown and self.can_shoot: #APPLY can_shoot WHERE NEEDED
			self.is_on_cooldown = True
			self.muzzle_flash.enabled = True
			self.gunshot.play()
			invoke(self.muzzle_flash.disable, delay = 0.001)
			invoke(setattr, self, 'is_on_cooldown', False, delay=self.shoot_delay)
			self.cur_bul_count -= 1
			destroy(self.ammo_display)
			self.ammo_display = ammo_display(self.cur_bul_count, self.left_ammo)
														#œ≈–Ã≈—“»“‹ ›“Œ ¬ Œ“ƒ ‘”Õ ÷»ﬁ, œ–»Õ»Ã¿ﬁŸ»”ﬁ œ¿–¿Ã≈“–¿Ã» Ã¿√¿«»Õ + Œ—“¿“Œ  » √≈Õ. “≈ —“
			if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
				mouse.hovered_entity.hp -= self.damage
				mouse.hovered_entity.blink(color.red)

	def reload_gun(self): #part that is used for realoding weapon #APPLY can_shoot WHERE NEEDED and REWORK 
		if self.cur_bul_count < self.clip_capacity: #checks if you dont have full mag
			self.can_shoot = False # used so that you cant shoot while reloading
			if self.left_ammo == 0: #if you dont have any ammo left at all, you cant reload, duh
				return
			elif self.left_ammo - (self.clip_capacity - self.cur_bul_count) <= 0: # checking of you almost ran out of ammo to not go negative
				self.cur_bul_count += self.left_ammo
				self.left_ammo = 0
				self.text = Text(text="reloading", color=color.black, y=-0.02)
				self.pistol_reload.play()
			else:
				#rework the part where if you have left 
				self.left_ammo += self.cur_bul_count
				self.cur_bul_count = self.clip_capacity
				self.left_ammo -= self.clip_capacity #normal reload
				self.text = Text(text="reloading", color=color.black, y=-0.02)
				self.pistol_reload.play()
		else: return #returns if the mag is full 

		invoke(setattr, self, 'can_shoot', True, delay=self.reload_time)
		destroy(self.text, delay=self.reload_time)
		destroy(self.ammo_display)
		self.ammo_display = ammo_display(self.cur_bul_count, self.left_ammo)
		#here, the animation is supposed to play


	def aim(self): #doesn't work now. (non-aim - |aim-non-aim| should work in theory)
		self.position = self.aim_pos #(self.non_aim_pos - (self.aim_pos - self.non_aim_pos)*-1) * time.dt * 3
		self.crosshair.visible = False

	#def unaim(self):
	#	self.position = (self.aim_pos + self.non_aim_pos) * time.dt * 3

	def input(self, key):
		if key == 'r':
			self.reload_gun()

	def update(self):
		if held_keys["left mouse"] and not self.is_reloading:
			self.shoot()
		elif held_keys["right mouse"]: #used to if and it worked
			self.aim()
		elif self.position == self.non_aim_pos:
			return
		else:
			self.position = self.non_aim_pos
			self.crosshair.visible = True
			#elif not held_keys["right mouse"]: not good cuz it will be checking it all the time which will drop preformance
		
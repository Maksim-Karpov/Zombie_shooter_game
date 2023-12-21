from ursina import Text
from ursina import color

def ammo_display(bullet_count, ammo_left):
    display_text = Text(text=str(bullet_count)+"/"+str(ammo_left), scale=2, x=0.7, y=-0.35, color=color.black)
    return display_text

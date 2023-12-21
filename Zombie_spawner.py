#Импортировать необходимые модули
from Zombies import zombie

zombi = zombie()
#Zombie spawner, a for loop cycle, that spawns zombies assigning i and j as coordinates for spawn
def ZombieSpawner(player, zombi):
    for i in range (-90, 90, 25):
        for j in range (-90, 90, 25):
            if i in range (-70, 70) and j in range (-70, 70):
                continue
            else: enemy = zombi(player, (i, 1, j)) #Переработать алогритм и позиции спавна + уменьшить кол-во зомбей


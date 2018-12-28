"""
author:Roelof Roessingh
start_date:2018, dec, 25
end_date:2018, dec, 29
source and structure from:
https://pythonspot.com/snake-with-pygame/
"""
from pygame.locals import *
import pygame 
import time
import random

class Player:
	x= 10 
	y = 10 
	speed = 1
	def movRight(self):
		self.x = self.x + self.speed
	def movLeft(self):
		self.x = self.x - self.speed
	def movUp(self):
		self.y = self.y - self.speed
	def movDown(self):
		self.y = self.y + self.speed


class Food:
	x_min,x_max = 20, 750
	y_min,y_max = 20, 450
	x = random.choice(range(x_min,x_max))
	y = random.choice(range(y_min,y_max))
	
		
class Game:
	w = 800
	h = 500
	player = 0 # this initiates what, why needed?

	def __init__(self):
		self._running = True
		self._display_surf = None #??
		self._image_surf = None #??
		self.player = Player()
		self.food = Food()
		self.food_image = None

	def on_init(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE)
		pygame.display.set_caption('SNAKE adpatation from pythonspot.com')
		self._running = True
		#self._image_surf = pygame.image.load("C:/Users/THINK_SUBJECT22/Documents/python/apple.png").convert() #what doe the convert funtion do??
		self._image_surf = pygame.image.load("snake_body_small.png").convert()
		self.food_image = pygame.image.load("food_small.png").convert()
		
	def on_event(self,event):
		keys = pygame.key.get_pressed()
		if event.type == QUIT:
			self._running = False
		if (keys[K_q]):#NOT WORKING ATM, ONLY EXC IS WORKING
			self._running = False

	def on_loop(self):
		pass###pass is used when something is needed for syntactial reasons
	
	def on_render(self):
		self._display_surf.fill((40,100,40))
		self._display_surf.blit(self._image_surf,(self.player.x, self.player.y))
		self._display_surf.blit(self.food_image,(self.food.x, self.food.y))
		pygame.display.flip()
		
	def on_cleanup(self):
		pygame.quit()
		
	def on_execute(self):
		if self.on_init() == False:
			self._running == False
			
		while(self._running):
			pygame.event.pump() #??
			keys = pygame.key.get_pressed()
						
			if (keys[K_RIGHT]):
				self.player.movRight()
			if(keys[K_LEFT]):
				self.player.movLeft()
			if(keys[K_DOWN]):
				self.player.movDown()
			if(keys[K_UP]):
				self.player.movUp()
			if(keys[K_ESCAPE]):
				self._running = False
			if self.player.x < self.food.x+30 and self.player.x > self.food.x-30:
				self.food = Food()
				print('herereeeeeeeeeeeeeeeeeeeee') ###this does nto work at all yet:: think about structure !
		
			
		
			#self.on_loop()
			self.on_render()
			#time.sleep (100.0 / 1000.0)
		self.on_cleanup()



if __name__ == "__main__":
	theGame = Game()
	theGame.on_execute()
	
	
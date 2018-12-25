#cave_swimmer_forest_walker_1.4
"""
author: 		Roelof Roessingh
start_date: 			2018 - dec - 17, Amsterdam
current_date: 			2018 - dec - 25, Amsterdam
main dependencies:	Python 3.7, pygame 1.9.4
git repos:	 	tbd
"""

this = 1
#imports:
import pygame 
import time
import random
import os
import tkinter as tk

#game introduction:
welcome_text1 = "Welcome to Cave Diver" 
welcome_text2 = "control your diver with the arrow keys"
welcome_text3 = "navigate to the end of the cave without hitting the walls" 
welcome_text4 = "(press q to quit)"

#user input settings:
full_screen		= False
symmetry		= False
speed			= .5 		#levels: 1:slowest .5, .3:fastest
player_size_ratio	= 25		#player size will be 1/player_size_ratio of the screen height, should be between 10 (largest) and 50 (smallest)
buffer			= 100

#get device screen size and set game screen size
root 			= tk.Tk()
woriginal, horiginal 	= root.winfo_screenwidth(), root.winfo_screenheight()
wgame,hgame 		= int(root.winfo_screenwidth()/2), int(root.winfo_screenheight()/2)
if full_screen == True:
	wgame,hgame = woriginal,horiginal

#initiate the (py)game screen:
screen 			= pygame.display.set_mode((wgame, hgame))
player_size 		= hgame/player_size_ratio

#set generic variables
done		= False 	#determines if main while loop is broken, if True = game ends
move_step 	= 4 		#how many pixels 1 button press makes player move

#set background:
#define simple function to tell programm to look for images in same folder as the current file, and rescale to game screen size:
_image_library = {} 		
def get_image(path, w, h):
	global _image_library
	image = _image_library.get(path)
	if image == None:
		default_path = path.replace('/', os.sep).replace('\\', os.sep)
		image = pygame.image.load(default_path)
		_image_library[path] = image
		image = pygame.transform.scale(image,(w,h))
	return image

#create a level, relative to the current screen size:
class Level:
	def __init__(self, wgame, hgame, max_range_y, player_size, buffer):
		self.wgame		= wgame
		self.hgame 		= hgame
		self.player_size	= player_size
		self.buffer		= buffer
		self.min_range_x_step 	= int(self.wgame/16)
		self.max_range_x_step 	= int(self.wgame/10)
		self.min_range_y 	= int(self.hgame/54)
		self.max_range_y 	= int(self.hgame-self.player_size-self.buffer)

	def make_level(self, top_line, bottom_line, y_val_checker, y_val_checker_bottom):
		x1 	= 0
		#lists with indices for drawing the lines of the cave:
		self.top_line		= top_line
		self.bottom_line	= bottom_line
		while x1 < self.wgame:
			x_step 	= random.choice(range(self.min_range_x_step, self.max_range_x_step))
			y1 	= random.choice(range(self.min_range_y, self.max_range_y))
			y2 	= self.hgame - y1
			if y1 > (self.hgame/2)-self.player_size-self.buffer:
				y2 = self.hgame - random.choice(range(0, int(self.hgame - y1 - self.player_size - self.buffer)))
			self.top_line.append((x1,y1))
			self.bottom_line.append((x1,y2))
			x1 += x_step

		#append last indices, always the same:
		self.top_line.append((self.wgame, self.hgame-(self.hgame-(self.player_size+10))))
		self.bottom_line.append((self.wgame, self.hgame - (self.player_size+10)))

		#create long check list with y-value for each pixel of the width of the game:
		self.y_val_checker		= y_val_checker
		self.y_val_checker_bottom	= y_val_checker_bottom
		for i in range(len(self.top_line)-1):
			x1 = self.top_line[i][0]
			y1 = self.top_line[i][1]
			x2 = self.top_line[i+1][0]
			y2 = self.top_line[i+1][1]
			y3 = self.bottom_line[i][1]
			y4 = self.bottom_line[i+1][1]

			x_step = x2-x1
			for j in range(x_step):
				y_check_top 	= (abs(y2-y1)/x_step)*j
				y_check_bottom 	= (abs(y4-y3)/x_step)*j
				if y1 >= y2:
					self.y_val_checker.append(y1-y_check_top)
				if y1 < y2:
					self.y_val_checker.append(y1+y_check_top)
				if y3 >= y4: 
					self.y_val_checker_bottom.append(y3-y_check_bottom)
				if y3 < y4:
					self.y_val_checker_bottom.append(y3+y_check_bottom)
		#summcheck:
#		print('length of check lists should be equal to game width (i.e True):')
#		print('top:', len(self.y_val_checker) == self.wgame)
#		print('bottom:', len(self.y_val_checker_bottom) == self.wgame)

		#set starting point player:s	
		self.x,self.y		= 5,((self.top_line[0][1]+self.bottom_line[0][1])/2)+ player_size/2 	#this aligns the starting point of the player in the middle of the 

#initiate (py)game:
pygame.init()
pygame.font.init()
font1 		= pygame.font.SysFont('Times New Roman', 30)
font2 		= pygame.font.SysFont('Times New Roman', 50)
start_text1 	= font1.render(welcome_text1, False, (255, 255, 0))
start_text2 	= font1.render(welcome_text2, False, (255, 255, 0))
start_text3 	= font1.render(welcome_text3, False, (255, 255, 0))
start_text4 	= font1.render(welcome_text4, False, (255, 255, 0))
end_text 	= font2.render('Game completed, Congratulations!', False, (0, 255, 0))

#main loop: this loads the game
level_counter	= 0
nr_levels 	= 4 #should be an even number
#background 	= ["sea.jpg", "forest.jpg"]*int(nr_levels/2)
background = ['C:/Users/THINK_SUBJECT22/Documents/python/cave_diver_roessingh_old/sea.jpg', 'C:/Users/THINK_SUBJECT22/Documents/python/cave_diver_roessingh_old/forest.jpg']*int(nr_levels/2)
current_level 	= Level(wgame, hgame,10,player_size, buffer)
current_level.make_level([], [], [], [])

screen.blit(start_text1,(30,20))
screen.blit(start_text2,(30,50))
screen.blit(start_text3,(30,80))
screen.blit(start_text4,(30,140))
pygame.display.update()
time.sleep(4)

for j in range(nr_levels):
	while not done:
		pressed = pygame.key.get_pressed()

		#define how to end the game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		if pressed[pygame.K_q]: #always include a keyboard exit besides the standard quit event
			done = True
			
		#define arrow keys as controls:
		if pressed[pygame.K_UP]:
			current_level.y -= move_step #movement in pixels
		if pressed[pygame.K_DOWN]:
			current_level.y += move_step
		if pressed[pygame.K_LEFT] and current_level.x > 0 : #make sure player cannot disappear left off-screen
			current_level.x -= move_step
		if pressed[pygame.K_RIGHT]:
			current_level.x += move_step

		#this makes sure that the player does not leave a trail, fills the screen with black
		screen.fill((0, 0, 0))
		#draw background
		screen.blit(get_image(background[level_counter], wgame, hgame), (0,0))
		
		#draw the cave
		for i in range((len(current_level.top_line)-1)):
			x1, y1 = current_level.top_line[i][0], current_level.top_line[i][1]
			x2, y2 = current_level.top_line[i+1][0], current_level.top_line[i+1][1]
			
			x3, y3 = current_level.bottom_line[i][0], current_level.bottom_line[i][1]
			x4, y4 = current_level.bottom_line[i+1][0], current_level.bottom_line[i+1][1]
	
			#top
			pygame.draw.line(screen, (0, 128, 255),(x1,y1), (x2, y2))
			#bottom
			pygame.draw.line(screen, (128, 0, 255),(x3,y3), (x4, y4))
					
			#define current coordinates to check if player is out of bounds:
			if current_level.x < wgame-player_size and current_level.x > player_size:
				check_top_l, check_top_r 	= current_level.y_val_checker[current_level.x], current_level.y_val_checker[current_level.x+int(player_size)]
				check_bottom_l, check_bottom_r 	= current_level.y_val_checker_bottom[current_level.x], current_level.y_val_checker_bottom[current_level.x+int(player_size)]
		
				if check_top_l > current_level.y or check_top_r > current_level.y or check_bottom_l < current_level.y+player_size or check_bottom_r < current_level.y+player_size:
					current_level.x,current_level.y= 5,((current_level.top_line[0][1]+current_level.bottom_line[0][1])/2)+ player_size/2
					pygame.draw.rect(screen, (120, 0, 0), pygame.Rect(0,0, wgame, 30))
					pygame.draw.rect(screen, (120, 0, 0), pygame.Rect(0,hgame-30,wgame, hgame-30))
					pygame.display.update()
					time.sleep(.05)
		
		#finishing a level:
		if current_level.x >= wgame:
			level_counter += 1
			#initiate new level
			current_level = Level(wgame, hgame,10,player_size, buffer)
			current_level.make_level([], [], [], [])
			current_level.x, current_level.y= 5,((current_level.top_line[0][1]+current_level.bottom_line[0][1])/2)+ player_size/2
		
		if level_counter == nr_levels:
			screen.blit(end_text,(30,hgame/2))
			pygame.display.update()
			print('game finished')
			done = True
			for i in range(0, 200, 1):
				time.sleep(0.01)
			
		#draw the player:
		pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(current_level.x,current_level.y, player_size, player_size))
	
		#sleep time is virtually equivalent to speed of the player:
		time.sleep(speed/100)
	
		pygame.display.flip()
		


##bugs:
#when running in spyder: quit does not work: not with q and not with clicking the screen exit
				
##improvements:
#add introduction text
#add intro GUI
#add save option
#add 'lifes' + game over
#add power ups
#add constant movement to the right option
#finetune the math governing the player size + level creation 
#streamline / simplify level class + add a player class
	
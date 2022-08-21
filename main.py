import pygame
from pygame.locals import *
import time
import random

#Pixel size of the block
SIZE = 40
BACKGROUND_COLOR = (204,255,255)

class Apple:
	def __init__(self, parent_screen):
		self.apple = pygame.image.load("resources/apple.jpg").convert()
		self.parent_screen = parent_screen
		self.x = SIZE*3
		self.y = SIZE*3

	def draw(self):
		self.parent_screen.blit(self.apple, (self.x,self.y))
		pygame.display.flip()
 
	def move(self):
		self.x = random.randint(1,24)*SIZE
		self.y = random.randint(1,19)*SIZE

class Snake:
	def __init__(self, parent_screen, length):
		self.length = length
		self.parent_screen = parent_screen
		self.block = pygame.image.load("resources/block.jpg").convert()
		self.x = [SIZE]*length
		self.y = [SIZE]*length
		self.direction = 'down'
		

	# Directional buttons settings
	def move_up(self):
		self.direction = 'up'

	def move_down(self):
		self.direction = 'down'

	def move_right(self):
		self.direction = 'right'

	def move_left(self):
		self.direction = 'left'

	# Walking function
	def walk(self):
		
		for i in range(self.length-1,0,-1):
			self.x[i] =self.x[i - 1]
			self.y[i] =self.y[i - 1]

		if self.direction == 'up':
			self.y[0] -= SIZE
		if self.direction == 'down':
			self.y[0] += SIZE
		if self.direction == 'left':
			self.x[0] -= SIZE
		if self.direction == 'right':
			self.x[0] += SIZE

		self.draw()


	def draw(self):
		for i in range (self.length):
			self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
		pygame.display.flip()

	def lengthen(self):
		self.length+=1
		self.x.append(-1)
		self.y.append(-1)

	#def spd_up(self):
		#walk_spd

class Game:
	def __init__(self):
		#To initialize pygame modules
		pygame.init()
		pygame.display.set_caption("Snake Game")
		pygame.mixer.init()

		#To bring up the pygame window and set screen size
		self.screen = pygame.display.set_mode((1000, 800))
		#To fill the screen with RGB color
		self.screen.fill((0,0,0))

		#To play background music
		self.play_bg_music()

		self.snake = Snake(self.screen, 3)
		self.snake.draw()
		self.apple = Apple(self.screen)
		self.apple.draw()


	def is_collision(self, x1, y1, x2, y2):
		if x1 >= x2 and x1 < x2 + SIZE:
			if y1 >= y2 and y1 < y2 + SIZE:
				return True

		return False

	def is_collision_wall_right(self, x):
		if x > 1000:
			return True
		return False

	def is_collision_wall_left(self, x):
		if x < 0:
			return True
		return False

	def is_collision_wall_top(self, y):
		if y < 0:
			return True
		return False

	def is_collision_wall_bot(self, y):
		if y > 800:
			return True
		return False

	def render_background(self):
		bg = pygame.image.load("resources/background.jpg")
		self.screen.blit(bg, (0,0))

	def play_sound(self, sound):
		sound = pygame.mixer.Sound(f"resources/{sound}.wav")
		pygame.mixer.Sound.play(sound)

	def play_bg_music(self):
		pygame.mixer.music.load("resources/bg-music.mp3")
		pygame.mixer.music.play()

	def play(self):
		self.render_background()
		self.snake.walk()
		self.apple.draw()
		self.display_score()
		pygame.display.flip()

		#Snake colliding with self	
		for i in range(3,self.snake.length):
			if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
				self.play_sound("quack")
				raise "Game Over"

		#Snake colliding with left wall
		if self.is_collision_wall_left(self.snake.x[0]):
			self.snake.x[0] = 1000

		#Snake colliding with right wall
		if self.is_collision_wall_right(self.snake.x[0]):
			self.snake.x[0] = 0
		#Snake colliding with top wall

		if self.is_collision_wall_top(self.snake.y[0]):
			self.snake.y[0] = 800

		#Snake colliding with top wall
		if self.is_collision_wall_bot(self.snake.y[0]):
			self.snake.y[0] = 0


		#Snake collide with apple
		if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
			self.play_sound("pop")
			self.snake.lengthen()
			self.apple.move()

		#Speed of snake walking
		time.sleep(0.3)

	def display_score(self):
		font = pygame.font.SysFont('arial', 30)
		score = font.render(f'Score: {self.snake.length}', True, (200, 200, 200))
		self.screen.blit(score, (800, 10))


	def show_game_over(self):
		self.render_background()
		font = pygame.font.SysFont('arial', 30)
		line1 = font.render(f'Game over! Your score is {self.snake.length}', True, (0,0,0))
		self.screen.blit(line1, (200,300))
		line2 = font.render("Press Enter to play again. To exit press Escape!", True, (0,0,0))
		self.screen.blit(line2, (200,350))
		pygame.display.flip()
		
		pygame.mixer.music.pause()



	def reset(self):
		self.snake = Snake(self.screen, 3)
		self.apple = Apple(self.screen) 


	def run(self):
		running = True
		pause = False

		while running:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False

					if event.key == K_RETURN:
						pygame.mixer.music.unpause()
						pause = False


					if not pause:

						if event.key == K_UP:
							self.snake.move_up()

						if event.key == K_DOWN:
							self.snake.move_down()

						if event.key == K_RIGHT:
							self.snake.move_right()

						if event.key == K_LEFT:
							self.snake.move_left()

				elif event.type == QUIT:
					running = False

			
			try:		
				if not pause:
					self.play()


			except Exception as e:
				self.show_game_over()
				pause = True
				self.reset()


			

if __name__ == "__main__":
	game = Game()
	game.run()

	

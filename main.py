import pygame
from pygame.locals import *
import time

#Pixel size of the block
SIZE = 40

class Apple:
	def __init__(self, parent_screen):
		self.apple = pygame.image.load("resources/apple.jpg").convert()
		self.parent_screen = parent_screen
		self.x = SIZE*3
		self.y = SIZE*3

	def draw(self):
		self.parent_screen.blit(self.apple, (self.x,self.y))
		pygame.display.flip()

class Snake:
	def __init__(self, parent_screen, length):
		self.length = length
		self.parent_screen = parent_screen
		self.block = pygame.image.load("resources/block.jpg").convert()
		self.x = [SIZE]*length
		self.y = [SIZE]*length
		self.direction = 'down'


	def move_up(self):
		self.direction = 'up'

	def move_down(self):
		self.direction = 'down'

	def move_right(self):
		self.direction = 'right'

	def move_left(self):
		self.direction = 'left'

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
		self.parent_screen.fill ((204,255,255))
		for i in range (self.length):
			self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
		pygame.display.flip()

class Game:
	def __init__(self):
		pygame.init()
		#To bring up the pygame window and set screen size
		self.screen = pygame.display.set_mode((1000, 800))
		#To fill the screen with RGB color
		self.screen.fill((204,255,255))
		self.snake = Snake(self.screen, 5)
		self.snake.draw()
		self.apple = Apple(self.screen)
		self.apple.draw()


	def play(self):
		self.snake.walk()
		self.apple.draw()

	def run(self):
		running = True

		while running:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False

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

			self.play()

			time.sleep(0.5)


if __name__ == "__main__":
	game = Game()
	game.run()

	

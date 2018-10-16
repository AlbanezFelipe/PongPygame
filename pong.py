##############################
# PONG GAME                  #
# BY: FELIPE ALBANEZ CONTIN  #
##############################

import pygame
import os
import random

# CONFIGURATIONS #
# Colors
white = (255, 255, 255)
black = (0, 0 , 0)

# Dimens
screen_width = 800
screen_height = 600

block_height = 90
block_width = 15

padding_left = 20
padding_right = screen_width - padding_left - block_width

left_block_y = (screen_height / 2) - (block_height / 2)
right_block_y = (screen_height / 2) - (block_height / 2)

ball_size = 10

ball_x = (screen_width / 2) - (ball_size / 2)
ball_y = (screen_height / 2) - (ball_size / 2)

# False = Left and Down | True = Right and Up
ball_direction_x = bool(random.getrandbits(1)) # Random Boolean
ball_direction_y = bool(random.getrandbits(1)) # Random Boolean
ball_speed_step = 0.5 # Speed increases by every hit on blocks
ball_speed_start = 3
ball_speed = ball_speed_start

# Speed
enemy_speed = 10
player_speed = 10

#Counters
player1 = 0
player2 = 0

# False = Right hitted | True = Left hitted
who_hit = ball_direction_x # Do not change this

two_players = None

# FUNCTIONS #

def reset():
	"""
		Reset match, not the counters
	"""
	global ball_x, ball_y, ball_speed, ball_direction_x, ball_direction_y, who_hit
	ball_x = (screen_width / 2) - (ball_size / 2)
	ball_y = (screen_height / 2) - (ball_size / 2)
	ball_speed = ball_speed_start
	ball_direction_x = bool(random.getrandbits(1))
	ball_direction_y = bool(random.getrandbits(1))
	who_hit = ball_direction_x

	console()

def draw():
	"""
		Draws the ball and the blocks
	"""
	# Player_Block
	pygame.draw.rect(screen, white, pygame.Rect(padding_left, left_block_y, block_width, block_height))

	# Ball
	pygame.draw.rect(screen, white, pygame.Rect(ball_x, ball_y, ball_size, ball_size))

	# Enemy_Block (or 2nd Player)
	pygame.draw.rect(screen, white, pygame.Rect(padding_right, right_block_y, block_width, block_height))

def controllers():
	"""
		Configures the Controllers
	"""
	global left_block_y, right_block_y, ball_speed

	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP] and left_block_y > 0 : left_block_y -= player_speed
	if pressed[pygame.K_DOWN] and left_block_y < screen_height - block_height: left_block_y += player_speed
	if pressed[pygame.K_r]: reset()
	# DEVELOPER MODE - Do not use this keys for play
	if pressed[pygame.K_z]: ball_speed += 0.2
	if pressed[pygame.K_x] and ball_speed > 1: ball_speed -= 0.2
	###############
	if pressed[pygame.K_w] and right_block_y > 0 and two_players: right_block_y -= player_speed
	if pressed[pygame.K_s] and right_block_y < screen_height - block_height and two_players: right_block_y += player_speed

def ball():
	"""
		Ball logic
	"""
	global ball_speed, ball_direction_x, ball_direction_y, ball_x, ball_y, who_hit, player1, player2

	if ball_direction_x: ball_x += ball_speed
	else: ball_x -= ball_speed

	if ball_direction_y: ball_y -= ball_speed
	else: ball_y += ball_speed 

	# Block Colision
	if(
		# Left
		(
			(ball_x + ball_size >= padding_left and ball_x <= block_width + padding_left) and
			(ball_y + ball_size >= left_block_y and ball_y <= block_height + left_block_y) and
			(not who_hit)
		) or
		# Right
		(
			(ball_x + ball_size >= padding_right and ball_x <= padding_right + block_width) and
			(ball_y + ball_size >= right_block_y and ball_y <= block_height + right_block_y) and
			(who_hit)
		) 
	):
		ball_direction_x = not ball_direction_x
		ball_speed += ball_speed_step
		who_hit = not who_hit

	# Top and Bottom Walls Colison
	if(ball_y <= 0 or ball_y >= screen_height - ball_size): ball_direction_y = not ball_direction_y
	
	# GameOver
	if(ball_x < 0):
		# Right won
		player2 += 1
		reset()

	elif(ball_x + ball_size > screen_width):
		# Left won
		player1 += 1
		reset()

def enemy():
	"""
		Enemy logic
	"""
	global right_block_y
	if ball_y + (ball_size / 2) < right_block_y + (block_height / 2) and right_block_y > 0: 
		if (right_block_y + (block_height / 2)) - (ball_y + (ball_size / 2)) < enemy_speed:
			right_block_y -= (right_block_y + (block_height / 2)) - (ball_y + (ball_size / 2))
		else:
			right_block_y -= enemy_speed
	
	elif ball_y + (ball_size / 2) > right_block_y + (block_height / 2) and right_block_y < screen_height - block_height: 
		if (ball_y + (ball_size / 2)) - (right_block_y + (block_height / 2)) < enemy_speed:
			right_block_y += (ball_y + (ball_size / 2)) - (right_block_y + (block_height / 2))
		else:
			right_block_y += enemy_speed

def console():
	"""
		Draw console
	"""
	global two_players

	os.system('cls' if os.name == 'nt' else 'clear') #Clear Screen
	print()
	print(' ______')
	print(' | ___ \\')
	print(' | |_/ /__  _ __   __ _ ')
	print(' |  __/ _ \\| \'_ \\ / _` |')
	print(' | | | (_) | | | | (_| |')
	print(' \\_|  \\___/|_| |_|\\__, |')
	print('                   __/ |')
	print('                  |___/')
	print()
	print('------------------------------------')
	print()
	print('Two Players[Y/N] >>> ',end='')
	if two_players == None: two_players = input().lower() == 'y'
	else: print('Y' if two_players else 'N')
	print()
	print('Player 1:',player1)
	print('Player 2:',player2)
	print()
	print('Screen: ' + str(screen_width) + 'x' + str(screen_height))
	print('Ball Size:', ball_size)
	print('Blocks width:', block_width)
	print('Blocks height:', block_height)
	print()
	print('Controls')
	print('Player 1 UP:   UP ARROW')
	print('Player 1 DOWN: DOWN ARROW')
	print('Player 2 UP:   W')
	print('Player 2 DOWN: S')
	print()
	print('By: Felipe Albanez Contin')
	print()

# GAME #
console()

pygame.init()
pygame.display.set_caption('Pong')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
end = False

while not end:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = True

	controllers()	
	ball()
	if not two_players: enemy()

	screen.fill(black)
	draw()
	pygame.display.flip()
	clock.tick(60)

print('Thanks For Playing')
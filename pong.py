import pygame, sys, random

# -------
# CLASSES
# -------

class Paddle:
	def __init__(self, screen, color, posX, posY, width, height):
		self.screen = screen
		self.color = color
		self.posX = posX
		self.posY = posY
		self.width = width
		self.height = height
		self.state = 'stopped'
		self.draw()

	def draw(self):
		pygame.draw.rect( self.screen, self.color, (self.posX, self.posY, self.width, self.height) )

	def move(self):
		# moving up
		if self.state == 'up':
			self.posY -= 10

		# moving down
		elif self.state == 'down':
			self.posY += 10

	def clamp(self):
		if self.posY <= 0:
			self.posY = 0

		if self.posY + self.height >= HEIGHT:
			self.posY = HEIGHT - self.height

	def restart_pos(self):
		self.posY = HEIGHT//2 - self.height//2
		self.state = 'stopped'
		self.draw()

class Ball:
	def __init__(self, screen, color, posX, posY, radius):
		self.screen = screen
		self.color = color
		self.posX = posX
		self.posY = posY
		self.dx = 0
		self.dy = 0
		self.radius = radius
		self.draw()

	def draw(self):
		pygame.draw.circle( self.screen, self.color, (self.posX, self.posY), self.radius )

	def start(self):
		# this will be random
		self.dx = 15
		self.dy = 5

	def move(self):
		self.posX += self.dx
		self.posY += self.dy

	def wall_collision(self):
		self.dy = -self.dy

	def paddle_collision(self):
		self.dx = -self.dx

	def restart_pos(self):
		self.posX = WIDTH//2
		self.posY = HEIGHT//2
		self.dx = 0
		self.dy = 0
		self.draw()

class PlayerScore:
	def __init__(self, screen, points, posX, posY):
		self.screen = screen
		self.points = points
		self.posX = posX
		self.posY = posY
		self.font = pygame.font.SysFont("monospace", 80, bold=True)
		self.label = self.font.render(self.points, 0, WHITE)
		self.show()

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

	def increase(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, WHITE)

	def restart(self):
		self.points = '0'
		self.label = self.font.render(self.points, 0, WHITE)

class CollisionManager:
	def between_ball_and_paddle1(self, ball, paddle):
		ballX = ball.posX
		ballY = ball.posY
		paddleX = paddle.posX
		paddleY = paddle.posY

		# y is in collision area?
		if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
			# x is in collision area?
			if ballX - ball.radius <= paddleX + paddle.width:
				# collision
				return True

		# no collision
		return False

	def between_ball_and_paddle2(self, ball, paddle):
		ballX = ball.posX
		ballY = ball.posY
		paddleX = paddle.posX
		paddleY = paddle.posY

		# y is in collision?
		if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
			# x is in collision?
			if ballX + ball.radius >= paddleX:
				# collision
				return True

		# no collision
		return False

	def between_ball_and_walls(self, ball):
		ballY = ball.posY

		# top collision
		if ballY - ball.radius <= 0:
			return True

		# bottom collision
		if ballY + ball.radius >= HEIGHT:
			return True

		# no collision
		return False

	def between_ball_and_goal1(self, ball):
		return ball.posX + ball.radius <= 0

	def between_ball_and_goal2(self, ball):
		return ball.posX - ball.radius >= WIDTH

# ---------------------------------------------

# ---------
# CONSTANTS
# ---------
WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# SCREEN
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('PONG')

# ---------
# FUNCTIONS
# ---------
def draw_board():
	screen.fill( BLACK )
	pygame.draw.line( screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5 )

def restart():
	draw_board()
	score1.restart()
	score2.restart()
	ball.restart_pos()
	paddle1.restart_pos()
	paddle2.restart_pos()

draw_board()

# -------
# OBJECTS
# -------
paddle1 = Paddle( screen, WHITE, 15, HEIGHT//2 - 60, 20, 120 )
paddle2 = Paddle( screen, WHITE, WIDTH - 20 - 15, HEIGHT//2 - 60, 20, 120 )
ball = Ball( screen, WHITE, WIDTH//2, HEIGHT//2, 12 )
collision = CollisionManager()
score1 = PlayerScore( screen, '0', WIDTH//4, 15 )
score2 = PlayerScore( screen, '0', WIDTH - WIDTH//4, 15 )

# ---------
# VARIABLES
# ---------
playing = False
clock = pygame.time.Clock()

# --------
# MAINLOOP
# --------
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p and not playing:
				ball.start()
				playing = True

			if event.key == pygame.K_r and playing:
				restart()
				playing = False

			if event.key == pygame.K_w:
				paddle1.state = 'up'

			if event.key == pygame.K_s:
				paddle1.state = 'down'

			if event.key == pygame.K_UP:
				paddle2.state = 'up'

			if event.key == pygame.K_DOWN:
				paddle2.state = 'down'

		if event.type == pygame.KEYUP:
			paddle1.state = 'stopped'
			paddle2.state = 'stopped'

	if playing:
		draw_board()

		# ball
		ball.move()
		ball.draw()

		# paddle 1
		paddle1.move()
		paddle1.clamp()
		paddle1.draw()

		# paddle 2
		paddle2.move()
		paddle2.clamp()
		paddle2.draw()

		# wall collision
		if collision.between_ball_and_walls(ball):
			print('WALL COLLISION')
			ball.wall_collision()

		# paddle1 collision
		if collision.between_ball_and_paddle1(ball, paddle1):
			print('COLLISION WITH PADDLE 1')
			ball.paddle_collision()

		# paddle2 collision
		if collision.between_ball_and_paddle2(ball, paddle2):
			print('COLLISION WITH PADDLE 2')
			ball.paddle_collision()

		# GOAL OF PLAYER 1 !
		if collision.between_ball_and_goal2(ball):
			draw_board()
			score1.increase()
			ball.restart_pos()
			paddle1.restart_pos()
			paddle2.restart_pos()
			playing = False

		# GOAL OF PLAYER 2!
		if collision.between_ball_and_goal1(ball):
			draw_board()
			score2.increase()
			ball.restart_pos()
			paddle1.restart_pos()
			paddle2.restart_pos()
			playing = False

	score1.show()
	score2.show()

	clock.tick(40)
	pygame.display.update()
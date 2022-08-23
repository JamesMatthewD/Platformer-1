import pygame, os, sys
from pygame.locals import *
pygame.init()
vec = pygame.math.Vector2
font=pygame.font.SysFont("Arial", 24)

def updateFPS():
	fps=str(int(framePerSec.get_fps()))
	fps_text=font.render(fps, 1,pygame.Color("coral"))
	return fps_text

WIDTH=1600
HEIGHT=900
screen=pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("just close this")
ACC=1.5
FRIC=-0.12
FPS=60

framePerSec=pygame.time.Clock()

playerSprite=pygame.image.load(str(os.path.join(os.getcwd(),'sprites\\ned.png')))

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=pygame.transform.scale(playerSprite, (100,60))
		
		self.pos=vec((400,HEIGHT-95))
		self.vel=vec(0,0)
		self.acc=vec(0,0)

	def move(self):
		self.acc=vec(0,0)

		pressedKeys=pygame.key.get_pressed()

		if pressedKeys[K_LEFT]:
			self.acc.x-=ACC
			#self.pos=vec((300,HEIGHT-95))  testing
		if pressedKeys[K_RIGHT]:
			self.acc.x=ACC
			#self.pos=vec((500,HEIGHT-95))  testing

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x>WIDTH:
			self.pos.x=WIDTH
		if self.pos.x<0:
			self.pos.x=0



class Platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf=pygame.Surface((WIDTH,50))
		self.surf.fill((50, 168, 82))
		self.rect=self.surf.get_rect(center=(WIDTH/2,HEIGHT-10))

PLAT1=Platform()
PLAYER=Player()

allSprites=pygame.sprite.Group()
allSprites.add(PLAT1)
allSprites.add(PLAYER)

running=True
while running:

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
			pygame.quit()
			sys.exit()

		screen.fill((64, 138, 207))

		PLAYER.move()

		for entity in allSprites:
			try:
				screen.blit(entity.image, entity.pos)
			except:
				screen.blit(entity.surf, entity.rect)

		#screen.blit(PLAYER.image, PLAYER.pos)
		#screen.blit(PLAT1.surf, PLAT1.rect)
		screen.blit(updateFPS(), (30,0))

		pygame.display.update()
		framePerSec.tick(FPS)

		pass

	


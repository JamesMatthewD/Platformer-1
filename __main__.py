import pygame, os, sys, random
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

playerSprite=pygame.image.load(str(os.path.join(os.getcwd(),'sprites\\ned.png'))).convert_alpha()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.pos=vec((400,HEIGHT-150))
		self.vel=vec(0,0)
		self.acc=vec(0,0)
		self.jumping=False

		self.image=pygame.transform.scale(playerSprite, (100,60))
		self.surf=pygame.Surface((100,60))
		self.rect=self.surf.get_rect(center=(self.pos.x, self.pos.y))
		self.surf.set_colorkey((0,0,0))
		self.surf.blit(self.image, (0,0))
		

	def move(self):
		self.acc=vec(0,0.5)

		pressedKeys=pygame.key.get_pressed()

		if pressedKeys[K_LEFT]:
			self.acc.x-=ACC
		if pressedKeys[K_RIGHT]:
			self.acc.x=ACC

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x>WIDTH:
			self.pos.x=0
		if self.pos.x<0:
			self.pos.x=WIDTH

		self.rect=self.surf.get_rect(center=(self.pos.x, self.pos.y))

	def jump(self):
		hits=pygame.sprite.spritecollide(PLAYER, platforms, False)
		if hits and not self.jumping:
			self.vel.y=-15
			self.jumping=True

	def cancelJump(self):
		if self.jumping:
			if self.vel.y<-3:
				self.vel.y=-3

	def update(self):
		hits=pygame.sprite.spritecollide(PLAYER, platforms, False)
		if PLAYER.vel.y > 0:
			if hits and not self.jumping:
				self.vel.y=0
				self.pos.y=hits[0].rect.top-29
			elif self.jumping==False:
				self.jumping=True
		if hits and self.jumping!=0:
			self.pos.y=hits[0].rect.top-29
			self.vel.y=0



class Platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf=pygame.Surface((random.randint(150,500),50))
		self.surf.fill((50, 168, 82))
		self.rect=self.surf.get_rect(center=(random.randint(0,WIDTH-50), random.randint(0,HEIGHT-50)))
	
	def move(self):
		pass

PLAT1=Platform()
PLAYER=Player()

allSprites=pygame.sprite.Group()
allSprites.add(PLAT1)
allSprites.add(PLAYER)

platforms=pygame.sprite.Group()
platforms.add(PLAT1)

for x in range(random.randint(4,8)):
	pl=Platform()
	platforms.add(pl)
	allSprites.add(pl)
PLAT1.surf=pygame.Surface((WIDTH, 50))
PLAT1.surf.fill((50,168,82))
PLAT1.rect=PLAT1.surf.get_rect(center=(WIDTH/2, HEIGHT-10))

def screenUpdate():
	for entity in allSprites:
		screen.blit(entity.surf, entity.rect)
		entity.move()


	screen.blit(updateFPS(), (30,0))
	pygame.display.update()
	framePerSec.tick(FPS)

def platGen():
	while len(platforms)<9:
		width=random.randrange(150,500)
		p=Platform()
		p.rect.center=(random.randrange(0,WIDTH-width), random.randrange(-50,0))
		platforms.add(p)
		allSprites.add(p)


running=True
while running:

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_SPACE or event.key==pygame.K_UP:
				PLAYER.jump()

		if event.type == pygame.KEYUP:
			if event.key==pygame.K_SPACE or event.key==pygame.K_UP:
				PLAYER.cancelJump()

	if framePerSec.get_fps()>30:
		screen.fill((64, 138, 207))
	else:
		screen.fill((255,0,0))

	if PLAYER.rect.top<=HEIGHT/3:
		PLAYER.pos.y+=abs(PLAYER.vel.y)
		for plat in platforms:
			plat.rect.y+=abs(PLAYER.vel.y)
			if plat.rect.top>=HEIGHT:
				plat.kill()

	platGen()
	PLAYER.update()	
	screenUpdate()



	


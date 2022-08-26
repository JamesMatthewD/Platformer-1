import pygame, os, sys, random, time
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
		self.score=0

		self.image=pygame.transform.scale(playerSprite, (100,60))
		self.surf=pygame.Surface((100,60))
		self.rect=self.surf.get_rect(center=(self.pos.x, self.pos.y))
		self.surf.set_colorkey((0,0,0))
		self.surf.blit(self.image, (0,0))
		

	def move(self):
		self.acc=vec(0,0.34)

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
			if hits:
				if self.pos.y < hits[0].rect.bottom:
					if hits[0].point==True:
						hits[0].point=False
						self.score+=1
					self.pos.y=hits[0].rect.top-29
					self.vel.y=0
					self.jumping=False


class Platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.moving=True
		self.point=True
		self.speed=random.random()
		if self.speed>0.7:
			self.speed=0
			while self.speed==0:
				self.speed=random.randint(-1,1)
		else:
			self.speed=0

		self.surf=pygame.Surface((random.randint(150,500),50))
		self.surf.fill((50, 168, 82))
		self.rect=self.surf.get_rect(center=(random.randint(0,WIDTH-50), random.randint(0,HEIGHT-50)))

		if self.speed!=0:
			self.surf.fill((201, 204, 37))
	
	def move(self):
		hits=self.rect.colliderect(PLAYER.rect)
		if self.moving==True:
			self.rect.move_ip(self.speed,0)
			if hits:
				PLAYER.pos+=(self.speed,0)
			if self.speed>0 and self.rect.left>WIDTH:
				self.rect.right=0
			if self.speed<0 and self.rect.right<0:
				self.rect.left=WIDTH

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
PLAT1.moving=False
PLAT1.point=False

def screenUpdate():
	for entity in allSprites:
		screen.blit(entity.surf, entity.rect)
		entity.move()


	screen.blit(updateFPS(), (30,0))
	pygame.display.update()
	framePerSec.tick(FPS)

def platGen():
	while len(platforms)<random.randint(6,10):
		width=random.randrange(150,500)
		p=Platform()
		C=True

		while C:
			p=Platform()
			p.rect.center=(random.randrange(0,WIDTH-width), random.randrange(-50,0))
			C=check(p,platforms)
			
		platforms.add(p)
		allSprites.add(p)

def check(platform, groupies):
	if pygame.sprite.spritecollideany(platform, groupies):
		return True
	else:
		for entity in groupies:
			if entity==platform:
				continue
			if (abs(platform.rect.top-entity.rect.bottom)<50) and (abs(platform.rect.bottom-entity.rect.top)<50):
				return True
			C=False


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

	font=pygame.font.SysFont("Comic Sans", 32)
	scoreDisplay=font.render(str(PLAYER.score),True, (189, 35, 219))
	screen.blit(scoreDisplay, (WIDTH/2, 50))

	if PLAYER.rect.top<=HEIGHT/3:
		PLAYER.pos.y+=abs(PLAYER.vel.y)
		for plat in platforms:
			plat.rect.y+=abs(PLAYER.vel.y)
			if plat.rect.top>=HEIGHT:
				plat.kill()

	if PLAYER.rect.top>HEIGHT:
		for entity in allSprites:
			entity.kill()
			time.sleep(1)
			screen.fill((255,0,0))
			pygame.display.update()
			time.sleep(1)
			pygame.quit()
			sys.exit()

	platGen()
	PLAYER.update()	
	screenUpdate()



	


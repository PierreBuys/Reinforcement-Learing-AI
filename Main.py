import pygame
import random
import sys
import time


pygame.init()


screen_width = 600
screen_height = 700


screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Rocket to Mars")
Game_Over_IMG = pygame.transform.scale(pygame.image.load("images/Game Over.png"), (300, 200))


class Rocket:

  def __init__(self):
    self.SIZE = 50
    self.X = ((screen_width - self.SIZE) // 2)
    self.Y = (screen_height - 100)
    self.SPEED = 5
    self.IMG = pygame.transform.scale(pygame.image.load("images/Rocket.png"), (50, 70))
    self.IMG_EX_1 = pygame.transform.scale(pygame.image.load("images/Explosion Stage 1.png"), (70, 70))
    self.IMG_EX_2 = pygame.transform.scale(pygame.image.load("images/Explosion Stage 2.png"), (80, 80))
    self.IMG_EX_3 = pygame.transform.scale(pygame.image.load("images/Explosion Stage 3.png"), (85, 85))
    self.IMG_EX_4 = pygame.transform.scale(pygame.image.load("images/Explosion Stage 4.png"), (80, 80))
    self.IMG_EX_5 = pygame.transform.scale(pygame.image.load("images/Explosion Stage 5.png"), (75, 75))
    self.MISSILES = []

  def move_left(self):
    if self.X > 0:
      self.X -= self.SPEED

  def move_right(self):
    if self.X < screen_width - 50:
      self.X += self.SPEED

  def shoot(self):
    missile = Missile(self.X + 22, self.Y)
    if len(self.MISSILES) == 0:
      self.MISSILES.append(missile)



rocket = Rocket()

class Missile:

  def __init__(self, x, y):
    self.X = x
    self.Y = y
    self.ACTIVE = True
    self.SPEED = 5
    self.SIZE = (3,10)

  def move(self):
    self.Y -= self.SPEED
    if self.Y < 0:
      self.ACTIVE = False
      rocket.MISSILES.pop()

  def draw(self, screen):
    pygame.draw.rect(screen, (255, 255, 255), (self.X, self.Y, self.SIZE[0], self.SIZE[1]))


class Asteroid:

  def __init__(self):
    self.ASTEROIDS = []
    self.SPAWN_RATE = 50
    self.SPEED = 3
    self.IMG = pygame.transform.scale(pygame.image.load("images/Asteroid.png"), (50, 70))

  def create(self):
    if random.randint(1, self.SPAWN_RATE) == 1:
      asteroid_width = random.randint(30, 80)
      asteroid_height = asteroid_width
      asteroid_x = random.randint(0, screen_width - asteroid_width)
      self.ASTEROIDS.append([asteroid_x, 0, asteroid_width, asteroid_height])

  def draw(self, screen):
    for a in self.ASTEROIDS:
      resized_asteroid = pygame.transform.scale(asteroid.IMG, (a[2], a[3]))
      screen.blit(resized_asteroid, (a[0], a[1]))

  def move(self):
    for a in self.ASTEROIDS[:]:
      a[1] += self.SPEED
      if a[1] > screen_height:
        self.ASTEROIDS.remove(a)


class Star:

  def __init__(self):
    self.NUM = 40
    self.STARS = [[random.randint(0, screen_width), random.randint(0, screen_height), random.randint(1, 3)] for _ in range(self.NUM)]
    self.SPEED = 1

  def draw(self, screen):
    for s in star.STARS:
      pygame.draw.circle(screen, (255,255,255), (s[0], s[1]), s[2])

  def move(self):
    for s in self.STARS:
      s[1] += self.SPEED
      if s[1] > screen_height:  
        s[0] = random.randint(0, screen_width)
        s[1] = 0



asteroid = Asteroid()
star = Star()

running = True

while running:

  screen.fill((0,0,0))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False


  #GANE MECHANICS
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    rocket.move_left()
  if keys[pygame.K_RIGHT]:
    rocket.move_right()
  if keys[pygame.K_UP]:
    rocket.shoot()


  #STARS
  star.draw(screen)
  star.move()


  #ASTEROID
  asteroid.create()
  asteroid.draw(screen)
  asteroid.move()


  #MISSILE
  if len(rocket.MISSILES) > 0:
    rocket.MISSILES[0].move()
    if len(rocket.MISSILES) > 0:
      rocket.MISSILES[0].draw(screen)

  rocket.MISSILES = [m for m in rocket.MISSILES if m.ACTIVE]
  

  #ROCKET
  screen.blit(rocket.IMG, (rocket.X,rocket.Y))




  # Rocket -> Asteroid : Collision
  rocket_rect = pygame.Rect(rocket.X, rocket.Y, 30, 50)
  for a in asteroid.ASTEROIDS:
      asteroid_rect = pygame.Rect(a[0], a[1], a[2]-13, a[3]-13)
      if rocket_rect.colliderect(asteroid_rect):
          print("Game Over!")
          screen.blit(Game_Over_IMG, (screen_width//2-150,screen_height//2-120))
          screen.blit(rocket.IMG_EX_1, (rocket.X,rocket.Y))
          pygame.display.flip()
          time.sleep(0.5)
          screen.blit(rocket.IMG_EX_2, (rocket.X,rocket.Y))
          pygame.display.flip()
          time.sleep(0.3)
          screen.blit(rocket.IMG_EX_3, (rocket.X,rocket.Y))
          pygame.display.flip()
          time.sleep(0.3)
          screen.blit(rocket.IMG_EX_4, (rocket.X,rocket.Y))
          pygame.display.flip()
          time.sleep(0.3)
          screen.blit(rocket.IMG_EX_5, (rocket.X,rocket.Y))
          pygame.display.flip()
          time.sleep(1.5)
          running = False
  

  # Missile -> Asteroid : Collision
  if not (len(rocket.MISSILES) == 0):
    missile_rect = pygame.Rect(rocket.MISSILES[0].X, rocket.MISSILES[0].Y, rocket.MISSILES[0].SIZE[0], rocket.MISSILES[0].SIZE[0])
    for a in asteroid.ASTEROIDS:
      asteroid_rect = pygame.Rect(a[0], a[1], a[2]-5, a[3]-5)
      if missile_rect.colliderect(asteroid_rect):
        rocket.MISSILES[0].ACTIVE = False
        rocket.MISSILES.pop()
        asteroid.ASTEROIDS.remove(a)
        print("Collision!")



  pygame.display.flip()
  pygame.time.Clock().tick(30)



pygame.quit()
sys.exit()
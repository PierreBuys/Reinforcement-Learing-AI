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
    self.MISSILES = []

  def move_left(self):
    if self.X > 0:
      self.X -= self.SPEED

  def move_right(self):
    if self.X < screen_width - 50:
      self.X += self.SPEED

  def shoot(self):
    missile = Missile(self.X + 22, self.Y)
    self.MISSILES.append(missile)

  def check_collision(missile, asteroid):
    if (missile.X < asteroid.X + asteroid.SIZE[0] and
      missile.X + missile.SIZE[0] > asteroid.X and
      missile.Y < asteroid.Y + asteroid.SIZE[1] and
      missile.Y + missile.SIZE[1] > asteroid.Y):
      return True
    return False



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

  def draw(self, screen):
    pygame.draw.rect(screen, (255, 255, 255), (self.X, self.Y, self.SIZE[0], self.SIZE[1]))


class Asteroid:

  def __init__(self):
    self.ASTEROIDS = []
    self.SPAWN_RATE = 50
    self.SPEED = 3
    self.IMG = pygame.transform.scale(pygame.image.load("images/Asteroid.png"), (50, 70))


class Star:

  def __init__(self):
    self.NUM = 40
    self.STARS = [[random.randint(0, screen_width), random.randint(0, screen_height), random.randint(1, 3)] for _ in range(self.NUM)]
    self.SPEED = 1



rocket = Rocket()
asteroid = Asteroid()
star = Star()

running = True

while running:

  screen.fill((0,0,0))


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False


  for s in star.STARS:
    s[1] += star.SPEED
    if s[1] > screen_height:  
      s[0] = random.randint(0, screen_width)
      s[1] = 0

  for s in star.STARS:
    pygame.draw.circle(screen, (255,255,255), (s[0], s[1]), s[2])


  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    rocket.move_left()
  if keys[pygame.K_RIGHT]:
    rocket.move_right()
  if keys[pygame.K_UP]:
    rocket.shoot()

  for m in rocket.MISSILES:
    m.move()
    m.draw(screen)

  rocket.MISSILES = [m for m in rocket.MISSILES if m.ACTIVE]

  if random.randint(1, asteroid.SPAWN_RATE) == 1:
    asteroid_width = random.randint(30, 80)
    asteroid_height = asteroid_width
    asteroid_x = random.randint(0, screen_width - asteroid_width)
    asteroid.ASTEROIDS.append([asteroid_x, 0, asteroid_width, asteroid_height])


  for a in asteroid.ASTEROIDS[:]:
    a[1] += asteroid.SPEED
    if a[1] > screen_height:
      asteroid.ASTEROIDS.remove(a)

  for a in asteroid.ASTEROIDS:
    resized_asteroid = pygame.transform.scale(asteroid.IMG, (a[2], a[3]))
    screen.blit(resized_asteroid, (a[0], a[1]))

  rocket_rect = pygame.Rect(rocket.X, rocket.Y, 30, 50)
  for a in asteroid.ASTEROIDS:
      asteroid_rect = pygame.Rect(a[0], a[1], a[2]-13, a[3]-13)
      if rocket_rect.colliderect(asteroid_rect):
          print("Game Over!")
          screen.blit(Game_Over_IMG, (screen_width//2-150,screen_height//2-120))
          pygame.display.flip()
          time.sleep(1.5)
          running = False

  
  screen.blit(rocket.IMG, (rocket.X,rocket.Y))

  pygame.display.flip()
  pygame.time.Clock().tick(30)





pygame.quit()
sys.exit()
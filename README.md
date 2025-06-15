# stormfield - A Pygame Library
<img src="logo.png" alt="Alt text" width="1000" />

**Stormfield aims to partially recreate Love2D's windfield physics library.** <br/>
**The main idea behind it is to easily intergrate collisions in your game**

## Features
✅ Collision system with separation <br/>
✅ Collider friction <br/>
✅ Collider types: static, dynamic, kinematic <br/>
✅ Collision classes with ignore rule <br/>
✅ Collision events <br/>

## Instalation
```
git clone https://github.com/clxakz/stormfield/
```

## Example Usage
### In your main.py
```python
import pygame
from stormfield import World

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Initialize world with 0 gravity since this example will be topdown movement
world = World(0)

# Create collision classes
world.addCollisionClass("Player")
world.addCollisionClass("Wall")

running = True
while running:
    screen.fill((0,0,0))
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update world
    world.update(dt)

    pygame.display.flip()
pygame.quit()
```

### Next let's create a player script
```python
import pygame
from stormfield import World

class Player(pygame.sprite.Sprite):
    def __init__(self, world: World):
        super().__init__()
        self.world = world

        self.sprite = pygame.Surface((100, 100))
        self.sprite.fill((255,0,0))

        self.rect = pygame.FRect(250, 250, 100, 100)

        # Create a phyisics collider
        self.collider = self.world.addCollider(self.rect, "Player", self, "dynamic", 1000)

        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dir = pygame.Vector2(0, 0)

        if keys[pygame.K_w]: dir.y -= 1
        if keys[pygame.K_a]: dir.x -= 1
        if keys[pygame.K_s]: dir.y += 1
        if keys[pygame.K_d]: dir.x += 1

        if dir.length() > 0:
            dir = dir.normalize() * self.speed
            # Apply linear velocity to rect
            self.world.setLinearVelocity(self.collider, dir)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)
```

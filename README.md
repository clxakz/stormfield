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

## Usage
**In your main.py** <br/>
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

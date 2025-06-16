# stormfield - A Pygame Library
**Stormfield aims to partially recreate Love2D's windfield physics library.** <br/>
**The main idea behind it is to easily intergrate collisions in your game**

<img src="logo.png" alt="Alt text" width="1000" />


## Instalation
```bash
git clone https://github.com/clxakz/stormfield/
```
or
```bash
pip install stormfield
```

# Quick Start
place the `stormfield` folder inside your project and import it:
```python
from stormfield import World
```

# Create a world
A physics world can be created similarly to windfield
```python
world = World(pygame.Vector2(0, 500))
```

# Create collider
A collider is a single object that attaches to your sprite
```python
box = world.newRectangleCollider(300, 350, 100, 100)
box.setRestitution(0.8)
box.applyLinearImpulse(pygame.Vector2(0, 1000))

ground = world.newRectangleCollider(100, 600, 600, 100)
ground.setType("static") # <- Types can be 'static', 'dynamic' or 'kinematic'. Defaults to 'dynamic'

# In your main loop
world.draw(screen) # <- The world can be drawn for debugging purposes
```
And that looks like this


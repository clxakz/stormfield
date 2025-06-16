# stormfield - A Pygame Library
**Stormfield aims to partially recreate Love2D's windfield physics library.** <br/>
**The main idea behind it is to easily intergrate collisions in your game**

<img src="assets/logo.png" alt="Alt text" width="1000" />

> [!NOTE]
> `Stormfield` is still in development, some expected features may not be present.

> [!IMPORTANT]
> The main reason i created `stormfield` was to easily manage collisions and collision classes, **NOT** to handle full physics — although some physics features are present.

-----

# Contents
- [Instalation](#instalation)
- [Quick Start](#quick-start)
  - [Create a world](#create-a-world)
  - [Create colliders](#create-colliders)
- [Documentation](#documentation)
    - [World](#world)
      - [New World](#worldgravity)
      - [Collision classes](#addcollisionclassname-ignores)
      - [Draw](#drawscreen-color-width)
      - [New Rectangle Collider](#newrectanglecolliderx-y-width-height)
      - [Destroy](#destroy)
    - [Rectangle Collider](#rectangle-collider)
      - [Set Linear Velocity](#setlinearvelocityvelocity)
      - [Apply Linear Impluse](#applylinearimpulseimpulse)
      - [Set Friction](#setfrictionfriction)
      - [Set Mass](#setmassmass)
      - [Set Restitution](#setrestitutionrestitution)
      - [Set Type](#settypetype)
      - [Set Object](#setobjectobj)
      - [Set Collision Class](#setcollisionclassname)

-----

## Instalation
```bash
git clone https://github.com/clxakz/stormfield/
```
or
```bash
pip install stormfield
```

-----

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

# Create colliders
A `collider` is an object that handles collision detection and can be attached to your game entities or sprites.
```python
box = world.newRectangleCollider(300, 350, 100, 100)
box.setRestitution(0.8)
box.applyLinearImpulse(pygame.Vector2(0, 1000))

ground = world.newRectangleCollider(100, 600, 600, 100)
ground.setType("static") # <- Types can be 'static', 'dynamic' or 'kinematic'. Defaults to 'dynamic'

# In your main loop
world.update(dt)
world.draw(screen) # <- The world can be drawn for debugging purposes
```
And that looks like this: <br/>

<img src="assets/demo1.gif" alt="Alt text" width="500" />

-----

# Documentation

## World
### `World(gravity)`
The `World` class is the core of the Stormfield collision system.
It manages all `colliders`, updates their positions, resolves collisions, and handles collision class logic.

`Stormfield’s World` object is inspired by the `windfield` library in LÖVE2D, focusing on ease of use and flexibility for collision handling in Pygame.
```python
world = World(pygame.Vector2(0, 500))
```

Arguments:
- `gravity` `(pygame.Vector2)` - The gravity for all of your collider objects

-----

### `.addCollisionClass(name, ignores)`
A `collision class` is a way to group colliders and control which objects should interact with each other.
You can assign a collision class to each collider, and configure which classes should ignore collisions with others. This allows you to easily manage complex collision relationships without writing custom logic for every case.
```python
world.addCollisionClass("Player")
world.addCollisionClass("Enemies", ["Walls"]) # <- The enemy class will ignore all objects in the 'Walls' class
world.addCollisionClass("Walls")

collider.setCollisionClass("Player") # <- Assigns a collision class to your object
```

Arguments:
- `name` `(str)` - The name of a collision class
- `ignores` `(list[str])` - A list of other classes a class should ignore

-----

### `.draw(screen, color, width)`
The draw() function allows you to quickly visualize all colliders in the world by drawing their shapes on the screen using pygame.draw.rect().
This is mainly useful for debugging and development purposes.
```python
world.draw(screen, (255,255,255), 1)
```

Arguments:
- `screen` `(pygame.Surface)` - The surface where all colliders should be drawn
- `color` `(tuple)` - RGB color of the outline
- `width` `(int)` - The width of the outline

-----

### `.newRectangleCollider(x, y, width, height)`
Creates a new rectangle collider and automatically adds it to the world.
```python
box = world.newRectangleCollider(0, 0, 100, 100)
```

Arguments:
- `x` `(int)` - The X position of the collider
- `y` `(int)` - The Y position of the collider
- `width` `(int)` - The width of the collider
- `height` `(int)` - The height of the collider

-----

### `.destroy()`
The destroy() function will clear all colliders, collision classes and resets the gravity.
```python
world.destroy()
```

-----

## Rectangle Collider

### `.setLinearVelocity(velocity)`
Sets the linear velocity vector of the collider. This controls how fast and in what direction the collider moves each frame.
```python
collider.setLinearVelocity(pygame.Vector2(100, 0))
```
Arguments:
- `velocity` `(pygame.Vector2)` — The velocity vector to apply.

-----

### `.applyLinearImpulse(impulse)`
Applies an instantaneous impulse to the collider, changing its velocity immediately based on the impulse and the collider’s mass. Only affects colliders of type "dynamic".
```python
collider.applyLinearImpulse(pygame.Vector2(0, 500))
```

Arguments:
- `impulse` `(pygame.Vector2)` — The impulse vector to apply.

-----

### `.setFriction(friction)`
Sets the friction coefficient for the collider, which slows it down over time when moving.
```python
collider.setFriction(0.5)
```

Arguments:
- `friction` `(float)` — The friction value. Higher values mean more friction.

-----

### `.setMass(mass)`
Sets the mass of the collider, which affects how impulses change its velocity.
```python
collider.setMass(2.0)
```

Arguments:
- `mass` `(float)` — The mass value (must be positive).

-----

### `.setRestitution(restitution)`
Sets the restitution (bounciness) of the collider. Determines how much velocity is retained after collisions.
```python
collider.setRestitution(0.8)
```

Arguments:
- restitution (float) — A value between 0 (no bounce) and 1 (perfect bounce).

-----

### `.setType(type)`
Sets the physics type of the collider. Types control whether the collider moves and how:

"static" — Does not move and does not respond to forces.
"dynamic" — Moves according to velocity, forces, and collisions.
"kinematic" — Moves only via velocity but does not respond to forces or collisions.
```python
collider.setType("static")
```

Arguments:
- `type` `(str)` — One of "static", "dynamic", or "kinematic".

-----

### `.setObject(obj)`
Associates a custom Python object with the collider, usually the game entity or sprite it belongs to. Useful for accessing your entity during collision callbacks.
```python
collider.setObject(player)
```

Arguments:
- `obj` `(any)` — Your custom object reference.

-----

### `.setCollisionClass(name)`
Assigns a collision class to the collider to manage which other colliders it can interact with.
```python
collider.setCollisionClass("Player")
```

Arguments:
- `name` `(str)` — The name of the collision class.

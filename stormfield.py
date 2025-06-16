#MIT License
#
#Copyright (c) 2025 clxakz
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import pygame
from typing import Literal

class RectangleCollider():
    def __init__(self, x, y, width, height):
        self.rect = pygame.FRect(x, y, width, height)
        self.velocity = pygame.Vector2(0, 0)
        self.friction = 0
        self.type: Literal["static", "dynamic", "kinematic"] = "dynamic"

        self.mass = 1.0
        self.restitution = 0.0

        self._object = self
        self.colliding_with = set()
        
        # Callback placeholders
        self.onCollisionEnter = None
        self.onCollisionExit = None
        self.onCollisionStay = None

        self.collision_class = None


    def setLinearVelocity(self, velocity: pygame.Vector2) -> None:
        self.velocity = velocity

    
    def applyLinearImpulse(self, impulse: pygame.Vector2) -> None:
        if self.type == "dynamic" and self.mass > 0:
            velocity_change = impulse / self.mass
            self.velocity += velocity_change


    def setFriction(self, friction: float) -> None:
        self.friction = friction


    def setMass(self, mass: float) -> None:
        self.mass = mass

    def setRestitution(self, restitution: float) -> None:
        if not 0 <= restitution <= 1:
            raise ValueError("Restitution must be between 0 and 1")
        self.restitution = restitution

    
    def setType(self, type: Literal["static", "dynamic", "kinematic"]) -> None:
        allowed = ["static", "dynamic", "kinematic"]
        
        if type not in allowed:
            raise ValueError(f"Invalid type '{type}'. Allowed types: {allowed}")
        
        self.type = type

    
    def setObject(self, obj) -> None:
        self._object = obj


    def _getObject(self) -> any:
        return self._object
    

    def setCollisionClass(self, name) -> None:
        self.collision_class = name


    def _update(self, dt, gravity) -> None:
        if self.type == "dynamic":
            self.__updateGravity(dt, gravity)
            self.__updateFriction(dt)
            self.rect.center += self.velocity * dt

        elif self.type == "kinematic":
            self.rect.center += self.velocity * dt


    def __updateGravity(self, dt, gravity) -> None:
        self.velocity += gravity * dt


    def __updateFriction(self, dt) -> None:
        if self.velocity.length_squared() > 0:
            friction_force = self.velocity.normalize() * (-self.friction)
            self.velocity += friction_force * dt




class World():
    def __init__(self, gravity: pygame.Vector2):
        self.gravity = gravity
        self.colliders: list[RectangleCollider] = []
        self.collision_classes = {}


    def destroy(self) -> None:
        # Clear all colliders
        self.colliders.clear()

        # Clear collision class definitions
        self.collision_classes.clear()

        # Reset gravity if desired
        self.gravity = pygame.Vector2(0, 0)


    def addCollisionClass(self, name: str, ignores: list[str] | None = None) -> None:
        if ignores is None:
            ignores = []
        self.collision_classes[name] = set(ignores)


    def __ignores(self, class_a, class_b) -> bool:
        return class_b in self.collision_classes.get(class_a, set())


    def draw(self, screen: pygame.Surface, color = (255,255,255), width = 1) -> None:
        for collider in self.colliders:
            pygame.draw.rect(screen, color, collider.rect, width)
    

    def newRectangleCollider(self, x, y, width, height) -> RectangleCollider:
        collider = RectangleCollider(x, y, width, height)
        self.colliders.append(collider)
        return collider
    

    def update(self, dt) -> None:
        for collider in self.colliders:
            collider._update(dt, self.gravity)

        self.__resolveCollisions()

    
    def __resolveCollisions(self) -> None:
        collisions_this_frame = {}
        num_colliders = len(self.colliders)
        
        # Detect collisions and separate
        for i in range(num_colliders):
            for j in range(i + 1, num_colliders):
                a = self.colliders[i]
                b = self.colliders[j]

                # Check if collision classes ignore each other
                if a.collision_class and b.collision_class:
                    if self.__ignores(a.collision_class, b.collision_class) or self.__ignores(b.collision_class, a.collision_class):
                        continue

                if a.rect.colliderect(b.rect):
                    collisions_this_frame.setdefault(a, set()).add(b)
                    collisions_this_frame.setdefault(b, set()).add(a)
                    self.__separate(a, b)

        # Handle collision callbacks: Enter, Stay, Exit
        for collider in self.colliders:
            current = collisions_this_frame.get(collider, set())
            previous = collider.colliding_with

            # Collisions that started this frame (Enter)
            entered = current - previous
            for other in entered:
                if callable(collider.onCollisionEnter):
                    collider.onCollisionEnter(other._getObject())

            # Collisions that continued this frame (Stay)
            stayed = current.intersection(previous)
            for other in stayed:
                if callable(collider.onCollisionStay):
                    collider.onCollisionStay(other._getObject())

            # Collisions that ended this frame (Exit)
            exited = previous - current
            for other in exited:
                if callable(collider.onCollisionExit):
                    collider.onCollisionExit(other._getObject())

            # Update collider's currently colliding set
            collider.colliding_with = current

            
    def __separate(self, a, b) -> None:
        if a.type == "static" and b.type == "static":
            return

        dx = a.rect.centerx - b.rect.centerx
        dy = a.rect.centery - b.rect.centery
        overlap_x = (a.rect.width + b.rect.width) / 2 - abs(dx)
        overlap_y = (a.rect.height + b.rect.height) / 2 - abs(dy)

        combined_restitution = (a.restitution + b.restitution) / 2
        threshold = 0.1

        def apply_bounce(v):
            if abs(v) < threshold:
                return 0
            return -v * combined_restitution

        if overlap_x < overlap_y:
            move = overlap_x if dx > 0 else -overlap_x
            self.__distributeMovement(a, b, move, axis="x")

            if a.type != "static":
                a.velocity.x = apply_bounce(a.velocity.x)
            if b.type != "static":
                b.velocity.x = apply_bounce(b.velocity.x)
        else:
            move = overlap_y if dy > 0 else -overlap_y
            self.__distributeMovement(a, b, move, axis="y")

            if a.type != "static":
                a.velocity.y = apply_bounce(a.velocity.y)
            if b.type != "static":
                b.velocity.y = apply_bounce(b.velocity.y)


    def __distributeMovement(self, a, b, move, axis) -> None:
        movable_a = (a.type != "static")
        movable_b = (b.type != "static")

        if movable_a and movable_b:
            # both can move
            move_a = move / 2
            move_b = -move / 2
        elif movable_a:
            move_a = move
            move_b = 0
        elif movable_b:
            move_a = 0
            move_b = -move
        else:
            move_a = 0
            move_b = 0

        if axis == "x":
            a.rect.x += move_a
            b.rect.x += move_b
        else:
            a.rect.y += move_a
            b.rect.y += move_b
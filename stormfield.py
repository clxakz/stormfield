import pygame

class World:
    def __init__(self, gravity=9.8):
        self.gravity = gravity
        self.collision_classes = {}
        self.colliders = []


    def addCollisionClass(self, name, ignores=None):
        if ignores is None:
            ignores = []
        self.collision_classes[name] = {
            "ignores": ignores,
            "colliders": []
        }


    def addCollider(self, rect, collision_class, owner, collider_type="dynamic", friction=0):
        collider = {
            "rect": rect,
            "class": collision_class,
            "type": collider_type,
            "velocity": pygame.Vector2(0, 0),
            "friction": friction,
            "current_colliders": [],
            "previous_colliders": [],
            "owner": owner
        }
        self.colliders.append(collider)
        self.collision_classes[collision_class]["colliders"].append(collider)
        return collider


    def applyGravity(self, dt):
        for collider in self.colliders:
            if collider["type"] == "dynamic":
                collider["velocity"].y += self.gravity * dt


    def moveColliders(self, dt):
        for collider in self.colliders:
            if collider["type"] in ("dynamic", "kinematic"):
                # Apply friction (drag)
                if collider["friction"] > 0:
                    friction_force = collider["friction"] * dt
                    collider["velocity"].x -= min(abs(collider["velocity"].x), friction_force) * (1 if collider["velocity"].x > 0 else -1)
                    collider["velocity"].y -= min(abs(collider["velocity"].y), friction_force) * (1 if collider["velocity"].y > 0 else -1)
                
                move = collider["velocity"] * dt
                collider["rect"].x += move.x
                collider["rect"].y += move.y


    def checkCollisions(self):
        # Clear current collisions first for all colliders
        for collider in self.colliders:
            collider["current_colliders"].clear()

        # Then do collision checks and fill current_collisions sets
        checked_pairs = set()

        for class_name_a, class_data_a in self.collision_classes.items():
            for class_name_b, class_data_b in self.collision_classes.items():
                if class_name_b in class_data_a["ignores"]:
                    continue
                if class_name_a in class_data_b["ignores"]:
                    continue

                for c1 in class_data_a["colliders"]:
                    for c2 in class_data_b["colliders"]:
                        if c1 is c2:
                            continue

                        pair = tuple(sorted((id(c1), id(c2))))
                        if pair in checked_pairs:
                            continue
                        checked_pairs.add(pair)

                        if c1["rect"].colliderect(c2["rect"]):
                            self.resolveCollision(c1, c2)

                            c1["current_colliders"].append(c2)
                            c2["current_colliders"].append(c1)


    def resolveCollision(self, c1, c2):
        r1, r2 = c1["rect"], c2["rect"]
        overlap = r1.clip(r2)

        # Priority: static > kinematic > dynamic
        # Static colliders do not move.
        # Kinematic colliders can move but are not pushed by dynamic.
        # Dynamic colliders are pushed by static and kinematic.

        types = (c1["type"], c2["type"])

        # Cases:
        # 1. Static vs Dynamic -> push Dynamic
        # 2. Static vs Kinematic -> push Kinematic
        # 3. Kinematic vs Dynamic -> push Dynamic
        # 4. Dynamic vs Dynamic -> simple separation

        # Determine who is pushed (moved) and who is static (or unmovable)
        if "static" in types:
            if c1["type"] == "static":
                moving = c2
                static = c1
            else:
                moving = c1
                static = c2
            self.pushOut(moving, static, overlap)
        elif "kinematic" in types:
            if c1["type"] == "kinematic" and c2["type"] == "dynamic":
                self.pushOut(c2, c1, overlap)
            elif c2["type"] == "kinematic" and c1["type"] == "dynamic":
                self.pushOut(c1, c2, overlap)
            else:
                # both kinematic or dynamic, just separate equally for simplicity
                self.pushOutDynamicPair(c1, c2, overlap)
        else:
            # both dynamic: separate both (equal push)
            self.pushOutDynamicPair(c1, c2, overlap)


    def pushOut(self, moving, static, overlap):
        r1, r2 = moving["rect"], static["rect"]
        if overlap.width < overlap.height:
            if r1.centerx < r2.centerx:
                r1.right = r2.left
            else:
                r1.left = r2.right
        else:
            if r1.centery < r2.centery:
                r1.bottom = r2.top
            else:
                r1.top = r2.bottom


    def pushOutDynamicPair(self, c1, c2, overlap):
        # Push both colliders apart equally
        r1, r2 = c1["rect"], c2["rect"]
        if overlap.width < overlap.height:
            shift = overlap.width / 2
            if r1.centerx < r2.centerx:
                r1.right -= shift
                r2.left += shift
            else:
                r1.left += shift
                r2.right -= shift
        else:
            shift = overlap.height / 2
            if r1.centery < r2.centery:
                r1.bottom -= shift
                r2.top += shift
            else:
                r1.top += shift
                r2.bottom -= shift


    def applyLinearImpulse(self, collider, impulse: pygame.Vector2):
        collider["velocity"] += impulse


    def setLinearVelocity(self, collider, velocity: pygame.Vector2):
        collider["velocity"] = pygame.Vector2(velocity)


    def colliderEnter(self, collider, collision_class):
        return (
            any(c["class"] == collision_class for c in collider["current_colliders"])
            and not any(c["class"] == collision_class for c in collider["previous_colliders"])
            )


    def getEnterCollisionData(self, collider, collision_class):
        entered = [
            c for c in collider["current_colliders"] 
            if c not in collider["previous_colliders"] and c["class"] == collision_class
        ]
        return [c["owner"] for c in entered]


    def update(self, dt):
        for collider in self.colliders:
            collider["previous_colliders"] = collider["current_colliders"].copy()

        self.applyGravity(dt)
        self.moveColliders(dt)
        self.checkCollisions()


    def draw(self, screen, color=(255, 255, 255), width=1):
        for collider in self.colliders:
            pygame.draw.rect(screen, color, collider["rect"], width)

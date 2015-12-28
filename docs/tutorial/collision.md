All objects have two methods `collision` and `on_collision`.


## Collision

This check if objects is in colision with another object. This returns `True` or `False`

## On colision

On colision is a event method. This is called from `MoveAction` and `MultipleMoveAction` when `collision` methods returns `True`.


## Create another Object

On your `objects.py` create a wall object at the end of file:

```py
class Wall(Object):
    x = 10
    y = 10
    width = 20
    height = 10
    color = 'blue'
    char = '~'
```

And add it to scene:

```py
# ...
# Import wall
from objects import Wall

class Scene(BaseScene):
    def __init__(self, *args, **kwargs):
        # ...
        # Add Wall object 
        self.wall = Wall()
        self.add_object(self.scene.wall)

```

## Blocking ball move in ball

Update your move methods of ball.


``` py
    def up(self):
        self.y -= 1
        if self.colision(self.scene.wall):
            self.y += 1

    def down(self):
        self.y += 1
        if self.colision(self.scene.wall):
            self.y -= 1

    def left(self):
        self.x -= 1
        if self.colision(self.scene.wall):
            self.x += 1

    def right(self):
        self.x += 1
        if self.colision(self.scene.wall):
            self.x -= 1
```

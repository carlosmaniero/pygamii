Actions are a Thread based class. This is started by the Scene and all actions have the scene atribute.

## Standard Actions:

See a list of standard actions (pygamii.action), to use in your project.

- **`BaseKeyboard`**: This is a keyboard action.
- **`MoveAction`**: Used to move a specific object.
- **`MultipleMoveAction`**: used to move all objects in your scene.


## Controlling the Ball

We will use the `BaseKeyboard` to control our ball using the keyboard.

Firstily, we will create the move methods in our Ball class.

```py
class Ball(Object):
    # the same content ...

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1
```


Create your `actions.py` file with this content:


```py
from pygamii.action import BaseKeyboard


class Keyboard(BaseKeyboard):
    def handler(self, key):
        if key == 'w':
            self.scene.ball.up()
        elif key == 's':
            self.scene.ball.down()
        elif key == 'a':
            self.scene.ball.left()
        elif key == 'd':
            self.scene.ball.right()
        elif key == 'q':
            self.scene.stop()

```

## Add the Keyboard in scene.

```py
from pygamii.scene import BaseScene
from objects import Ball
from actions import Keyboard


class Scene(BaseScene):
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.ball = Ball()
        self.add_object(self.ball)
        self.add_action(Keyboard)
```

Now, we can controll the ball with the keyboard using the keys (`w`, `a`, `s`, `d`) and quit the game on `q` key is pressed;

---

**Note**:  

- The `add_action`, possibly will be changed to be used like Objects (Passing a instance) in the beta version.  So, we recommend don't override the `__init__` from actions to use the scene instance, use the `on_create` method for it.  
- The `pygamii.action` will be changed to `pygamii.actions` in the beta version.
- For while pygamii don't support arrow keys.

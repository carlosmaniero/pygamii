To create an object, import the Object class inside `pygamii.objects` package.
We will create an object called ball, this will be contains 1x1 chars, will be red and your character will be an asterisk.

Create an file called `objects.py` for it.

## Create a ball Object
```py
from pygamii.objects import Object


class Ball(Object):
    width = 1
    height = 1
    x = 0
    y = 0
    color = 'red'
    char = '*'
```

Now we need add the object to the scene.


## Add the ball to the scene
```py
from pygamii.scene import BaseScene
from objects import Ball


class Scene(BaseScene):
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.ball = Ball()
        self.add_object(self.ball)


if __name__ == '__main__':
    scene = Scene()
    scene.start()
```

Run the `game.py` and you will see a red asterisk in the first col and first row (0, 0) of scene.


## Create a custom character made object

To render an object in the scene, the `__str__` (`str()`) method is called. By default the `__str__` method is:

```py
def __str__(self):
    return (self.get_char() * self.width + '\n') * self.height
```

So, if we change our Ball class to the below:


```py
class Ball(Object):
    width = 5
    height = 3
    x = 0
    y = 0
    color = 'red'
    char = '*'
```

The result will be:

    *****
    *****
    *****

This isn't a ball! For create a ball, you will need override the `__str__` method.


```py
class Ball(Object):
    width = 5
    height = 3
    x = 0
    y = 0
    color = 'red'

    def __str__(self):
        return ' *** \n*****\n *** '
```

## Make the `__str__` readable

The above example isn't readable, we can't know what is the figure of object. 
To improvement it, follow the below code:


```py
class Ball(Object):
    width = 5
    height = 3
    x = 0
    y = 0
    color = 'red'
    to_render = '\n'.join([
        ' *** ',
        '*****',
        ' *** ',
    ])

    def __str__(self):
        return self.to_render
```

This will generate:

     ***
    *****
     ***
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     ▊

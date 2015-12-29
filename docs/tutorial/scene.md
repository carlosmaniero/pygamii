To start your project, you need to create a file called `game.py`.  
This file will contains the scene of your game. Scene is the space where your objects will be rendered.

```py
from pygamii.scene import BaseScene


class Scene(BaseScene):
    pass

if __name__ == '__main__':
    scene = Scene()
    scene.start()
```


By default, scene contains 80x23 chars. 
When 80 is the num of cols and 23 the number of rows.

Now we will go the `game.py`:

    $ python game.py

You will see your console be cleaned. And a cursor in the 24 row. 

# PyGamii
Pygamii is a ascii game engine, created to make games in console.

[![Documentation Status](https://readthedocs.org/projects/pygamii/badge/?version=develop)](http://pygamii.readthedocs.org/en/develop/?badge=develop)

# Docs:

[http://pygamii.readthedocs.org/en/develop/](http://pygamii.readthedocs.org/en/develop/)

## Instalation
Clone this repository and run setup.py.

    python setup.py install

To use Audio Library, you need install PyGame http://www.pygame.org/download.shtml

## Examples
In examples path, you will found Arkanoid.

### Arkanoid
![Arkanoid](https://raw.githubusercontent.com/carlosmaniero/pygamii/develop/examples/arkanoid/screenshots/arkanoid-main.png)
![Arkanoid](https://raw.githubusercontent.com/carlosmaniero/pygamii/develop/examples/arkanoid/screenshots/arkanoid-game.png)

Click in the below image and see this in action.

[![Arkanoid Video](http://img.youtube.com/vi/QcgN2pBfaU0/0.jpg)](http://www.youtube.com/watch?v=QcgN2pBfaU0)

To run Arkanoid example, enter in your directory [examples/arkanoid](examples/arkanoid) and run:
    
    python arkanoid.py

## Notes
This is a alpha version, I create it using Python3 and Linux.
Compatibility errors may occur.


# News
## version 0.0.1.5 - Alpha
- Change the BaseKeyboard action to use curses.
- Change the add_action to use an object not a class.
- Improviments in the PyGamii


## version 0.0.1.4 - Alpha
- Change the render method to use the curses standard library.

## version 0.0.1.3 - Alpha
- Add on_create and on_destoy signals on object and action
- Add gun gift on Flycombat
- Add video of Arkanoid example (Thank you Yu-Jie Lin)
- Start Docs
- fix type error: colision -> collision

## version 0.0.1.2 - Alpha
- Add MultipleMoveAction: For control movement
- Fix Object.colision method
- Start Flycombat example
- Add Volume Control support in Audio class

## version 0.0.1 - Alpha
- Start of project

# TODO for 0.1 version Beta
- Complete the Flycombat game
    - Make a Boss
    - Make the splash and ending of the game.
- Documentation Review




![Logo Pygamii](docs/img/logo.png)

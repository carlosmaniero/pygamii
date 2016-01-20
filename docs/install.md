To install Pygamii, you will need to clone the repository from git and install.  
We're working to provide the instalation via pip :)

    $ git clone https://github.com/carlosmaniero/pygamii
    $ cd pygamii
    $ python setup.py install

## Virtualenv

Is recommended the installation inside a virtualenv. We use 
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html).

    $ mkvirtualenv pygamii
    $ git clone https://github.com/carlosmaniero/pygamii
    $ cd pygamii
    $ python setup.py install

When you need to activate the virtualenv use the bellow command:

    $ workon pygamii

## Audio Interface

For audio interface, Pygamii uses the audio module from [Pygame](http://www.pygame.org).
To install Pygame, follow the link:

[http://www.pygame.org/wiki/GettingStarted](http://www.pygame.org/wiki/GettingStarted)

## Compatibility

This is compatible with Linux consoles, we test it on:

- `gnome-terminal`
- `xterm`
- `zsh`

For while, Windows is not supported.

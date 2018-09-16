from setuptools import setup

with open('requirements.txt') as f:
    reqs = f.read().strip().split('\n')

setup(name='pygamii',
      version='0.0.1.4',
      description='Create ASCII games with Python',
      url='http://github.com/carlosmaniero/pygamii',
      author='Carlos Maniero',
      author_email='carlosmaniero@gmail.com',
      license='MIT',
      packages=['pygamii'],
      install_requires=reqs,
      zip_safe=False)

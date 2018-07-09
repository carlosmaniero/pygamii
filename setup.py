from setuptools import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

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

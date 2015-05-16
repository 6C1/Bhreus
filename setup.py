try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'Bhreus',
    'description': 'A tiny browser engine',
    'author': 'Cooper Stimson',
    'url': 'github.com/6c1/bhreus',
    'author_email': 'cooper@cooperstimson.com',
    'version': '0.1.0',
    'install_requires': ['nose'],
    'packages': ['bhreus'],
    'scripts': [],
}

setup(**config)

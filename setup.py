from setuptools import find_packages, setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()


"""
Build Info:
python3 -m build
twine upload dist/*
"""


setup(
    name='shade-sdk',
    packages=find_packages(),
    version='v0.0.1-beta',
    license='MIT',

    description="Shade SDK",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Shade',
    author_email='shade@shade.inc',

    url='https://github.com/open-shade/python-sdk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
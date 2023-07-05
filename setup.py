from setuptools import find_packages, setup

setup(
    name='promptprocessing',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'pandas',
        'pytest'
        ],
)

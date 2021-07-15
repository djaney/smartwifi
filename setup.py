from setuptools import setup


setup(
    name='smartwifi',
    version='',
    packages=['smartwifi'],
    url='',
    license='',
    author='thedjaney',
    author_email='thedjaney@gmail.com',
    description='Autoswitch wifi depending on strength',
    entry_points={
        'console_scripts': ['smartwifi=smartwifi.smartwifi:main'],
    },
)

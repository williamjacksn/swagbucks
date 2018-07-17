from setuptools import find_packages, setup

setup(
    name='swagbucks',
    version='1.0.0',
    author='William Jackson',
    author_email='william@subtlecoolness.com',
    url='https://github.com/williamjacksn/swagbucks',
    description='Swagbucks',
    license='MIT License',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'swagbucks = swagbucks.swagbucks:main'
        ]
    }
)

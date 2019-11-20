#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8") as f:
    description = f.read()

setup(name='minecraft-launcher-lib',
    version='0.2',
    description=' A library for creating a custom Minecraft launcher',
    long_description=description,
    long_description_content_type='text/markdown',
    author='JakobDev',
    author_email='jakobdev@gmx.de',
    url='https://gitlab.com/JakobDev/minecraft-launcher-lib',
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    license='BSD',
    keywords=['JakobDev','Minecraft','Mojang','launcher','minecraft-launcher','java'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'License :: OSI Approved :: BSD License',
        'Topic :: Games/Entertainment',
        'Operating System :: OS Independent',
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
 )


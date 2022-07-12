#!/usr/bin/env python3
from setuptools import setup
from pathlib import Path


with open(Path(__file__).parent / "minecraft_launcher_lib" / "version.txt", "r", encoding="utf-8") as f:
    version = f.read().strip()

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(name="minecraft-launcher-lib",
      version=version,
      description="A library for creating a custom Minecraft launcher",
      long_description=description,
      long_description_content_type="text/markdown",
      author="JakobDev",
      author_email="jakobdev@gmx.de",
      url="https://gitlab.com/JakobDev/minecraft-launcher-lib",
      python_requires=">=3.8",
      include_package_data=True,
      install_requires=[
          "requests",
      ],
      packages=["minecraft_launcher_lib"],
      license="BSD",
      keywords=["JakobDev", "Minecraft", "Mojang", "launcher", "minecraft-launcher", "java"],
      project_urls={
          "Issue tracker": "https://gitlab.com/JakobDev/minecraft-launcher-lib/-/issues",
          "Documentation": "https://minecraft-launcher-lib.readthedocs.io/en/stable/index.html",
          "Changelog": "https://minecraft-launcher-lib.readthedocs.io/en/stable/changelog.html",
          "Donation": "https://ko-fi.com/jakobdev",
      },
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Environment :: Other Environment",
          "License :: OSI Approved :: BSD License",
          "Topic :: Games/Entertainment",
          "Operating System :: OS Independent",
          "Operating System :: POSIX",
          "Operating System :: POSIX :: BSD",
          "Operating System :: POSIX :: Linux",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ],
)

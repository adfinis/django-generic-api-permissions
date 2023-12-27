# -*- coding: utf-8 -*-

from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-generic-api-permissions",
    version="0.3.0",
    author="adfinis",
    description="Generic API permissions and visibilities for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adfinis/django-generic-api-permissions",
    license="License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    packages=["generic_permissions"],
    install_requires=["django>=3.2"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

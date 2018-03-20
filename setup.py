#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="mkgreg",
    version="1.3",
    description="Making Greg's systems awesome",
    long_description="A set of scripts and Ansible playbooks to make Greg's" +
                     " systems awesome",
    url="https://github.com/greg-hellings/config",
    author="Gregory Hellings",
    license="GPLv3",
    classifiers=[
        "Development Status :: 5- Stable",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved : GNU General Public License v3 (GPLv3)"
    ],
    keywords="me, myself, I",
    packages=find_packages(exclude=("library", "bin")),
    install_package_data=True,
    install_requires=[
        "ansible>=2.4",
        "plumbum>=1.6.0"
    ],
    entry_points={
        'console_scripts': [
            "mkgreg-gui=mkgreg.bin.mkgreg:mkgreg_gui",
            "mkgreg-cli=mkgreg.bin.mkgreg:mkgreg_cli",
            "mkgreg-dev=mkgreg.bin.mkgreg:mkgreg_dev",
            "mkgreg-user=mkgreg.bin.mkgreg:mkgreg_user",
            "mkgreg=mkgreg.bin.mkgreg:mkgreg"
        ]
    }
)

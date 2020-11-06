import os
import sys
from setuptools import find_packages, setup
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

about = {}
with open(os.path.join(here, 'pyuac', '__version__.py'), 'r', encoding='utf-8') as fh:
    exec(fh.read(), about)

install_requires = ['tee']

if "win" in sys.platform:
    try:
        import win32file
    except ImportError:
        # Only require pywin32 if not already installed
        # version 223 introduced ability to install from pip
        install_requires.append("pywin32>=224")

setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages(include=['pyuac']),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    install_requires=install_requires,
    test_suite='tests',
    url=about['__url__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        # 'Documentation': '',
        'Source': 'https://github.com/Preston-Landers/pyuac',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)

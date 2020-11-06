import sys
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ['tee']

if "win" in sys.platform:
    try:
        import win32file
    except ImportError:
        # Only require pywin32 if not already installed
        # version 223 introduced ability to install from pip
        install_requires.append("pywin32>=224")

setup(
    name='pyuac',
    version='0.9.0',
    packages=find_packages(include=['pyuac']),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    install_requires=install_requires,
    test_suite='tests',
    url='https://github.com/Preston-Landers/pyuac',
    license='MIT',
    author='Preston Landers',
    author_email='planders@utexas.edu',
    description='Python library for Windows User Access Control (UAC)',
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

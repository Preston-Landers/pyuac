import sys
from setuptools import find_packages, setup

install_requires = ['tee']

if "win" in sys.platform:
    try:
        import win32file
    except ImportError:
        # Only require pywin32 if not already installed
        # version 223 introduced ability to install from pip
        install_requires.append("pywin32>=224")

#
# Classifiers
# python_requires?
#     long_description=readme,
#     long_description_content_type='text/markdown',

setup(
    name='pyuac',
    version='0.9.0',
    packages=find_packages(include=['pyuac']),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=6.1.2'],
    test_suite='tests',
    url='https://github.com/Preston-Landers/pyuac',
    license='MIT',
    author='Preston Landers',
    author_email='planders@utexas.edu',
    description='Python library for Windows User Access Control (UAC)',
    project_urls={
        # 'Documentation': '',
        'Source': 'https://github.com/Preston-Landers/pyuac',
    },
)

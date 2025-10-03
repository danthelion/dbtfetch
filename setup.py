#!/usr/bin/env python3
"""Setup configuration for dbtfetch."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='dbtfetch',
    version='1.0.1',
    author='Daniel Palma',
    author_email='danivgy@gmail.com',
    description='A neofetch-style system information tool for dbt projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/danthelion/dbtfetch',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    install_requires=[
        'PyYAML>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'dbtfetch=dbtfetch.cli:main',
        ],
    },
    keywords='dbt data analytics neofetch statistics',
    project_urls={
        'Bug Reports': 'https://github.com/danthelion/dbtfetch/issues',
        'Source': 'https://github.com/danthelion/dbtfetch',
    },
)
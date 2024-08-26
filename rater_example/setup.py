from setuptools import setup, find_packages

setup(
    name='rater',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    extra_requires={
        "dev": ["pytest==8.3.2"]
    },
    entry_point={
        'console_scripts':[],
    },
    author='Christopher Andersen',
    author_email='ctandersen@gmail.com',
    description='This package implements a premium rating for a simple D&O insurance product',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ctandersen/counterpart_interview',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating Syteme :: OS Independent',
    ],
    python_requires='>=3.10',
)


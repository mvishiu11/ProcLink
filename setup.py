from setuptools import setup, find_packages

setup(
    name='ProcLink',
    version='0.1.0',
    description='A lightweight package for inter-process communication',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jakub Muszynski',
    packages=find_packages(),
    install_requires=[
        'pyzmq>=22.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
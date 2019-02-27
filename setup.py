from setuptools import setup, find_packages

setup(
    name="soon",
    version="0.1",
    author="Lukas Šalkauskas",
    python_requires='>=3.7.0',
    author_email="halfas.online@gmail.com",
    packages=find_packages(
        exclude=[
            'tests'
        ]
    ),
    install_requires=[
        "futures >= 2.2.0"
    ],
    description="""
        Worker decorator for background tasks re-using ThreadPoolExecutor.
    """,
    license="MIT License (See LICENSE)",
    long_description=open("README.md").read(),
    url="https://github.com/dotpot/soon"
)

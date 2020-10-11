import setuptools

setuptools.setup(
    name = "pathe_api",
    version = "0.2",
    author = "Jorn Brinksma",
    description = "Wrapper module for Pathe Cinema's API.",
    packages=setuptools.find_packages(include=['pathe_api']),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

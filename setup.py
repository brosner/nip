from distutils.core import setup


setup(
    name = "nip",
    version = "0.1a1",
    py_modules = [
        "nip",
    ],
    scripts = [
        "bin/nip",
    ],
    author = "Brian Rosner",
    author_email = "brosner@gmail.com",
    description = "nip is environment isolation and installation for Node.js",
    long_description = open("README.rst").read(),
    license = "MIT",
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
    ],
)

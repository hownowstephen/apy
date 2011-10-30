from setuptools import setup, find_packages

setup(
    name = "apy",
    version = "0.2.1",
    author = "Stephen Young",
    author_email = "stephen@tryllo.com",
    description = ("Pythonic API development with flask"),
    url = "https://github.com/stephenyoung/apy/wiki",
    packages= ['apy'],
    install_requires=[
        'flask>=0.8.0',
        'oauth2>=1.5'
    ],
)
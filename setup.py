from setuptools import setup, find_packages

setup(
    name = "apy",
    version = "0.0.1",
    author = "Stephen Young",
    author_email = "stephen@tryllo.com",
    description = ("Pythonic API development with flask"),
    url = "https://github.com/getmelisted/fetch/wiki",
    packages= ['apy'],
    install_requires=[
        'flask>=8.0',
        'oauth2>=1.5'
    ],
)
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "SlackConnector",
    version = "0.0.4",
    author="HyeonGyu Lee",
    author_email="vazrupe@gmail.com",
    description="Slack Rtm Client",
    license = "MIT",
    keywords = "slack rtm",
    url = "https://github.com/vazrupe/SlackConnector",
    packages=['SlackConnector', ],
    install_requires=['slacker', 'websocket-client', ],
    long_description=read('README.md')
)

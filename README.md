# SlackConnector
Simple Slack Rtm Connector with python3

# Installation

    pip install --upgrade git+https://github.com/vazrupe/SlackConnector.git

# Quick Start

```
from SlackConnector import Rtm

slack_token = 'YOUR SLACK BOT TOKEN'
client = rtm(slack_token)
client.message_recv = print

client.run_forever()
```

# Requirement

* [websocket-client>=0.40.0](https://pypi.python.org/pypi/websocket-client/)
* [slacker>=0.9.30](https://pypi.python.org/pypi/slacker/)

# License
MIT

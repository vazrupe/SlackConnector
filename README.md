# SlackConnector
Simple Slack Rtm Connector with python3

# Installation

    pip install --upgrade git+https://github.com/vazrupe/SlackConnector.git

# Usage

```
from SlackConnector import Rtm

slack_token = 'YOUR SLACK BOT TOKEN'
client = rtm(slack_token)
client.message_recv = print

# non-blocking
client.connect(True)
time.sleep(1)
client.send('YOUR MESSAGE', 'YOUR_CHANNEL')
time.sleep(1)
client.disconnect()

# blocking
client.connect()
```


# Requirement

* [websocket-client>=0.40.0](https://pypi.python.org/pypi/websocket-client/)
* [slacker>=0.9.30](https://pypi.python.org/pypi/slacker/)

# License
MIT

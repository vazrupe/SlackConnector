from SlackConnector import rtm

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

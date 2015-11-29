bitfinexpy
======
Python wrapper for Bitfinex API.

Dependencies
======
Requests and Pandas libraries are required.

Usage
======

Include the bitfinexpy module and create an bitfinexpy instance with your account credentials. For trading, a key and a secret key must be provided.

	import bitfinexpy

	bitfinex = bitfinexpy.API(environment="live", key="AaBbCc012...", secret_key="123a456...")

**Method names are referred by the part of HTML label name after #, which you can see [Bitfinex API web page](http://docs.bitfinex.com/).**

**In the label name, you don't forget to replace all '-'s with '_'.** (e.g. multiple-new-orders -> multiple_new_orders)


Examples
======

### Get the latest BTCUSD price
	bitfinex.ticker(symbol='BTCUSD')

### View your active orders
    bitfinex.active_orders()

### See your balances
    bitfinex.wallet_balances()

### Submit a new order
For example, if you'd like to buy 0.001 BTC as 0.01 BTC/USD, you need to specify following parameters.

	bitfinex.new_order(symbol="BTCUSD", amount=0.001, price=0.01, side="buy", type="market")


BTC Price Streaming
======
Create a custom streamer class to setup how you want to handle the data.
Each tick is sent through the `on_success` and `on_error` functions.
You can override these functions to handle the streaming data.

Initialize an instance of your custom streamer, and start connecting to the stream.

    stream = bitfinexpy.Streamer(environment=DOMAIN, heartbeat=1.0)
    stream.start()



Copyright (c) 2015 jimako1989

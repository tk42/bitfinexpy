# -*- coding: utf-8 -*-
""" BITFINEX API wrapper """

"""
AUTHOR: @jimako1989
GITHUB: github.com/jimako1989/bitfinexpy
LICENSE: MIT
"""

import json,time,hmac,hashlib,requests,datetime,base64

"""EndpointsMixin provides a mixin for the API instance """
class EndpointsMixin(object):

    """Public API"""
    def ticker(self, **params):
        """ Gives innermost bid and asks and information on the most recent trade, as well as high, low and volume of the last 24 hours.
        Docs: https://docs.bitfinex.com/v1/reference#rest-public-ticker
        """
        symbol = params.pop('symbol')
        endpoint = 'pubticker/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def stats(self, **params):
        """ Various statistics about the requested pair.
        Docs: http://docs.bitfinex.com/#stats
        """
        symbol = params.pop('symbol')
        endpoint = 'stats/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def fundingbook(self, **params):
        """ Get the full margin funding book.
        Docs: http://docs.bitfinex.com/#fundingbook
        """
        symbol = params.pop('symbol')
        endpoint = 'lendbook/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def orderbook(self,**params):
        """ Get the full order book.
        Docs: http://docs.bitfinex.com/#orderbook
        """
        symbol = params.pop('symbol')
        endpoint = 'book/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def trades(self,**params):
        """ Get a list of the most recent trades for the given symbol.
        Docs: http://docs.bitfinex.com/#trades
        """
        symbol = params.pop('symbol')
        endpoint = 'trades/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def lends(self,**params):
        """ Get a list of the most recent funding data for the given currency: total amount lent and Flash Return Rate (in % by 365 days) over time.
        Docs: http://docs.bitfinex.com/#lends
        """
        symbol = params.pop('symbol')
        endpoint = 'book/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def symbols(self,**params):
        """ Get a list of valid symbol IDs.
        Docs: http://docs.bitfinex.com/#symbols
        """
        symbol = params.pop('symbol')
        endpoint = 'book/'+symbol
        return self.request(endpoint, auth=False, params=params)

    def symbol_details(self,**params):
        """ Get a list of valid symbol IDs and the pair details.
        Docs: http://docs.bitfinex.com/#symbol-details
        """
        symbol = params.pop('symbol')
        endpoint = 'book/'+symbol
        return self.request(endpoint, auth=False, params=params)


    """ Private API """
    """ Account """
    def account_infos(self, **params):
        """ Check the balance.
        Docs: http://docs.bitfinex.com/#account-info
        """
        endpoint = 'account_infos'
        return self.request(endpoint, payload_params=params)

    """ Deposit """
    def deposit(self, **params):
        """ Return your deposit address to make a new deposit.
        Docs: http://docs.bitfinex.com/#deposit
        """
        endpoint = 'deposit/new'
        return self.request(endpoint, payload_params=params)

    """ Order """
    def new_order(self, symbol, amount, price, side, order_type, **params):
        """ Submit a new order.
        Docs: http://docs.bitfinex.com/#new-order
        """
        endpoint = 'order/new'
        params['symbol'] = symbol
        params['amount'] = amount
        params['price'] = price
        params['side'] = side
        params['type'] = order_type
        params['exchange'] = 'bitfinex'
        return self.request(endpoint, method='POST', payload_params=params)

    def multiple_new_orders(self, orders, **params):
        """ Submit several new orders at once.
        Docs: http://docs.bitfinex.com/#new-order
        """
        endpoint = 'order/new/multi'
        params['orders']=json.dumps(orders)
        return self.request(endpoint, method='POST', payload_params=params)

    def cancel_order(self, order_id, **params):
        """ Cancel an order.
        Docs: http://docs.bitfinex.com/#cancel-order
        """
        endpoint = 'order/cancel'
        params['oder_id'] = order_id
        return self.request(endpoint, method='POST', payload_params=params)

    def cancel_multiple_orders(self, order_ids, **params):
        """ Cancel multiples orders at once.
        Docs: http://docs.bitfinex.com/#cancel-multiple-orders
        """
        endpoint = 'order/cancel/multi'
        params['order_ids'] = order_ids
        return self.request(endpoint, method='POST', payload_params=params)

    def cancel_all_orders(self, **params):
        """ Cancel multiples orders at once.
        Docs: http://docs.bitfinex.com/#cancel-all-orders
        """
        endpoint = 'order/cancel/all'
        return self.request(endpoint, method='POST', payload_params=params)

    def replace_order(self, order_id, symbol, amount, price, side, order_type, **params):
        """ Replace an orders with a new one.
        Docs: http://docs.bitfinex.com/#replace-orders
        """
        endpoint = 'order/cancel/replace'
        params['order_id'] = order_id
        params['symbol'] = symbol
        params['amount'] = amount
        params['price'] = price
        params['side'] = side
        params['type'] = order_type
        params['exchange'] = 'bitfinex'
        return self.request(endpoint, method='POST', payload_params=params)

    def order_status(self, order_id, **params):
        """ Get the status of an order. Is it active? Was it cancelled? To what extent has it been executed? etc.
        Docs: http://docs.bitfinex.com/#order-status
        """
        endpoint = 'order/status'
        params['order_id'] = order_id
        return self.request(endpoint, method='POST', payload_params=params)

    def active_orders(self, **params):
        """ View your active orders.
        Docs: http://docs.bitfinex.com/#active-orders
        """
        endpoint = 'orders'
        return self.request(endpoint, method='POST', payload_params=params)

    """ Positions """
    def active_positions(self, **params):
        """ View your active positions.
        Docs: http://docs.bitfinex.com/#active-positions
        """
        endpoint = 'positions'
        return self.request(endpoint, method='POST', payload_params=params)

    def claim_position(self, position_id, **params):
        """ A position can be claimed if:
        It is a long position:
            The amount in the last unit of the position pair that you have in your trading wallet AND/OR the realized profit of the position is greater or equal to the purchase amount of the position (base price * position amount) and the funds which need to be returned.
            For example, for a long BTCUSD position, you can claim the position if the amount of USD you have in the trading wallet is greater than the base price * the position amount and the funds used.
        It is a short position:
            The amount in the first unit of the position pair that you have in your trading wallet is greater or equal to the amount of the position and the margin funding used.
        Docs: http://docs.bitfinex.com/#claim-position
        """
        endpoint = 'position/claim'
        params['position_id'] = position_id
        return self.request(endpoint, method='POST', payload_params=params)

    """ Historical Data """
    def balance_history(self, currency, **params):
        """ View all of your balance ledger entries.
        Docs: http://docs.bitfinex.com/#balance-history
        """
        endpoint = 'history'
        params['currency'] = currency
        return self.request(endpoint, method='POST', payload_params=params)

    def deposit_withdrawal_history(self, currency, **params):
        """ View all of your balance ledger entries.
        Docs: http://docs.bitfinex.com/#balance-history
        """
        endpoint = 'history/movements'
        params['currency'] = currency
        return self.request(endpoint, method='POST', payload_params=params)

    def past_trades(self, symbol, **params):
        """ View all of your balance ledger entries.
        Docs: http://docs.bitfinex.com/#balance-history
        """
        endpoint = 'mytrades'
        params['symbol'] = symbol
        return self.request(endpoint, method='POST', payload_params=params)

    """ Margin Funding """
    def new_offer(self, currency, amount, rate, period, direction, **params):
        """ Submit a new offer.
        Docs: http://docs.bitfinex.com/#new-offer
        """
        endpoint = 'offer/new'
        params['currency'] = currency
        params['amount'] = amount
        params['rate'] = rate
        params['period'] = period
        params['direction'] = direction
        return self.request(endpoint, method='POST', payload_params=params)

    def cancel_offer(self, offer_id, **params):
        """ Cancel an offer.
        Docs: http://docs.bitfinex.com/#cancel-offer
        """
        endpoint = 'offer/cancel'
        params['offer_id'] = offer_id
        return self.request(endpoint, method='POST', payload_params=params)

    def offer_status(self, offer_id, **params):
        """ Get the status of an offer. Is it active? Was it cancelled? To what extent has it been executed? etc.
        Docs: http://docs.bitfinex.com/#offer-status
        """
        endpoint = 'offer/status'
        params['offer_id'] = offer_id
        return self.request(endpoint, method='POST', payload_params=params)

    def active_credits(self, **params):
        """ View your active offers.
        Docs: http://docs.bitfinex.com/#active-credits
        """
        endpoint = 'offers'
        return self.request(endpoint, method='POST', payload_params=params)

    def active_funding_used_in_a_margin_position(self, **params):
        """ View your funding currently borrowed and used in a margin position.
        Docs: http://docs.bitfinex.com/#active-funding-used-in-a-margin-position
        """
        endpoint = 'taken_funds'
        return self.request(endpoint, method='POST', payload_params=params)

    def total_taken_funds(self, **params):
        """ View the total of your active-funding used in your position(s).
        Docs: http://docs.bitfinex.com/#total-taken-funds
        """
        endpoint = 'total_taken_funds'
        return self.request(endpoint, method='POST', payload_params=params)

    def close_margin_funding(self, **params):
        """ Return the funding taken in a margin position.
        Docs: http://docs.bitfinex.com/#total-taken-funds
        """
        endpoint = 'funding/close'
        return self.request(endpoint, method='POST', payload_params=params)

    """ Wallet Balances """
    def wallet_balances(self, **params):
        """ See your balances.
        Docs: http://docs.bitfinex.com/#wallet-balances
        """
        endpoint = 'balances'
        return self.request(endpoint, method='POST', payload_params=params)

    """ Margin Information """
    def margin_information(self, **params):
        """ See your trading wallet information for margin trading.
        Docs: http://docs.bitfinex.com/#margin-information
        """
        endpoint = 'margin_infos'
        return self.request(endpoint, method='POST', payload_params=params)

    """ Transfer Between Wallets """
    def offer_status(self, amount, currency, walletfrom, walletto, **params):
        """ Allow you to move available balances between your wallets.
        Docs: http://docs.bitfinex.com/#margin-information
        """
        endpoint = 'transfer'
        params['amount'] = amount
        params['currency'] = currency
        params['walletfrom'] = walletfrom
        params['walletto'] = walletto
        return self.request(endpoint, method='POST', payload_params=params)

    """ Withdrawal """
    def withdrawal(self, withdraw_type, walletselected, amount, **params):
        """ Allow you to request a withdrawal from one of your wallet.
        Docs: http://docs.bitfinex.com/#withdrawal
        """
        endpoint = 'withdraw'
        params['withdraw_type'] = withdraw_type
        params['walletselected'] = walletselected
        params['amount'] = amount
        return self.request(endpoint, method='POST', payload_params=params)



""" Provides functionality for access to core BITFINEX API calls """

class API(EndpointsMixin, object):
    def __init__(self, environment='live', key=None, secret_key=None):
        """ Instantiates an instance of BitfinexPy's API wrapper """

        if environment == 'live':
            self.api_url = 'https://api.bitfinex.com/v1/'
        else:
            # for future, access to a demo account.
            pass

        self.key = key
        self.secret_key = bytes(secret_key, 'utf-8')

        self.client = requests.Session()

    def request(self, endpoint, method='GET', auth=True, params=None, payload_params=None):
        """ Returns dict of response from Bitfinex's open API """
        method = method.lower()

        url = '%s%s' % ( self.api_url, endpoint)

        request_args = {'params':params}

        if auth:
            payloadObject = {
                "request": "/v1/%s" % endpoint,
                "nonce": str(time.time() * 1000000) # update nonce each POST request
            }
            if payload_params is not None:
                payloadObject.update(payload_params)
            payload = base64.b64encode(bytes(json.dumps(payloadObject), "utf-8"))
            signature = hmac.new(self.secret_key, msg=payload, digestmod=hashlib.sha384).hexdigest()
            request_args['headers'] = {
                'X-BFX-APIKEY': self.key,
                'X-BFX-PAYLOAD': payload,
                'X-BFX-SIGNATURE': signature
            }
            #request_args['data'] = {}

        func = getattr(self.client, method)
        try:
            response = func(url, **request_args)
        except Exception as e:
            print("Failed to get the response because %s. \
			      The request url is %s"%(str(e),url))

        content = response.json()

        # error message
        if response.status_code >= 400:
            print("%s error_response : %s"%(str(response.status_code),content))
            raise BitfinexError(response.status_code,content)

        return content


"""HTTPS Streaming"""
class Streamer():
    """ Provides functionality for HTTPS Streaming """

    def __init__(self, symbol, environment='live', heartbeat=1.0):
        """ Instantiates an instance of BitfinexPy's streaming API wrapper. """

        if environment == 'live':
            self.api_url = 'https://api.bitfinex.com/v1/pubticker/'+symbol
        else:
            # for future, access to a demo account.
            pass

        self.heartbeat = heartbeat

        self.client = requests.Session()


    def start(self, **params):
        """ Starts the stream with the given parameters """
        self.connected = True

        request_args = {}

        content_ = {'last':None,'bid':None,'volume':None,'ask':None,'low':None,'high':None}

        while self.connected:
            response = self.client.get(self.api_url, **request_args)
            content = response.content.decode('ascii')
            content = json.loads(content)

            if response.status_code != 200:
                self.on_error(content)

            # when the tick is updated
            if any([content[key] != content_[key] for key in ['last', 'bid', 'volume', 'ask', 'low', 'high']]):
                self.on_success(content)
                content_ = content

            time.sleep(self.heartbeat)

    def on_success(self, content):
        """ Called when data is successfully retrieved from the stream """
        print(content)
        return True

    def on_error(self, content):
        """ Called when stream returns non-200 status code
        Override this to handle your streaming data.
        """
        self.connected = False
        return


""" Contains BITFINEX exception """
class BitfinexError(Exception):
    """ Generic error class, catches bitfinex response errors
    """

    def __init__(self, status_code, error_response):
        msg = "BITFINEX API returned error code %s (%s)" % (status_code, error_response['error'])

        super(BitfinexError, self).__init__(msg)

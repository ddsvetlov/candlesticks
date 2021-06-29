import unittest

from kindlestick import (
	generate_stream_url,
	calculate_avg,
	BASE_URL,
	TOKEN_PAIRS,
)


class TestKindlestick(unittest.TestCase):

	test_list = [0,1,2,3,4,5,6,7,8]
	test_url = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m/btcusdt@kline_1m/bnbbtc@kline_1m'
	def test_generate_stream_url(self):
	    self.assertEqual(
	    	generate_stream_url(
	    		base_url=BASE_URL, 
	    		token_pairs=TOKEN_PAIRS
	    		), self.test_url)

	def test_calculate_avg(self):
	    self.assertEqual(calculate_avg(self.test_list), 4)


if __name__ == "__main__":
	unittest.main()

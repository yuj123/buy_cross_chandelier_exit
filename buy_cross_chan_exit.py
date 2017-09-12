import datetime
import os.path
import sys
import pandas as pd
import backtrader as bt

def read_csv(datapath):
	return pd.read_csv(datapath, parse_dates=True, index_col=0)

# Create a Stratey
class BuyChandelierStrategy(bt.Strategy):

	params = (
		('stake', 100),
	)

	def log(self, txt, dt=None):
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		self.sizer.setsizing(self.params.stake)
	
		# Keep a reference to the "close" line in the data[0] dataseries
		self.dataclose1  = self.datas[0].close
		self.high        = self.datas[0].high
		self.chan_exit_l = bt.ind.Highest(self.high, period=22) - 3 * bt.ind.ATR(period=22) 
		self.rsa         = bt.ind.RSI_SMA(period=14)

	def next(self):
		
		if  self.dataclose1[0] < self.chan_exit_l[0] and \
			self.dataclose1[-1] >= self.chan_exit_l[-1] and \
			self.rsa <= 35:
			
			self.log('BUY CREATE, price=%.2f chan=%.2f  %.2f' % (
				self.dataclose1[0], 
				self.chan_exit_l[0], 
				self.rsa[0], 
				))
			
			self.buy()
				
	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
			# Buy/Sell order submitted/accepted to/by broker - Nothing to do
			return

		# Check if an order has been completed
		# Attention: broker could reject order if not enougth cash
		if order.status in [order.Completed]:
			if order.isbuy():
				self.log(
					'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
					(order.executed.price,
					 order.executed.value,
					 order.executed.comm))

				self.buyprice = order.executed.price
				self.buycomm = order.executed.comm
			else:  # Sell
				self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
						 (order.executed.price,
						  order.executed.value,
						  order.executed.comm))

			self.bar_executed = len(self)

		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		self.order = None

	def notify_trade(self, trade):
		if not trade.isclosed:
			return

		self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
				 (trade.pnl, trade.pnlcomm))				
				 
def backtest(sid):
	
	# Read CSV (From Yahoo) to Pandas dataframe
	df1 = read_csv("%s.HK.csv" % sid)

	# Some Yahoo dataframe had zero volume, exclude them
	df1 = df1[df1.Volume != 0]
	
	# Back test the BuyChandelierStrategy with BackTrader
	cerebro = bt.Cerebro()
	
	cerebro.broker.setcash(1000000.0)
	cerebro.broker.setcommission(commission=0.0035)
	cerebro.addstrategy(BuyChandelierStrategy)
	
	data = bt.feeds.PandasData(dataname=df1)
	cerebro.adddata(data)
	
	startValue = cerebro.broker.getvalue()
	print('Starting Portfolio Value: %.2f' % startValue)
	
	cerebro.run()
	
	endValue = cerebro.broker.getvalue()
	print('Final Portfolio Value: %.2f' % endValue)
	
	perc = (endValue - startValue) / startValue * 100
	
	# Print percentage change in the value
	print("pct_chg(%s)=%.2f%%" % (sid, perc))
	
				
def main():
	# Backtest a list of HKEX stocks.
	sidList = ["0027", "0066", "0762", "1038", "1928", "2318", "2388"]

	for sid in sidList:
		backtest(sid)
		
if __name__ == "__main__":
	main()
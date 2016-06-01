__author__ = 'Corey Petty'
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls

# Bring your packages onto the path
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'poloniex')))
# Now do your import
import poloniex as polo
from api_key import key, secret
# (*) Import module keep track and format current time
import time

api = polo.Poloniex(APIKey=key, Secret=secret)

stream_ids = tls.get_credentials_file()['stream_ids']
stream_id, stream_id2 = stream_ids[0], stream_ids[1]

# Make instance of stream id object
stream_1 = go.Stream(
    token=stream_id,  # link stream id to 'token' key
    maxpoints=80      # keep a max of 80 pts on screen
)
stream_2 = go.Stream(
    token=stream_id2,
    maxpoints=80
)
# # Initialize trace of streaming plot by embedding the unique stream_id
# trace1 = go.Scatter(
#     x=[],
#     y=[],
#     mode='lines',
#     stream=stream_1         # (!) embed stream id, 1 per trace
# )
#
# trace2 = go.Scatter(
#     x=[],
#     y=[],
#     mode='lines',
#     stream=stream_2
# )
#
# data = go.Data([trace1, trace2])
# # Add title to layout object
# layout = go.Layout(title='Polo BTC/ETH Depth Chart')
#
# # Make a figure object
# fig = go.Figure(data=data, layout=layout)
#
# # Send fig to Plotly, initialize streaming plot, open new tab
# py.iplot(fig, filename='Polo_plots/depth_chart')

# We will provide the stream link object the same token that's associated with the trace we wish to stream to
s = py.Stream(stream_id)
s2 = py.Stream(stream_id2)

# We then open a connection
s.open()
s2.open()

# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)

while True:
    ethBook = pd.DataFrame(api.api('returnOrderBook', {'currencyPair': 'BTC_ETH', 'depth': 1000}))
    ask_prices = []
    ask_amounts = []
    bid_prices = []
    bid_amounts = []
    for (ask_price, ask_amount), (bid_price, bid_amount) in zip(ethBook.asks.values,ethBook.bids.values):
        ask_prices.append(float(ask_price))
        ask_amounts.append(float(ask_amount))
        bid_prices.append(float(bid_price))
        bid_amounts.append(float(bid_amount))
    df = pd.DataFrame({'ask_price': ask_prices, 'ask_amount': ask_amounts, 'bid_price': bid_prices, 'bid_amount': bid_amounts})
    df['ask_amount_cum'] = df.ask_amount.cumsum()
    df['bid_amount_cum'] = df.bid_amount.cumsum()
    # Current time on x-axis, random numbers on y-axis
    x = df.ask_price.values
    y = df.ask_amount_cum.values
    x2 = df.bid_price.values
    y2 = df.bid_amount_cum.values
    # Send data to your plot
    s.write(dict(x=x, y=y))
    s2.write(dict(x=x2, y=y2))
    #     Write numbers to stream to append current data on plot,
    #     write lists to overwrite existing data on plot
# Close the stream when done plotting
s.close()
s2.close()

import streamlit as st
import yfinance as yf
from datetime import datetime , date
from utils import chart, db
from PIL import Image
import matplotlib.pyplot as plt
from vega_datasets import data
from pandas_datareader.data import DataReader



img = Image.open('images/Stockx_logo.png')

# PAGE CONFIGURATION'
st. set_page_config(page_title="StockX")
padding = 1
v = 2.5
st.markdown(f""" <style>
    .appview-container .main .block-container{{
        padding-top: {padding}rem;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .css-1oe6wy4 {{padding-top : {v}rem ;}}
    .css-1kyxreq {{justify-content : center;
    margin-bottom : 1rem;}}
     </style> """, unsafe_allow_html=True)

# SIDEBAR
st.sidebar.image(img,width=150)
# st.sidebar.title("STOCKX")
st.sidebar.success("Welcome To StockX !!")

# BODY
st.write("""# STOCK PREDICTIONS :chart_with_upwards_trend: """)

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")
###########################################

# Data visualisation part

source = data.stocks()
all_symbols = source.symbol.unique()
symbols = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:2])

space(1)

source = source[source.symbol.isin(symbols)]
chart = chart.get_chart(source)
st.altair_chart(chart, use_container_width=True)

space(2)


########################################################
# def get_ticker(name):
#     company = yf.Ticker(name)
#     return company

# c1 = get_ticker("AAPL")
# c2 = get_ticker("MSFT")
# c3 = get_ticker("TSLA")

# apple = yf.download("AAPL",start="2021-11-11",end="2021-11-11")
# microsoft = yf.download("MSFT",start="2021-11-11",end="2021-11-11")
# tesla = yf.download("TSLA",start="2021-11-11",end="2021-11-11")

# data1 = c1.history(period="3mo")
# data2 = c2.history(period="3mo")
# data3 = c3.history(period="3mo")


user_input = st.text_input('Enter Stock Ticker',placeholder="ex: AAPL")
if(user_input):
    def get_ticker(user_input):
        company = yf.Ticker(user_input)
        return company

    c = get_ticker(user_input) 
    co_name = yf.download(user_input,start="2021-11-11",end="2021-11-11")

    data = c.history(period="3mo")

    st.write(c.info['longBusinessSummary'])
    space(2)
    st.write(co_name)
    space(2)
    st.line_chart(data.values)

# st.write(""" ### Apple """)
# space(1)
# st.write(c1.info['longBusinessSummary'])
# space(2)
# st.write(apple)
# st.line_chart(data1.values)
space(4)
####################################################
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
stocks = ('GOOG', 'AAPL', 'MSFT', 'GME','TSLA')
selected_stock = st.selectbox('Select dataset for prediction', stocks)
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())
space(2)


#############################################
st.subheader("CORRELATION BETWEEN DIFFERENT STOCKS CLOSING PRICES")
tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)
closing_df = DataReader(tech_list, 'yahoo', start, end)['Adj Close']
st.write(closing_df)

#####################################################
start = '2010-01-01'
end = '2019-12-31'

st.title('Stock Trend Prediction')

user_input = st.text_input('Enter Stock Ticker', 'AAPL')
df = DataReader(user_input, 'yahoo', start, end)

#Describing Data

st.subheader('Data from 2010 - 2019')
st.write(df.describe())

#Visualizations

st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b') 
st.pyplot(fig)

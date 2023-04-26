# Import Applicable Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import os

# ------------------------------------------------------------------------
# Importing our Data Set
apple = pd.read_csv('apple.csv')
microsoft = pd.read_csv('MicroSoft.csv')
samsung = pd.read_csv('Samsung.csv')


# Add a new date column for each dataset
for df in [apple, microsoft, samsung]:
    df['newdate'] = pd.to_datetime(df['Date'])
    df['year'] = df['newdate'].dt.year

# Filter out observations from years 2020-2022
apple_date_time = apple[(apple['year'] >= 2020) & (apple['year'] <= 2022)]
microsoft_date_time = microsoft[(microsoft['year'] >= 2020) & (microsoft['year'] <= 2022)]
samsung_date_time = samsung[(samsung['year'] >= 2020) & (samsung['year'] <= 2022)]

# EDA Data frame now includes Month, Day, and Year column
EDA = apple_date_time.copy()
EDA['month'] = EDA['newdate'].dt.month
EDA['day'] = EDA['newdate'].dt.day

# Filter it for March 17th, 2022
EDA = EDA[(EDA['month'] == 3) & (EDA['day'] == 17) & (EDA['year'] == 2022)]
EDA = EDA.drop(columns=['Date', 'Volume', 'newdate', 'year', 'month', 'day']).melt(var_name='Indicators', value_name='Dollars')

# Create the Chart
fig = go.Figure(go.Bar(x=EDA['Indicators'], y=EDA['Dollars'], text=EDA['Dollars'], textposition='auto', marker_color=['#FFE2D1', '#E1F0C4', '#6BAB90', '#0D5C63', '#5E4C5A']))
fig.update_layout(title='March 17th, 2022: Apple Stock Price Statistics', xaxis_title='Stock Price Indicators', yaxis_title='Dollars')
fig.show()

# Helper function to resample and summarize the data
def resample_and_summarize(df, start_year, end_year):
    df_filtered = df[(df['year'] >= start_year) & (df['year'] <= end_year)].copy()
    df_filtered.set_index('newdate', inplace=True)
    df_resampled = df_filtered.resample('M').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'})
    return df_resampled

# Resample and summarize the data for each dataset
apple_monthly_2007_2009 = resample_and_summarize(apple, 2007, 2009)
microsoft_monthly_2007_2009 = resample_and_summarize(microsoft, 2007, 2009)
samsung_monthly_2007_2009 = resample_and_summarize(samsung, 2007, 2009)

apple_monthly_2020_2022 = resample_and_summarize(apple_date_time, 2020, 2022)
microsoft_monthly_2020_2022 = resample_and_summarize(microsoft_date_time, 2020, 2022)
samsung_monthly_2020_2022 = resample_and_summarize(samsung_date_time, 2020, 2022)

# Helper function to create the chart with specified colors
def create_chart(df, title, increasing_color,decreasing_color):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(
        go.Candlestick(x=df.index,
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'],
                       increasing_line_color=increasing_color,
                       decreasing_line_color=decreasing_color),
        row=1, col=1)

    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Dollars')

    return fig

apple_chart = create_chart(apple_monthly_2020_2022, 'Apple Monthly Candlestick Chart (2020-2022)', '#35C730', '#C73535')
microsoft_chart = create_chart(microsoft_monthly_2020_2022, 'Microsoft Monthly Candlestick Chart (2020-2022)', '#35C730', '#C73535')
samsung_chart = create_chart(samsung_monthly_2020_2022, 'Samsung Monthly Candlestick Chart (2020-2022)', '#35C730', '#C73535')

apple_chart.show()
microsoft_chart.show()
samsung_chart.show()


range_buttons = [
    dict(count=1, label="1 mo", step="month", stepmode="backward"),
    dict(count=3, label="3 mo", step="month", stepmode="backward"),
    dict(count=6, label="6 mo", step="month", stepmode="backward"),
    dict(count=1, label="1 yr", step="year", stepmode="backward"),
    dict(step="all")
]


def create_chart2(data, title, increasing_color, decreasing_color, line_color):
    chart2 = go.Figure()

    chart2.add_trace(go.Candlestick(x=data['month'],
                                    open=data['open'],
                                    high=data['high'],
                                    low=data['low'],
                                    close=data['close'],
                                    increasing=dict(line=dict(color=increasing_color), fillcolor=increasing_color),
                                    decreasing=dict(line=dict(color=decreasing_color), fillcolor=decreasing_color),
                                    name='Price'))

    chart2.add_trace(
        go.Scatter(x=data['month'], y=data['high'], mode='lines', name='High Price', line=dict(color=line_color)))

    chart2.update_layout(
        xaxis=dict(
            rangeselector=dict(buttons=range_buttons),
            rangeslider=dict(visible=True, type='date'),
            type='date',
            title='Month'
        ),
        yaxis=dict(title='High Price'),
        title=title
    )

    return chart2



# Create chart definitions with default colors
apple_line_chart_default2 = create_chart2(apple_monthly_2007_2009, "Apple Stock Price Movement 2007 - 2009 (Monthly)", "#99B668",
                                          "#E03616", "#9AC4F8")
microsoft_line_chart_default2 = create_chart2(microsoft_monthly_2007_2009,
                                              "Microsoft Stock Price Movement 2007 - 2009 (Monthly)", "#99B668",
                                              "#E03616", "#9AC4F8")
samsung_line_chart_default2 = create_chart2(samsung_monthly_2007_2009, "Samsung Stock Price Movement 2007 - 2009 (Monthly)",
                                            "#99B668", "#E03616", "#9AC4F8")

# Create chart definitions with colorblind-friendly colors
apple_line_chart_colorblind2 = create_chart2(apple_monthly_2007_2009, "Apple Stock Price Movement 2007 - 2009 (Monthly)",
                                             "#009E73", "#D55E00", "#56B4E9")
microsoft_line_chart_colorblind2 = create_chart2(microsoft_monthly_2007_2009,
                                                 "Microsoft Stock Price Movement 2007 - 2009 (Monthly)", "#009E73",
                                                 "#D55E00", "#56B4E9")
samsung_line_chart_colorblind2 = create_chart2(samsung_monthly_2007_2009, "Samsung Stock Price Movement 2007 - 2009 (Monthly)",
                                               "#009E73", "#D55E00", "#56B4E9")

# apple_line_chart_default2.show()
# microsoft_line_chart_default2.show()
# samsung_line_chart_default2.show()
#
#
# apple_line_chart_colorblind2.show()
# microsoft_line_chart_colorblind2.show()
# samsung_line_chart_colorblind2.show()










import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('formatted_data.csv')

# Convert date column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Create Dash application
app = dash.Dash(__name__)

# Calculate daily total sales
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create chart
fig = px.line(daily_sales, 
              x='date', 
              y='sales',
              title='Pink Morsel Sales Trend',
              labels={'date': 'Date', 'sales': 'Sales'},
              markers=True)

# Add vertical line for price increase date
price_increase_date = '2021-01-15'
fig.add_shape(
    type='line',
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref='paper',
    line=dict(color='red', dash='dash')
)

# Add annotation for price increase
fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref='paper',
    text="Price Increase",
    showarrow=False,
    yshift=10
)

# Calculate average sales before and after price increase
before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()

# Set chart style
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=12),
    annotations=[
        dict(
            text=f"Average Sales Before Price Increase: {before_increase:.2f}",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False
        ),
        dict(
            text=f"Average Sales After Price Increase: {after_increase:.2f}",
            xref="paper", yref="paper",
            x=0.02, y=0.95,
            showarrow=False
        )
    ]
)

# Application layout
app.layout = html.Div([
    html.H1('Soul Foods Sales Dashboard', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px'}),
    
    html.Div([
        dcc.Graph(figure=fig)
    ], style={'width': '90%', 'margin': 'auto'})
])

if __name__ == '__main__':
    app.run_server(debug=True)

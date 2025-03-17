import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('formatted_data.csv')

# Convert date column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Define styles
STYLES = {
    'container': {
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'margin': '20px auto',
        'maxWidth': '1200px'
    },
    'header': {
        'textAlign': 'center',
        'color': '#2c3e50',
        'margin': '20px',
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '32px',
        'textShadow': '2px 2px 4px rgba(0, 0, 0, 0.1)'
    },
    'radio-container': {
        'backgroundColor': 'white',
        'padding': '15px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
        'margin': '20px auto',
        'textAlign': 'center'
    },
    'radio-label': {
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '16px',
        'color': '#2c3e50',
        'margin': '10px'
    }
}

# Create Dash application
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1('Soul Foods Sales Dashboard', 
            style=STYLES['header']),
    
    html.Div([
        html.Label('Select Region:', style=STYLES['radio-label']),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px'}
        )
    ], style=STYLES['radio-container']),
    
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={'width': '90%', 'margin': 'auto'})
], style=STYLES['container'])

# Callback to update the chart based on region selection
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Calculate daily total sales
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    
    # Create chart
    fig = px.line(daily_sales, 
                  x='date', 
                  y='sales',
                  title=f'Pink Morsel Sales Trend - {selected_region.title()} Region',
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
        font=dict(size=12, family='Arial'),
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
        ],
        hovermode='x unified'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8053) 
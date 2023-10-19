import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Create the Dash app
app = dash.Dash(__name__)


# Define your background image and logo URLs
background_color = 'grey'
logo_url = 'colognelogo.jpg'
# Layout of the web app
app.layout = html.Div(style={'background-color': background_color, 'background-size': 'cover', 'height': '100vh'}, children=[
     html.Link(rel='stylesheet', href='/assets/styles.css'),
    html.Img(src="assets/cologne.png", alt='Logo', style={'width': '100px'}),
    html.H1("Aviation Cost Calculator"),
    
    # Sidebar inputs for Operating Costs (/hour)
    html.Div([
        html.H3("Operating Costs (/hour)"),
        dcc.Input(id='fuel-input', type='number', value=38.0),
        dcc.Input(id='oil-input', type='number', value=3.13),
        dcc.Checklist(id='engine-reserve', options=[{'label': 'Engine Reserve', 'value': 'engine-reserve'}]),
    ],className="container"),
    
    # Sidebar inputs for Ownership Costs (/Year)
    html.Div([
        html.H3("Ownership Costs (/Year)"),
        dcc.Input(id='insurance-input', type='number', value=1200.0),
        dcc.Input(id='hanger-input', type='number', value=600.0),
        dcc.Input(id='inspection-input', type='number', value=1500.0),
        dcc.Input(id='avionics-input', type='number', value=500.0),
        dcc.Input(id='loan-input', type='number', value=3090.0),
        dcc.Input(id='tax-input', type='number', value=255.0),
    ]),
    
    # Constants
    dcc.Store(id='rental-cost', data=135.0),
    dcc.Store(id='break-even-hours', data=77),
    dcc.Store(id='fly-hours', data=77),
    
    # Dropdown menu for calculations
    dcc.Dropdown(
        id='calculation-dropdown',
        options=[
            {'label': 'Total Variable Cost per Hour', 'value': 'variable-cost-hour'},
            {'label': 'Fixed Cost per Month', 'value': 'fixed-cost-month'},
            {'label': 'Total Fixed Cost per Year', 'value': 'fixed-cost-year'},
            {'label': 'Total Cost to Break Even', 'value': 'cost-to-break-even'},
            {'label': 'Cost to Fly Those Hours', 'value': 'cost-to-fly-hours'},
            {'label': 'Money Saved or Lost by Buying', 'value': 'money-saved-lost'},
        ],
        value='variable-cost-hour'
    ),
    
    # Display the result
    html.Div(id='output-results'),
])

# Define callback functions to update the result based on user inputs
@app.callback(
    Output('output-results', 'children'),
    Input('calculation-dropdown', 'value'),
    Input('fuel-input', 'value'),
    Input('oil-input', 'value'),
    Input('engine-reserve', 'value'),
    Input('insurance-input', 'value'),
    Input('hanger-input', 'value'),
    Input('inspection-input', 'value'),
    Input('avionics-input', 'value'),
    Input('loan-input', 'value'),
    Input('tax-input', 'value'),
    Input('rental-cost', 'data'),
    Input('break-even-hours', 'data'),
    Input('fly-hours', 'data')
)
def update_result(selected_calculation, fuel, oil, engine_reserve, insurance, hanger, inspection, avionics, loan, tax, rental, break_even, fly_hours):
    # Implement the calculations based on the selected calculation
    # Return the result to be displayed in the web app
    result = ""
    if selected_calculation == "variable-cost-hour":
        # Calculate total variable cost per hour
        result = f"Total Variable Cost per Hour: ${(100 / 50 + (7.50 * 0.15) if not engine_reserve else 100 / 50 + (7.50 * 0.15) + 4.75 * 8):.2f}"
    elif selected_calculation == "fixed-cost-month":
        # Calculate fixed cost per month
        result = f"Fixed Cost per Month: ${((insurance + hanger + inspection + avionics + loan + tax) / 12):.2f}"
    elif selected_calculation == "fixed-cost-year":
        # Calculate total fixed cost per year
        result = f"Total Fixed Cost per Year: ${insurance + hanger + inspection + avionics + loan + tax:.2f}"
    elif selected_calculation == "cost-to-break-even":
        # Calculate total cost to break even
        result = f"Total Cost to Break Even: ${(break_even * (100 / 50 + (7.50 * 0.15) if not engine_reserve else 100 / 50 + (7.50 * 0.15) + 4.75 * 8) + (insurance + hanger + inspection + avionics + loan + tax)):.2f}"
    elif selected_calculation == "cost-to-fly-hours":
        # Calculate cost to fly those hours
        result = f"Cost to Fly Those Hours: ${(fly_hours * (100 / 50 + (7.50 * 0.15) if not engine_reserve else 100 / 50 + (7.50 * 0.15) + 4.75 * 8) + (insurance + hanger + inspection + avionics + loan + tax)):.2f}"
    elif selected_calculation == "money-saved-lost":
        # Calculate money saved or lost by buying
        result = f"Money Saved or Lost by Buying: ${(fly_hours * rental - (fly_hours * (100 / 50 + (7.50 * 0.15) if not engine_reserve else 100 / 50 + (7.50 * 0.15) + 4.75 * 8) + (insurance + hanger + inspection + avionics + loan + tax))):.2f}"
    return result

if __name__ == '__main__':
    app.run_server(debug=True)

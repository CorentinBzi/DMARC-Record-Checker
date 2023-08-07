import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dns.resolver
import csv
from datetime import datetime
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load missing domains from the CSV file into a DataFrame
def load_domains():
    try:
        df = pd.read_csv('missing_dmarc.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Domaine", "Date"])
    return df

missing_domains_df = load_domains()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Vérificateur DMARC", className="text-center my-4")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Input(id='domain-input', type='text', placeholder='Entrez un domaine...', className='form-control'),
            html.Button('Vérifier', id='check-button', n_clicks=0, className='btn btn-primary mt-2'),
            html.Div(id='output-container', className='mt-2'),
        ], md=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Pas de DMARC", className="text-center my-4"),
            html.Div(id='auto-discover-output', children=dbc.Table.from_dataframe(missing_domains_df, striped=True, bordered=True, hover=True))
        ])
    ])
])

@app.callback(
    [Output('output-container', 'children'),
     Output('auto-discover-output', 'children')],
    [Input('check-button', 'n_clicks')],
    [dash.dependencies.State('domain-input', 'value')]
)
def check_dns(n_clicks, domain):
    global missing_domains_df  # Add this line to use the global variable

    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate

    # Vérifier si le domaine existe
    try:
        dns.resolver.resolve(domain, 'A')
    except:
        try:
            dns.resolver.resolve(domain, 'AAAA')
        except:
            return dbc.Alert(f"Le domaine {domain} n'existe pas.", color="warning"), dash.no_update

    # Check if the domain already exists in the DataFrame
    if domain not in missing_domains_df["Domaine"].values:
        # Vérifier l'enregistrement DMARC
        try:
            dmarc = dns.resolver.resolve('_dmarc.' + domain, 'TXT')
            return dbc.Alert(f"Enregistrement DMARC pour {domain}: {dmarc[0].to_text()}", color="success"), dash.no_update
        except:
            missing_domains_df = missing_domains_df.append(
                {"Domaine": domain, "Date": datetime.now().strftime('%Y-%m-%d')}, ignore_index=True
            )
            # Write the updated DataFrame to the CSV file
            missing_domains_df.to_csv('missing_dmarc.csv', index=False)

    if not missing_domains_df.empty:
        table = dbc.Table.from_dataframe(missing_domains_df, striped=True, bordered=True, hover=True)
    else:
        empty_df = pd.DataFrame(columns=["Domaine", "Date"])
        table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True)
    return dbc.Alert(f"L'enregistrement DMARC pour {domain} n'a pas pu être trouvé.", color="danger"), table


if __name__ == '__main__':
    app.run_server(debug=True)


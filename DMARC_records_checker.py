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

# Charger les domaines sans DMARC depuis le fichier
def load_domains():
    try:
        with open('missing_dmarc.csv', 'r') as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        return []

missing_domains = load_domains()

# Initialiser le tableau avec les données existantes ou un tableau vide si aucune donnée n'est présente
if missing_domains:
    initial_table_content = dbc.Table.from_dataframe(pd.DataFrame(missing_domains, columns=["Domaine", "Date"]), striped=True, bordered=True, hover=True)
else:
    empty_df = pd.DataFrame(columns=["Domaine", "Date"])
    initial_table_content = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True)



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
            html.Div(id='auto-discover-output', children=initial_table_content)
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

    # Vérifier l'enregistrement DMARC
    try:
        dmarc = dns.resolver.resolve('_dmarc.'+domain, 'TXT')
        return dbc.Alert(f"Enregistrement DMARC pour {domain}: {dmarc[0].to_text()}", color="success"), dash.no_update
    except:
        # Vérifier si le domaine existe déjà dans la liste
        existing_entry = next((entry for entry in missing_domains if entry[0] == domain), None)
        if existing_entry:
            missing_domains.remove(existing_entry)
        missing_domains.append([domain, datetime.now().strftime('%Y-%m-%d')])

        # Écrire la liste mise à jour dans le fichier CSV
        with open('missing_dmarc.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(missing_domains)
        
        if missing_domains:
            table = dbc.Table.from_dataframe(pd.DataFrame(missing_domains, columns=["Domaine", "Date"]), striped=True, bordered=True, hover=True)
        else:
            empty_df = pd.DataFrame(columns=["Domaine", "Date"])
            table = dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True)
        return dbc.Alert(f"L'enregistrement DMARC pour {domain} n'a pas pu être trouvé.", color="danger"), table



if __name__ == '__main__':
    app.run_server(debug=True)

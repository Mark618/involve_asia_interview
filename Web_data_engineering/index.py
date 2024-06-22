from app import app
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
from apps import graph, error
server = app.server

app.layout = html.Div(
    [
        html.Nav(
            html.Div(
                className="nav-wrapper",
                children=[
                    html.A("Involve Asia Data Science & Data Engineering Assessments", className="brand-logo", style={"padding-left": "15px"},
                           href="/apps/home"),
                    html.Ul(
                        className="right hide-on-med-and-down",
                        children=[
                            html.Li(""),                            
                        ]
                    )
                ],
                style={"backgroundColor": "Teal"}
            ),
        ),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=[
            
            ]),

    ]
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):    
    if pathname == '/apps/':
        return graph.layout    
    else:
        return error.layout

if __name__ == '__main__':
    app.run_server(debug=True)
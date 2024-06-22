from app import app

from dash.dependencies import Input, Output
from dash import Dash, html, dcc

layout = html.Div(
    [
        html.Br(),
        html.Img(src=app.get_asset_url('undraw_page_not_found_su7k.svg'),
                 className="responsive-img")
    ]
    , className="center"
)

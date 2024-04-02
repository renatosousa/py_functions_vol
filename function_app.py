import azure.functions as func
import logging
import yfinance as yf

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_price(symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        last_price = data['Close'].iloc[-1]
        return last_price

@app.route(route="py_get_last_price")
def py_get_last_price(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        get_price(name)
        return func.HttpResponse(f"A ultima cotação da ação, {name} foi de " + str(round(get_price(name), 2)), status_code=200)
    else:
        return func.HttpResponse(
             "Passe o atributo da ação escolhida no parâmetro 'name' da requisição, o nome do ativo deve constar no yahoo finance." + 
             "\nExemplo: ?name=petr4.sa",
             status_code=200
        )
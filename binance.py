import json
import websocket
import datetime
from PrintException import PrintException


class BinanceTrade:
    def __init__(self):
        self.socket = f'wss://stream.binance.com:9443/ws/!ticker@arr'
        self.prices = []

    def on_message(self, wsapp, message):
        json_message = json.loads(message)
        self.handle_trades(json_message)
        if self.keep_running:
            print(self.prices)
        else:
            wsapp.close()

    def on_error(self, wsapp, error):
        print(error)

    def handle_trades(self, json_message):
        try:
            for item in json_message:
                date_time = datetime.datetime.fromtimestamp(item['E'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                self.prices.append(
                    {
                        'SYMBOL': item['s'],
                        'PRICE': item['p'],
                        'QTY': item['q'],
                        'TIMESTAMP': str(date_time)
                    }
                )
        except:
            print(PrintException)

    def run(self, keep_running=True):
        self.keep_running = keep_running
        self.wsapp = websocket.WebSocketApp(self.socket, on_message=self.on_message, on_error=self.on_error)
        self.wsapp.run_forever()

        return self.prices


start = datetime.datetime.now()
binance = BinanceTrade().run(keep_running=False)
for crypto in binance:
    print(crypto)
print(len(binance))
print(datetime.datetime.now() - start)

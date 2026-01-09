import sys

from django.apps import AppConfig
import threading

class DataConfig(AppConfig):
    name = "data"

    def ready(self) -> None:
        if len(sys.argv) > 1 and sys.argv[1] == "runserver":
            from data.services.stock_watch_service import StockWatchService
            thread = threading.Thread(
                target=StockWatchService.refresh_symbols_from_binance
            )

            # This will allow the thread to exit with the main program
            thread.daemon = True
            thread.start()        
        
        super().ready()

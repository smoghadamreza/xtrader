from django.apps import AppConfig
import threading

class DataConfig(AppConfig):
    name = "data"

    def ready(self) -> None:
        from data.services.stock_watch_service import StockWatchService
        thread = threading.Thread(
            target=StockWatchService.refresh_symbols_from_binance
        )

        # This will allow the thread to exit with the main program
        thread.daemon = True
        thread.start()        
        return super().ready()

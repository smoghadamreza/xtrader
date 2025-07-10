import threading
from django.apps import AppConfig

class FinanceConfig(AppConfig):
    name = 'finance'

    def ready(self):
        """Run startup tasks after Django is fully initialized"""
        import sys
        if 'manage.py' in sys.argv[0] and 'runserver' not in sys.argv:
            return  # Skip for management commands except runserver

        if not threading.current_thread().daemon:
            self.run_startup_tasks()

    def run_startup_tasks(self):
        """Import and run tasks here to avoid circular imports"""
        from .oms import Binance  # Import here, not at module level
        Binance.set_symbols()
        self.start_scheduler()

    def start_scheduler(self):
        """Start periodic tasks"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from .oms import Binance  # Import here
            
            scheduler = BackgroundScheduler()
            scheduler.add_job(Binance.set_symbols, 'interval', minutes=10)
            scheduler.start()
        except ImportError:
            # Handle case where APScheduler isn't installed
            pass
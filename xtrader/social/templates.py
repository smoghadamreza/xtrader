from utils.templates import TemplateFiles

class SocialTemplates(TemplateFiles):
    """
    Manages template paths for the 'accounts' app.
    """
    BASE = "social/"
    COPY_TRADING = BASE + "copy_trading"
    LEAGUE_LANDING = BASE + "league_landing"
    TRADE_PROFILE = BASE + "trader_profile"

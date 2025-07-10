# XTrader: Secure Crypto Trading for Iranian Users

XTrader is a comprehensive trading platform designed to empower Iranian cryptocurrency traders
by providing secure, unrestricted access to binance.com despite regional restrictions and sanctions. 
Our platform combines advanced trading tools with a unique proxy infrastructure that masks users' geographical
locations, allowing them to trade on Binance without fear of account bans or sanctions-related disruptions.

## Key Features

### Secure Binance Access
- Bypasses geo-restrictions using proprietary proxy technology
- Protects user identities and prevents account bans
- Maintains full trading functionality while complying with local regulations

### Trading Ecosystem
- **Finance App**: Automated trading via exchange APIs and TradingView alerts
- **Social App**: Follow and copy verified ProTraders with transparent performance history
- **Data App**: Comprehensive market analytics and financial metrics tracking

### Asset Management
- **AUM App**: Track investments and portfolio performance
- **Accounts App**: Secure wallet management and deposit tracking
- **Sales App**: Subscription-based access to premium features

## Technical Architecture
Built on Django, XTrader integrates multiple specialized apps:
1. **Social**: Community-driven trading with follower relationships
2. **Finance**: Automated strategy execution and exchange connectivity
3. **Data**: Financial market analysis and instrument tracking
4. **AUM**: Investment portfolio management
5. **Accounts**: User profile and financial record management
6. **Sales**: Subscription and payment processing

XTrader provides Iranian traders with a complete, secure solution for global 
cryptocurrency markets, combining technical innovation with community features for all experience levels.

## Entity Relation Diagram 

The ERD of the project is visible in the following image. The image is automatically generated via the `conda run -n xtrader-env python manage.py graph_models -a -g -o ../Writerside/images/ERD.png`
command which is located in `docker-compose.yml`.

For a better look at the ERD, open the image in new tab. The image is in high resolution and can be zoomed on.

![XTrader-ERD](ERD.png)
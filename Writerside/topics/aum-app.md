# AUM

The AUM (Assets Under Management) Django app is designed to manage and track mutual funds or 
investment portfolios within the platform. It provides a comprehensive system for recording fund-related data,
including fund definitions, investor details, unit transfers, and historical snapshots for analytical and
operational purposes.

At its core, the [](fund-model.md) model captures essential data about each investment portfolio, including asset composition, 
fee structures, and performance indicators. The [](fund-investor-model.md) model tracks individual investors
and the number of
units they hold in each fund. To support transparency and operational tracking, the [](unit-transfer-model.md) 
model records all
unit transfer activities between funds. Additionally, the [](fund-unit-snapshot.md) model captures time-based 
snapshots of 
fund attributes, allowing for historical analysis and performance monitoring. Together, these models facilitate
robust fund management and investor engagement within the AUM app.

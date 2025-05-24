# Accounts

The **Accounts** Django app is responsible for managing user-related data, 
particularly focusing on profile information, financial records, and deposit transactions.
It encapsulates three core models—[](accounts-profile-model.md), [](accounts-wallet-model.md), and [](accounts-deposit-model.md)—
each serving a distinct function in 
supporting user identity and financial activity within the %product% platform.

The [](accounts-profile-model.md) model handles auxiliary user information such as phone numbers and social media 
identifiers (e.g., Telegram ID), enriching the base user data. The [](accounts-wallet-model.md) model tracks users' 
financial metrics, including balances and income, allowing for real-time management of funds on the platform. 
Meanwhile, the [](accounts-deposit-model.md) model records and synchronizes USDT deposit transactions with a remote site,
ensuring accurate and up-to-date financial data. Together, these models enable a comprehensive system for
user account and financial management.

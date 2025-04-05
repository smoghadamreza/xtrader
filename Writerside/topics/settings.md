# Django Settings

This document provides a concise overview of the key components defined in the `settings.py` file for
the %product% Django project. It covers the essential configurations including environment variables, 
installed applications, database settings, middleware, email, templates, static files, 
and additional custom settings.

---

## 1. Environment Variables

The project uses several environment variables to securely manage sensitive information and configure key settings. Below is a summary:

| **Variable**        | **Description**                                                   | **Further Information**                                                                    |
|---------------------|-------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **SECRET_KEY**      | Django’s secret cryptographic key (must be kept confidential).    | [Django SECRET_KEY](https://docs.djangoproject.com/en/1.10/ref/settings/#secret-key)       |
| **DEBUG**           | Flag to enable/disable debug mode (1 for True, 0 for False).      | [Django DEBUG](https://docs.djangoproject.com/en/1.10/ref/settings/#debug)                 |
| **ALLOWED_HOSTS**   | Comma-separated list of domains allowed to serve the application. | [Django ALLOWED_HOSTS](https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts) |
| **DB_HOST**         | Host address for the PostgreSQL database.                         | <include from="repeatable-texts.topic" element-id="django-db">                             |
| **DB_NAME**         | Name of the PostgreSQL database.                                  | <include from="repeatable-texts.topic" element-id="django-db">                             |
| **DB_USER**         | Username for connecting to the PostgreSQL database.               | <include from="repeatable-texts.topic" element-id="django-db">                             |
| **DB_PASS**         | Password for the PostgreSQL database user.                        | <include from="repeatable-texts.topic" element-id="django-db">                             |
| **XTREASURY_BOT**   | Custom variable for bot integration (usage-specific).             | N/A (custom project variable)                                                              |
| **USDT_WALLET**     | Custom variable for specifying a USDT wallet address.             | N/A (custom project variable)                                                              |
| **REFERRAL_BOUNCE** | Referral commission rate as a float (e.g., 0.3).                  | N/A (custom project logic)                                                                 |
| **ADMIN_TEL_ID**    | Telegram ID for admin notifications.                              | N/A (custom project variable)                                                              |
| **COPYTRADEFEE**    | Fee rate for copy-trading services as a float.                    | N/A (custom project variable)                                                              |
| **LOG_LEVEL**       | Logging level setting (e.g., INFO, DEBUG, ERROR).                 | [Django Logging](https://docs.djangoproject.com/en/1.10/topics/logging/#loggers)           |

---

## 2. Installed Applications

The settings include a mix of Django's built-in apps, project-specific apps, and third-party packages:

- **Django Built-in Apps:**  
  - Examples: `django.contrib.admin`, `django.contrib.auth`, `django.contrib.sessions`, etc.
  - Provide core functionalities such as administration, authentication, session management, and static file handling.

- **Project-Specific Apps:**  
  - Examples: `accounts`, `main`, `finance`, `data`, `sales`, `social`, `aum`
  - Contain the custom business logic and functionalities of the "xtrader" project.

- **Third-Party Apps:**  
  - **Userena:** Enhances user management features.  
  - **Guardian:** Adds object-level permission capabilities.  
  - **Easy Thumbnails:** Assists with generating and managing image thumbnails.  
  - **Channels:** Supports asynchronous communication and WebSocket integration.  
  - **Bootstrap3:** Integrates Bootstrap for front-end styling.  
  - **django.contrib.sites:** Enables Django’s sites framework for multi-site support.

---

## 3. Database Configuration

- **Database Engine:** PostgreSQL  
- **Configuration:** Uses environment variables (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`) with the default port set to 5432.
- **Reference:** [Django DATABASES](https://docs.djangoproject.com/en/1.10/ref/settings/#databases)

---

## 4. Middleware

Below is a table listing the middleware components used in the project, their purposes, and links to their documentation.

| **Middleware Component**                                  | **Purpose**                                                                                                                | **Documentation**                                                                                              |
|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| `django.middleware.security.SecurityMiddleware`           | Enhances security by enforcing SSL redirects, setting security headers (e.g., HSTS), and managing other security settings. | [SecurityMiddleware](https://docs.djangoproject.com/en/1.10/ref/middleware/#module-django.middleware.security) |
| `django.contrib.sessions.middleware.SessionMiddleware`    | Manages user sessions, allowing storage and retrieval of per-user data across requests.                                    | [Sessions](https://docs.djangoproject.com/en/1.10/topics/http/sessions/)                                       |
| `django.middleware.csrf.CsrfViewMiddleware`               | Protects against Cross-Site Request Forgery (CSRF) attacks by ensuring that POST requests come from trusted sources.       | [CSRF Protection](https://docs.djangoproject.com/en/1.10/ref/csrf/)                                            |
| `django.contrib.auth.middleware.AuthenticationMiddleware` | Associates users with requests via sessions, enabling authentication mechanisms throughout the application.                | [Authentication](https://docs.djangoproject.com/en/1.10/topics/auth/)                                          |
| `django.contrib.messages.middleware.MessageMiddleware`    | Enables temporary messaging (e.g., notifications) between views and templates.                                             | [Messages](https://docs.djangoproject.com/en/1.10/ref/contrib/messages/)                                       |
| `django.middleware.clickjacking.XFrameOptionsMiddleware`  | Prevents clickjacking attacks by setting the X-Frame-Options HTTP header to control whether the site can be framed.        | [Clickjacking Protection](https://docs.djangoproject.com/en/1.10/ref/clickjacking/)                            |


## 5. Email Configuration

The project is set up to send emails using Django's SMTP backend. Key configurations include:
- SMTP server settings (host, port, and credentials)
- TLS usage for secure email transmission

For more details, refer to [Django Email Docs](https://docs.djangoproject.com/en/1.10/topics/email/).

---

## 6. Templates and Static Files

- **Templates:**  
  - Configured with a designated directory and several context processors to support debugging, request data, user authentication, messaging, and internationalization.
  
- **Static Files:**  
  - **Static URL/Root:** Manages CSS, JavaScript, and image files.
  - **Media URL/Root:** Configured for handling uploaded media content.

For further guidance, see [Django Static Files](https://docs.djangoproject.com/en/1.10/howto/static-files/).

---

## 7. Additional Configurations

- **Localization & Time Zone:**  
  - Time zone is set to "Iran" (consider using official timezone identifiers like "Asia/Tehran").  
  - Internationalization (i18n) and localization (l10n) are enabled with a defined locale path.
  
- **Authentication Backends:**  
  - Combines custom backends from Userena and Guardian with Django’s default backend for flexible authentication strategies.
  
- **Logging:**  
  - Configured to output logs to the console, with the log level determined by the `LOG_LEVEL` environment variable.
  
- **Local Overrides:**  
  - The file optionally imports local settings from `localsetting.py` to allow environment-specific overrides without modifying the main settings file.

---

This overview encapsulates the essential configuration aspects of the `settings.py` file 
for the %product% project, providing quick references to key environment variables and settings.
For additional details on each section, please consult the 
[Django documentation](https://docs.djangoproject.com/).

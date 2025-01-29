# TradingView

This model represents a trading strategy defined by a user.

## What does it inherit?

This class inherits `django.db.models.Model`. Django offers this class as a tool for defining a SQL database in python.
The documentation is available at <include from="third-party-libraries-links.topic" element-id="django.db.models"></include>.

*Notes*
- No field has `unique=True` attribute.

## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>is_nullable</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>trader</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user">)</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user who owns the <code>TradingView</code> configuration.</td>
    </tr>
    <tr>
        <td>webhook</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:heavy_check_mark:</td>
        <td>N/A</td>
        <td>The webhook URL for <code>TradingView</code>.</td>
    </tr>
    <tr>
        <td>trading</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.boolean-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>Indicates whether trading is enabled. Defaults to <code>False</code>.</td>
    </tr>
    <tr>
        <td>notification</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.boolean-field"/></td>
        <td>:x:</td>
        <td>N/A</td>
        <td>Indicates whether notifications are enabled. Defaults to <code>False</code>.</td>
    </tr>
</table>

## Methods

### create_hook  
  - **usage**: Generates a unique webhook code using `Profile.code_generator`. #TODO If the generated code already exists in the database, it recursively calls itself to generate a new one.  
  - **signature**: `create_hook() -> str`  
  - **output**: Returns a unique webhook code as a string.  
> **Note**: This method ensures that the generated webhook code is unique by checking its existence in the `TradingView` model's `webhook` field. If a duplicate is found, it regenerates the code.

### activate  
  - **usage**: Activates trading and/or notifications for the `TradingView` configuration. Ensures that the necessary conditions (e.g., exchange configuration or Telegram connection) are met before activation.  
  - **signature**: `activate(self, trading: bool, notification: bool) -> str`  
  - **parameters**:  
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />  
    + **trading**: A boolean indicating whether to activate trading. Defaults to `False`.  
    + **notification**: A boolean indicating whether to activate notifications. Defaults to `False`.  
  - **output**: Returns an error message as a string if activation fails. Otherwise, returns an empty string.  
> **Note**:  
> - For trading activation, the user must have a connected exchange with both `public` and `private` keys.  
> - For notification activation, the user must have a connected Telegram account (i.e., `telegram_id` must be set in their profile).  
> - If no errors occur, the changes are saved to the database.
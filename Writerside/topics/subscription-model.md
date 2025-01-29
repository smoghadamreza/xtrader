# Subscription

The `Subscription` class represents a purchased [](package-model.md). In other words
it connects a [](package-model.md) to [](payment-model.md).

## What does it inherit?

<include from="repeatable-texts.topic" element-id="django-models.desc"/>

*Notes*
- No field has `unique=True` attribute.
- All fields are nullable.

## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>package</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<a href="package-model.md"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The package associated with this subscription. Can be null or blank.</td>
    </tr>
    <tr>
        <td>user</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user associated with this subscription. Can be null or blank.</td>
    </tr>
    <tr>
        <td>expiry</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-time-field"/></td>
        <td>N/A</td>
        <td>The expiration date and time of the subscription. Defaults to the current time.</td>
    </tr>
</table>

## Methods

### have_subscribe
  - **usage**: To check if a specified `User` has a non-expired `Subscription` with specified `Package.category`.
  - **signature**: `have_subscribe(cls, user: django.contrib.auth.User, packages)`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
    + **user**: The user which we want to see if he/she has a non-expired `Subscription`.
    + **packages**: A list of strings or a string which represents the category of packages we wish to know 
       whether the use has a subscription of. 
  - **output**: One of the matched `Subscription` entries or `None` if no match was found.

### subscribe
  - **usage**: Creates a `Subscription` for given `User` with given [](package-model.md). Subtracts cost of the [](package-model.md) 
    from the user's [](accounts-wallet-model.md). 
  - **signature**: `subscribe(cls, user: django.contrib.auth.User, pack: Package) -> dict`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
    + **user**: The user which we want to create a `Subscription`.
    + **pack**: An object of [](package-model.md).
  - **output**: A `dict` which represents proper status code and message for user's request. 

### *Trivia Methods*

#### \_\_str\_\_
Returns `self.package.name` + `self.user.username`

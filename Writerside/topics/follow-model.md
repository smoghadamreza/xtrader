# Follow

The `Follow` class represents a one-way relationship from a `User` to a [](pro-trader-model.md). For a better intuition you
can think of it as the same relation in popular social medias like `Instagram`. A `User` can view and inspect 
activities of the `ProTrader`. #TODO

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
        <td>proTrader</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<a href="pro-trader-model.md"/> )</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The professional trader being followed.</td>
    </tr>
    <tr>
        <td>follower</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/> (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>The user who is following the professional trader.</td>
    </tr>
    <tr>
        <td>expiry</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-time-field"/></td>
        <td>N/A</td>
        <td>The expiration date and time of the follow relationship. Defaults to the current time.</td>
    </tr>
</table>

## Methods

### subscribe
  - **usage**: A `User` can subscribe to the [](pro-trader-model.md) that he/she is following. By doing so The subscription fee plus
    %product% service fee will be deducted from the `User`'s [](accounts-wallet-model.md) and added to the corresponding [](accounts-wallet-model.md)s.
  - **signature**: `subscribe(self, preiod: int) -> bool`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **period**: The duration which the subscription is going to last. It will be added to `expiry` field of the `Follow` object.
  - **output**: The status of the `subscribe` function. If `True` the function have succeeded completely, and if `False`
     some issue have occurred along the way like insufficient fund in the `User`'s [](accounts-wallet-model.md). 

### copytrade  #TODO: very unreadable function.
  - **usage**: A `User` can subscribe to the [](pro-trader-model.md) that he/she is following. By doing so The subscription fee plus
    %product% service fee will be deducted from the `User`'s [](accounts-wallet-model.md) and added to the corresponding [](accounts-wallet-model.md)s.
  - **signature**: `copytrade(user, brand, action)`
  - **parameters**: 
    + **user**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **brand**: The duration which the subscription is going to last. It will be added to `expiry` field of the `Follow` object.
    + **action**: The duration which the subscription is going to last. It will be added to `expiry` field of the `Follow` object.
  - **output**: The status of the `subscribe` function. If `True` the function have succeeded completely, and if `False`
     some issue have occurred along the way like insufficient fund in the `User`'s [](accounts-wallet-model.md). 

### *Trivial Method*

#### unfollow
Deletes this `Follow` object.
# Profile

This doc is a thorough explanation of the model `Profile` which is located in `accounts/models.py`.
This django model is for storing a user's profile information; e.g. phone number, social network ID (telegram), etc.

## What does it inherit?

This class inherits `UsernaBaseProfile`. This class is from
[Django Userna (Community Edition)](https://github.com/django-userena-ce/django-userena-ce) library
which according to their GitHub webpage do the following:

> Userena is a Django application that supplies your Django project
> with full account management. It's a fully customizable application
> that takes care of the signup, activation, messaging and more.

## Fields

<table>
    <tr>
        <td>field_name</td>
        <td>field_type</td>
        <td>is_unique</td>
        <td>is_nullable</td>
        <td>on_delete (for <include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>)</td>
        <td>description</td>
    </tr>
    <tr>
        <td>user</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.one-to-one"/>
            (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td>:heavy_check_mark:</td>
        <td>:x:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>Each user can have <b>only one</b> profile and each profile must be mapped to 
            <b>exactly one</b> user, thus this field has a one-to-one relation with <code>User.</code>
        </td>
    </tr>
    <tr>
        <td>cellPhone</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td> Each profile might have a cell phone number. Multiple profiles may have the same cell phone number.</td>
    </tr>
    <tr>
        <td>expire</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.date-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Profiles might have an expiry date. We check that in #TODO.</td>
    </tr>
    <tr>
        <td>telegram_id</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>A user may (#TODO) activate its panel via Telegram social media. Thus, we need this to send the activation code.</td>
    </tr>
    <tr>
        <td>telegram_activation_code</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>We compare this with what user has submitted in #TODO.</td>
    </tr>
    <tr>
        <td>telegram_activation_timestamp</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.integer-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Stores the time when <code>telegram_activation_code</code> is updated.</td>
    </tr>
    <tr>
        <td>referral_code</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.char-field"/></td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td>NA</td>
        <td>Users may suggest %product% to each other. We track these suggestions via <b>suggester</b> <code>referral_code</code>.</td>
    </tr>
    <tr>
        <td>referred_by</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.foreign-key"/>
            (<include from="third-party-libraries-links.topic" element-id="django-models.user"/>)</td>
        <td>:x:</td>
        <td>:heavy_check_mark:</td>
        <td><include from="third-party-libraries-links.topic" element-id="django-models.cascade"/></td>
        <td>If a <code>Profile</code> is created because of a referral, we store the referrer <code>User</code> in this field.</td>
    </tr>
</table>



## Methods

### save
  - **usage**: According to parent's class <include from="third-party-libraries-links.topic" element-id="python-docstring"/> we have:
    > Save the current instance. Override this in a subclass if you want to
        control the saving process.
    
    In this override we set all the characters of `user.username` and `user.email` to lower-case and we set
    `referral_code` equal to `user.username`.
  - **signature**: `save(self, *args, **kwargs)`
  - **parameters**: 
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
    + **\*args**: Allows a function to accept any number of positional arguments as a tuple.
    + **\*\*kwargs**: Allows it to accept any number of keyword arguments as a dictionary.
  - **output**: `None`

### make_referral_codes
  - **usage**: It iterates over all `Profile` objects that are stored in database and sets their `referral_code` 
    field equal to their `user.username`.
  - **signature**: `make_referral_codes(cls)`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
  - **output**: `None`

### make_lowercase
  - **usage**: It iterates over all `Profile` objects that are stored in database and makes characters of 
    `user.username` and `user.email` into lowercase.
  - **signature**: `make_lowercase(cls)`
  - **parameters**:
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
  - **output**: `None`

### code_generator
  - **usage**: By getting a `size` in the input, it returns a randomly sampled code with that size. Pool of sample characters 
    are all the ascii characters and digits.
  - **signature**: `code_generator(size: int) -> str`
  - **parameters**:
    + **size**: Integer that determines length of wanted code.
  - **output**: A `str` that contains the result code.

### get_code
  - **usage**: As it is an instance method, it either returns `telegram_activation_code` field, if it is not expired yet. 
    Otherwise it creates a random code by calling `code_generator` and store it in the `telegram_activation_code` and 
    setting a 5 minutes expiration countdown and storing it in `telegram_activation_timestamp`.
  - **signature**: `get_code(self) -> str`
  - **parameters**
    + **self**: <include from="repeatable-texts.topic" element-id="python-self" />
  - **output**: A `str` that contains the result code.

### mail_users
  - **usage**: By using #TODO template, it mails all active users in a subset of users and informs them about #TODO. If any of the 
    emails fail, it logs the failed attempts.
  - **signature**: `mail_users(cls, subject:str, emails=List<str>) -> List<str>`
  - **parameters**: 
    + **cls**: <include from="repeatable-texts.topic" element-id="python-cls" />
    + **subject**: Subject of the email.
    + **emails**: List of email addresses that we wish to send the emails to. If it is `None` the `emails` is considered
      all the users' email addresses.
  - **output**: List of email addresses which sending the email to them has failed.

### *Trivial Methods*

#### first_name
Returns `user.first_name`

#### last_name
 Returns `user.last_name`

#### last_login
Returns `user.last_login`
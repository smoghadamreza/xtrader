# Forms

<include from="repeatable-texts.topic" element-id="django-forms"/>

## Classes

### `SignupFormExtra`

A form that extends `SignupForm` to include additional fields such as `first_name`, `last_name`, `cellPhone`, and custom validation for `username`, `email`, and passwords.

#### Fields {id=fields}

- **`first_name`**: The user's first name (in Persian).
- **`last_name`**: The user's last name (in Persian).
- **`email`**: The user's email address.
- **`cellPhone`**: The user's mobile phone number (optional).
- **`password1`**: The user's password.
- **`password2`**: Confirmation of the user's password.
- **`username`**: The user's username (in English).

---

#### **`__init__`**

Initializes the form and ensures `first_name` and `last_name` fields appear at the top of the form.

- **Behavior**:
  - Calls the parent class's `__init__` method.
  - Adjusts the field order to prioritize `first_name` and `last_name`.

---

#### **`save`** {id="save_1"}

Overrides the `save` method to save additional fields (`first_name`, `last_name`, and `cellPhone`) to the user and their profile.

- **Behavior**:
  - Creates a new user using `UserenaSignup.objects.create_user`.
  - Updates the `first_name` and `last_name` fields of the new user.
  - Updates the `cellPhone` field in the user's profile.
  - Sends an activation email to the user.
  - Returns the newly created user object.

---

#### **`clean_username`**

Validates the username to ensure it is alphanumeric, not already in use, and not listed in `USERENA_FORBIDDEN_USERNAMES`.

- **Behavior**:
  - Checks if the username already exists in the database (case-insensitive).
  - Raises a validation error if the username is already taken or forbidden.
  - Returns the validated username.

---

#### **`clean_email`**

Validates the email to ensure it is unique and not already in use.

- **Behavior**:
  - Checks if the email already exists in the database (case-insensitive).
  - Raises a validation error if the email is already taken or associated with an unactivated account.
  - Returns the validated email.

---

#### **`clean`**

Validates the password fields to ensure they match, meet the minimum length requirement, and are not too common.

- **Behavior**:
  - Checks if `password1` and `password2` match.
  - Validates that the password is at least `MIN_LENGTH` (8 characters) long.
  - Uses Django's `CommonPasswordValidator` to ensure the password is not too common.
  - Raises validation errors for mismatched passwords, short passwords, or common passwords.
  - Returns the cleaned data.

---

### `PasswordResetForm`

A form for handling password reset requests. It collects the user's email (labeled as "username") and provides functionality to generate and send a password reset link.

---
#### Fields {id=fields_1}

- **`username`**: The username of the user which is trying to reset its password.

#### **`send_mail`**

Sends a `django.core.mail.EmailMultiAlternatives` email to the specified `to_email`.

- **Parameters**:
  - `subject_template_name`: The template for the email subject.
  - `email_template_name`: The template for the email body.
  - `context`: Context data to render the templates.
  - `from_email`: The sender's email address.
  - `to_email`: The recipient's email address.
  - `html_email_template_name`: Optional template for the HTML version of the email.

- **Behavior**:
  - Renders the subject and body from the provided templates.
  - Creates an `EmailMultiAlternatives` object and attaches the HTML email if provided.
  - Sends the email.

---

#### **`get_users`**

Retrieves active users with a usable password who match the provided email.

- **Parameters**:
  - `email1`: The email address to search for.

- **Returns**:
  - A generator of user objects that match the email and are eligible for password reset.

---

#### **`save`** {id=save_2}

Generates a one-time password reset link and sends it to the user.

- **Parameters**:
  - `domain_override`: Optional domain to use in the reset link (defaults to the current site).
  - `subject_template_name`: Template for the email subject.
  - `email_template_name`: Template for the email body.
  - `use_https`: Whether to use HTTPS in the reset link.
  - `token_generator`: Token generator for creating the reset token.
  - `from_email`: The sender's email address.
  - `request`: The current HTTP request.
  - `html_email_template_name`: Optional template for the HTML version of the email.
  - `extra_email_context`: Additional context data for the email templates.

- **Behavior**:
  - Retrieves users matching the provided email using `get_users`.
  - Generates a password reset link with a token for each user.
  - Sends the reset link via email using `send_mail`.

### `AuthenticationForm`

A custom form where the identification can be either an email address or a username. It also includes a "remember me" option for extended login sessions.

---

#### Fields {id=fields_2}

- **`identification`**: The user's username or email address.
- **`password`**: The user's password.
- **`remember_me`**: A checkbox to enable extended login sessions (e.g., "remember me for one month").

---

#### **`__init__`** {id=init_2}

Initializes the form and adjusts the `identification` field label based on whether usernames are enabled or disabled in the settings.

- **Behavior**:
  - Calls the parent class's `__init__` method.
  - Translates and updates the `remember_me` label dynamically.
  - If `USERENA_WITHOUT_USERNAMES` is enabled, changes the `identification` field label to prompt for an email.

---

#### **`clean`** {id=clean_2}

Validates the identification and password combination.

- **Behavior**:
  - Checks if the `identification` and `password` fields are provided.
  - Authenticates the user using the provided identification (username or email) and password.
  - Raises a validation error if:
    - The identification and password do not match.
    - The user account is not active.
  - Returns the cleaned data if validation passes.

### `EditProfileForm`

A form used for editing user profile information, including `first_name` and `last_name`. It ensures these fields are always displayed at the top of the form.

---

#### Fields {id=fields_3}

- **`first_name`**: The user's first name (optional).
- **`last_name`**: The user's last name (optional).

---

#### **`__init__`** {id=init_3}

Initializes the form and ensures `first_name` and `last_name` fields appear at the top.

- **Behavior**:
  - Calls the parent class's `__init__` method.
  - Reorders the fields to prioritize `first_name` and `last_name`.
  - Handles differences between Django versions (< 1.7 and > 1.7) for field ordering.

---

#### **`save`** {id=save_3}

Saves the updated profile information, including the user's `first_name` and `last_name`.

- **Behavior**:
  - Saves the profile using the parent class's `save` method.
  - Updates the associated user's `first_name` and `last_name` fields.
  - Returns the updated profile.

---

#### Meta

<include from="repeatable-texts.topic" element-id="django-model-forms-meta"/>

- **Model**: The profile model returned by `get_profile_model()`.
- **Excluded Fields**: `user`, `privacy`, `mugshot`. These fields are excluded from the form and will not be editable.

### `ChangeEmailForm`

A form for changing a user's email address. It validates that the new email is not already registered with another user and initiates the email change process.

---

#### Fields {id=fields_4}

- **`email`**: The new email address for the user.

---

#### **`__init__`** {id=init_4}

Initializes the form with the current user to ensure the new email address is unique and not the user's current email.

- **Parameters**:
  - `user`: The current user instance.
- **Behavior**:
  - Calls the parent class's `__init__` method.
  - Validates that the provided `user` is an instance of the user model.
  - Stores the `user` instance for later use.

---

#### **`clean_email`** {id=clean_4}

Validates that the new email address is not already registered with another user.

- **Behavior**:
  - Raises a validation error if the new email is the same as the user's current email.
  - Raises a validation error if the new email is already registered with another user.
  - Returns the validated email.

---

#### **`save`** {id=save_4}

Initiates the email change process by calling the `change_email` method on the user's `userena_signup` object.

- **Behavior**:
  - Calls `self.user.userena_signup.change_email()` with the new email address.
  - Sends a verification email to the new address to confirm the change.
  - Returns the result of the `change_email` method.

---

### `SetPasswordForm`

A form that allows a user to set a new password without entering their old password. It includes validation to ensure the new password meets security requirements and matches the confirmation field.

---

#### Fields {id=fields_5}

- **`new_password1`**: The new password for the user.
  - **Help Text**: Provides guidelines for creating a strong password:
    - Must be at least 8 characters long and include a letter.
    - Should not be simple or commonly used.
    - Should not be similar to other account information.
- **`new_password2`**: Confirmation of the new password.

---

#### **`__init__`** {id=init_5}

Initializes the form with the current user.

- **Parameters**:
  - `user`: The current user instance.
- **Behavior**:
  - Calls the parent class's `__init__` method.
  - Stores the `user` instance for later use.

---

#### **`clean_new_password2`** {id=clean_5}

Validates that the new password and its confirmation match and meet security requirements.

- **Behavior**:
  - Raises a validation error if the passwords do not match.
  - Uses Django's `password_validation.validate_password` to ensure the password meets security standards.
  - Returns the validated password.

---

#### **`save`** {id=save_5}

Saves the new password for the user.

- **Behavior**:
  - Sets the new password using `self.user.set_password()`.
  - Saves the user instance if `commit=True`.
  - Returns the updated user instance.

---
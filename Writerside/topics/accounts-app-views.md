# Views

<include from="repeatable-texts.topic" element-id="django-views">
</include>

## View Classes

### `ExtraContextTemplateView`

This class-based view extends `TemplateView` to include additional context variables. Here we quote its docstring:  

> Add extra context to a simple template view  

#### Behavior {id=class_behavior_1}  

- Merges the `extra_context` dictionary into the template context via `get_context_data`.  
- Handles `POST` requests by delegating to the `get` method of `TemplateView`, resulting in template re-rendering (commonly used when form submissions are invalid).  

#### Context variables {id=class_context_1}  

- All key-value pairs provided in the `extra_context` attribute are added to the template context.

### `ProfileListView`

This class-based view handles rendering the list of profiles. Here we quote its docstring:  

> Lists all profiles  

#### Behavior {id=class_behavior_2}  

- If profile listing is disabled (via `USERENA_DISABLE_PROFILE_LIST`) and the requesting user is not staff, the view raises an `Http404` exception.  
- Extracts the `page` number from the query parameters (defaults to `1`).  
- Uses the template specified by `USERENA_PROFILE_LIST_TEMPLATE`.  
- **On rendering**:  
  - Retrieves visible profiles for the current user via `get_visible_profiles`.  
  - Adds `page`, `paginate_by` (currently disabled), and `extra_context` to the template context.  
  - Populates `profile_list` in the context with the retrieved profiles.  

#### Context variables {id=class_context_2}  

- `profile_list`: List of profile objects returned by the queryset.  
- `page`: Current page number (from query parameters).  
- `paginate_by`: Placeholder for pagination configuration (not active).  
- `extra_context`: Additional context variables provided via the `extra_context` class attribute.  

## Functions

### `signup`

This function handles rendering the sign-up form template on `GET` requests and apply the form on the 
`POST` requests. Here we quote its docstring: 

>   Signup requiring a username, email and password. After signup a user gets
    an email with an activation link used to activate their account. After
    successful signup redirects to ``success_url``.

#### Used Decorators {id=used_decorator_1}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input parameters {id=input_param_1}
We quote the docstring notes on the input parameters as they seem sufficient. 

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `signup_form`: Form that will be used to sign a user. Defaults to userena's
 [SignUpFormExtra](http://localhost:63342/xtrader/preview/accounts-app-forms.html#signupformextra).
- `template_name`: String containing the template name that will be used to display the signup form. 
  Defaults to``userena/signup_form.html``.
- `success_url`: String containing the URI which should be redirected to after a successful signup. 
 If not supplied will redirect to``userena_signup_complete`` view.
- `extra_context`: `dict` containing variables which are added to the template context. 
 Defaults to a dictionary with a ``form`` key containing the 
[``signup_form``](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/accounts/templates/userena/signup_form.html).

#### Behavior {id=behavior_1}

- If signup is disabled (via `USERENA_DISABLE_SIGNUP`), the function raises a `PermissionDenied` exception.
- If `USERENA_WITHOUT_USERNAMES` is enabled and the default form is used, the function falls back to `SignupFormOnlyEmail`.
- On `POST` requests:
  - Validates the form data.
  - Saves the user and sends a `signup_complete` signal.
  - Redirects to `success_url` or `userena_signup_complete` if `success_url` is not provided.
  - Logs out the current user if they are authenticated.
  - Logs in the new user if `USERENA_SIGNIN_AFTER_SIGNUP` is enabled and activation is not required.
- On `GET` requests:
  - Renders the signup form using the specified `template_name`.
  - Adds the form to the `extra_context` dictionary for template rendering.

### `activate`

This function handles rendering the activation process based on the provided `activation_key`. It checks if the key is valid, expired, or invalid and responds accordingly. Here we quote its docstring:

> Activate a user with an activation key.
>
> The key is a SHA1 string. When the SHA1 is found with an `UserenaSignup`, the `User` of that account will be activated. After a successful activation, the view will redirect to `success_url`. If the SHA1 is not found, the user will be shown the `template_name` template displaying a fail message. If the SHA1 is found but expired, `retry_template_name` is used instead, so the user can proceed to `activate_retry` to get a new activation key.

#### Used Decorators {id=used_decorator_2}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>

#### Input Parameters {id=input_param_2}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `activation_key`: String of a SHA1 string of 40 characters long. A SHA1 is always 160 bits long, with 4 bits per character, making it 40 characters long.
- `template_name`: String containing the template name that is used when the `activation_key` is invalid and the activation fails. Defaults to `userena/activate_fail.html`.
- `retry_template_name`: String containing the template name that is used when the `activation_key` is expired. Defaults to `userena/activate_retry.html`.
- `success_url`: String containing the URL where the user should be redirected to after a successful activation. Will replace `%(username)s` with string formatting if supplied. If `success_url` is left empty, will direct to `userena_profile_detail` view.
- `extra_context`: Dictionary containing variables which could be added to the template context. Defaults to an empty dictionary.

#### Behavior {id=behavior_2}

- If the activation key is **valid** and not expired, the user is activated, logged in, and redirected to `success_url`.
- If the activation key is **expired**, the user is shown the `retry_template_name` template.
- If the activation key is **invalid**, the user is shown the `template_name` template.


### `activate_pending`

This function checks if the account is not active and, if so, renders the activation pending template. This view takes precedence over the `disabled_account` view unless the account was disabled after activation completion. Here we quote its docstring:

> Checks if the account is not active, if so, returns the activation pending template. This view is meant to take precedent over the ``disabled_account`` view unless we know that the account was disabled after completion.

#### Input Parameters {id=input_param_3}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: String defining the username of the user that made the action.
- `template_name`: String defining the name of the template to use. Defaults to ``userena/activate_pending.html``.

**Keyword arguments**

- `extra_context`: A dictionary containing extra variables that should be passed to the rendered template. The ``account`` key is always the ``User`` that completed the action.

#### Behavior {id=behavior_3}

- If the user account is **not active** and the activation process was **not completed**, the function renders the `activate_pending` template.
- If the activation process was **completed** but the user is **not active**, the function redirects to the `userena_disabled` view.
- The `extra_context` dictionary is passed to the template for additional context.

### `activate_retry`

This function reissues a new `activation_key` for the user with an expired `activation_key`. If the `activation_key` does not exist, or if `USERENA_ACTIVATION_RETRY` is set to `False`, the user is redirected to the `activate` view for error message display. Here we quote its docstring:

> Reissue a new ``activation_key`` for the user with the expired ``activation_key``.
>
> If ``activation_key`` does not exist, or ``USERENA_ACTIVATION_RETRY`` is set to False and for any other error condition, the user is redirected to :func:`activate` for error message display.

#### Used Decorators {id=used_decorator_4}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>

#### Input Parameters {id=input_param_4}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `activation_key`: String of a SHA1 string of 40 characters long. A SHA1 is always 160 bits long, with 4 bits per character, making it 40 characters long.
- `template_name`: String containing the template name that is used when a new `activation_key` has been created. Defaults to ``userena/activate_retry_success.html``.
- `extra_context`: Dictionary containing variables which could be added to the template context. Defaults to an empty dictionary.

#### Behavior {id=behavior_4}

- If `USERENA_ACTIVATION_RETRY` is `False`, the user is redirected to the `activate` view.
- If the `activation_key` is expired, a new `activation_key` is reissued, and the `activate_retry_success` template is rendered.
- If the `activation_key` is not expired or does not exist, the user is redirected to the `activate` view with an appropriate error message.

### `email_confirm`

This function confirms an email address using a confirmation key. If the confirmation is successful, the user's email address is updated, and they are redirected to `success_url`. If the confirmation fails, a fail message is displayed using the specified template. Here we quote its docstring:

> Confirms a new email address by running :func:`User.objects.confirm_email` method. If the method returns an :class:`User`, the user will have their new email address set and be redirected to ``success_url``. If no ``User`` is returned, the user will be shown a fail message from ``template_name``.

#### Used Decorators {id=used_decorator_5}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>

#### Input Parameters {id=input_param_5}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `confirmation_key`: String with a SHA1 representing the confirmation key used to verify a new email address.
- `template_name`: String containing the template name which should be rendered when confirmation fails. When confirmation is successful, no template is needed because the user will be redirected to `success_url`. Defaults to ``userena/email_confirm_fail.html``.
- `success_url`: String containing the URL which is redirected to after a successful confirmation. The supplied argument must be able to be rendered by the ``reverse`` function.
- `extra_context`: Dictionary of variables that are passed on to the template supplied by ``template_name``.

#### Behavior {id=behavior_5}

- If the confirmation key is valid and the email is confirmed successfully:
  - The user's email address is updated.
  - A success message is displayed if `USERENA_USE_MESSAGES` is enabled.
  - The user is redirected to `success_url` or the `userena_email_confirm_complete` view if `success_url` is not provided.
- If the confirmation key is invalid:
  - The `email_confirm_fail` template is rendered with the provided `extra_context`.

### `direct_to_user_template`

This function is a simple wrapper for Django's `direct_to_template` view. It renders a template for a specific user, allowing the template to access the user's details. Here we quote its docstring:

> Simple wrapper for Django's :func:`direct_to_template` view.
>
> This view is used when you want to show a template to a specific user. A wrapper for :func:`direct_to_template` where the template also has access to the user that is found with ``username``. For example, used after signup, activation, and confirmation of a new email.

#### Input Parameters {id=input_param_6}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: String defining the username of the user that made the action.
- `template_name`: String defining the name of the template to use. Defaults to ``userena/signup_complete.html``.

**Keyword arguments**

- `extra_context`: A dictionary containing extra variables that should be passed to the rendered template. The ``account`` key is always the ``User`` that completed the action.

#### Behavior {id=behavior_6}

- Retrieves the user object based on the provided `username`.
- Adds the `viewed_user` and `profile` (user profile) to the `extra_context` dictionary.
- Renders the specified template with the updated context.

#### Extra Context

- `viewed_user`: The currently viewed :class:`User`.
- `profile`: The profile of the currently viewed user.

### `disabled_account`

This function checks if the account is disabled and, if so, renders the disabled account template. Here we quote its docstring:

> Checks if the account is disabled, if so, returns the disabled account template.

#### Input Parameters {id=input_param_7}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: String defining the username of the user that made the action.
- `template_name`: String defining the name of the template to use. Defaults to ``userena/signup_complete.html``.

**Keyword arguments**

- `extra_context`: A dictionary containing extra variables that should be passed to the rendered template. The ``account`` key is always the ``User`` that completed the action.

#### Behavior {id=behavior_7}

- Retrieves the user object based on the provided `username`.
- If the user is active, raises an `Http404` error.
- If the user is inactive:
  - Adds the `viewed_user` and `profile` (user profile) to the `extra_context` dictionary.
  - Renders the specified template with the updated context.

#### Extra Context {id=extra_context_7}

- `viewed_user`: The currently viewed :class:`User`.
- `profile`: The profile of the currently viewed user.

### `landing`

This function handles user sign-in using email or username with password. If the credentials are valid and the user is active, the user is logged in and redirected to the appropriate page. Here we quote its docstring:

> Signs a user in by combining email/username with password. If the combination is correct and the user :func:`is_active`, the :func:`redirect_signin_function` is called with the arguments ``REDIRECT_FIELD_NAME`` and an instance of the :class:`User` who is trying to log in. The returned value of the function will be the URL that is redirected to.
>
> A user can also select to be remembered for ``USERENA_REMEMBER_DAYS``.

#### Used Decorators {id=used_decorator_8}

<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>


#### Input Parameters {id=input_param_8}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `auth_form`: Form to use for signing the user in. Defaults to the :class:`AuthenticationForm` supplied by userena.
- `template_name`: String defining the name of the template to use. Defaults to ``landing.html``.
- `redirect_field_name`: Form field name which contains the value for a redirect to the succeeding page. Defaults to ``next`` and is set in ``REDIRECT_FIELD_NAME`` setting.
- `redirect_signin_function`: Function which handles the redirect. This function gets the value of ``REDIRECT_FIELD_NAME`` and the :class:`User` who has logged in. It must return a string which specifies the URI to redirect to.
- `extra_context`: A dictionary containing extra variables that should be passed to the rendered template. The ``form`` key is always the ``auth_form``.

#### Behavior {id=behavior_8}

- If the user is already authenticated, they are redirected to `/robots`.
- On `POST` requests:
  - Validates the form data.
  - Authenticates the user using the provided credentials.
  - If the user is active, logs them in and sets a session expiry based on the "remember me" option.
  - Redirects the user to the appropriate page using the `redirect_signin_function`.
  - If the user is inactive, redirects them to the `userena_disabled` view.
- On `GET` requests:
  - Renders the sign-in form using the specified `template_name`.
  - Adds the form, errors, and redirect information to the `extra_context` dictionary.

#### Extra Context {id=extra_context_8}

- `form`: Form used for authentication supplied by ``auth_form``.
- `errors`: Dictionary containing error messages for invalid credentials.
- `next`: The URL to redirect to after successful sign-in.

### `signin`

This function handles user sign-in using email or username with password. If the credentials are valid and the user is active, the user is logged in and redirected to the appropriate page. Here we quote its docstring:

> Signs a user in by combining email/username with password. If the combination is correct and the user :func:`is_active`, the :func:`redirect_signin_function` is called with the arguments ``REDIRECT_FIELD_NAME`` and an instance of the :class:`User` who is trying to log in. The returned value of the function will be the URL that is redirected to.
>
> A user can also select to be remembered for ``USERENA_REMEMBER_DAYS``.

#### Used Decorators {id=used_decorator_9}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>

#### Input Parameters {id=input_param_9}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `auth_form`: Form to use for signing the user in. Defaults to the :class:`AuthenticationForm` supplied by userena.
- `template_name`: String defining the name of the template to use. Defaults to ``userena/signin_form.html``.
- `redirect_field_name`: Form field name which contains the value for a redirect to the succeeding page. Defaults to ``next`` and is set in ``REDIRECT_FIELD_NAME`` setting.
- `redirect_signin_function`: Function which handles the redirect. This function gets the value of ``REDIRECT_FIELD_NAME`` and the :class:`User` who has logged in. It must return a string which specifies the URI to redirect to.
- `extra_context`: A dictionary containing extra variables that should be passed to the rendered template. The ``form`` key is always the ``auth_form``.

#### Behavior {id=behavior_9}

- On `POST` requests:
  - Validates the form data.
  - Authenticates the user using the provided credentials.
  - If the user is active:
    - Logs them in and sets a session expiry based on the "remember me" option.
    - Displays a success message if `USERENA_USE_MESSAGES` is enabled.
    - Sends a signal that a user has signed in.
    - Redirects the user to the appropriate page using the `redirect_signin_function`.
  - If the user is inactive:
    - Redirects to the `userena_disabled` view if activation is completed.
    - Redirects to the `userena_activate_pending` view if activation is pending.
- On `GET` requests:
  - Renders the sign-in form using the specified `template_name`.
  - Adds the form and redirect information to the `extra_context` dictionary.

#### Extra Context {id=extra_context_9}

- `form`: Form used for authentication supplied by ``auth_form``.
- `next`: The URL to redirect to after successful sign-in.

### `email_change`

This function allows a user to change their email address. If the form is valid, the email is updated, and the user is redirected to the success URL. Here we quote its docstring:

> Change email address.

#### Used Decorators {id=used_decorator_10}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="permission-required-or-403-decorator"></include>

#### Input Parameters {id=input_param_10}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: String of the username which specifies the current account.
- `email_form`: Form that will be used to change the email address. Defaults to :class:`ChangeEmailForm` supplied by userena.
- `template_name`: String containing the template to be used to display the email form. Defaults to ``userena/email_form.html``.
- `success_url`: Named URL where the user will get redirected to when successfully changing their email address. When not supplied, will redirect to ``userena_email_complete`` URL.
- `extra_context`: Dictionary containing extra variables that can be used to render the template. The ``form`` key is always the form supplied by the keyword argument ``form``, and the ``user`` key is the user whose email address is being changed.

#### Behavior {id=behavior_10}

- On `POST` requests:
  - Validates the form data.
  - If the form is valid, updates the user's email address.
  - Sends a signal that the email has changed.
  - Redirects the user to the `success_url` or the `userena_email_change_complete` view if `success_url` is not provided.
- On `GET` requests:
  - Renders the email change form using the specified `template_name`.
  - Adds the form and user profile to the `extra_context` dictionary.

#### Extra Context {id=extra_context_10}

- `form`: Form that is used to change the email address supplied by ``form``.
- `profile`: The profile of the user whose email address is being changed.

### `password_change`

This function allows a user to change their password. If the form is valid, the password is updated, and the user is redirected to the success URL. Here we quote its docstring:

> Change password of user.
>
> This view is almost a mirror of the view supplied in :func:`contrib.auth.views.password_change`, with the minor change that in this view we also use the username to change the password. This was needed to keep our URLs logical (and REST) across the entire application. And that in a later stadium administrators can also change the users password through the web application itself.

#### Used Decorators {id=used_decorator_11}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="permission-required-or-403-decorator"></include>

#### Input Parameters {id=input_param_11}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: String supplying the username of the user whose password is about to be changed.
- `template_name`: String of the name of the template that is used to display the password change form. Defaults to ``userena/password_form.html``.
- `pass_form`: Form used to change the password. Default is the form supplied by Django itself named ``PasswordChangeForm``.
- `success_url`: Named URL that is passed onto a :func:`reverse` function with ``username`` of the active user. Defaults to the ``userena_password_complete`` URL.
- `extra_context`: Dictionary of extra variables that are passed on to the template. The ``form`` key is always used by the form supplied by ``pass_form``.

#### Behavior {id=behavior_11}

- On `POST` requests:
  - Validates the form data.
  - If the form is valid, updates the user's password.
  - Sends a signal that the password has changed.
  - Redirects the user to the `success_url` or the `userena_password_change_complete` view if `success_url` is not provided.
- On `GET` requests:
  - Renders the password change form using the specified `template_name`.
  - Adds the form and user profile to the `extra_context` dictionary.

#### Extra Context {id=extra_context_11}

- `form`: Form used to change the password.
- `profile`: The profile of the user whose password is being changed.

### `profile_edit`

This function allows a user to edit their profile. If the form is valid, the profile is updated, and the user is redirected to the success URL. Here we quote its docstring:

> Edit profile.
>
> Edits a profile selected by the supplied username. First checks permissions if the user is allowed to edit this profile, if denied will show a 404. When the profile is successfully edited, will redirect to ``success_url``.

#### Used Decorators {id=used_decorator_12}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="permission-required-or-403-decorator"></include>

#### Input Parameters {id=input_param_12}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: Username of the user whose profile should be edited.
- `edit_profile_form`: Form that is used to edit the profile. The :func:`EditProfileForm.save` method of this form will be called when the form :func:`EditProfileForm.is_valid`. Defaults to :class:`EditProfileForm` from userena.
- `template_name`: String of the template that is used to render this view. Defaults to ``userena/profile_form.html``.
- `success_url`: Named URL which will be passed on to a Django ``reverse`` function after the form is successfully saved. Defaults to the ``userena_detail`` URL.
- `extra_context`: Dictionary containing variables that are passed on to the ``template_name`` template. The ``form`` key will always be the form used to edit the profile, and the ``profile`` key is always the edited profile.

#### Behavior {id=behavior_12}

- On `POST` requests:
  - Validates the form data.
  - If the form is valid, updates the user's profile.
  - Displays a success message if `USERENA_USE_MESSAGES` is enabled.
  - Sends a signal that the profile has changed.
  - Redirects the user to the `success_url` or the `userena_profile_detail` view if `success_url` is not provided.
- On `GET` requests:
  - Renders the profile edit form using the specified `template_name`.
  - Adds the form and profile to the `extra_context` dictionary.

#### Extra Context {id=extra_context_12}

- `form`: Form that is used to alter the profile.
- `profile`: Instance of the ``Profile`` that is edited.

### `profile_detail`

This function provides a detailed view of a user's profile. It ensures that the requesting user has permission to view the profile and renders the appropriate template. Here we quote its docstring:

> Detailed view of an user.

#### Input Parameters {id=input_param_13}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `username`: String of the username of which the profile should be viewed.
- `template_name`: String representing the template name that should be used to display the profile. Defaults to the value specified in `userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE`.
- `extra_context`: Dictionary of variables which should be supplied to the template. The ``profile`` key is always the current profile.

#### Behavior {id=behavior_13}

- Retrieves the user object based on the provided `username`.
- Retrieves the user's profile using `get_user_profile`.
- Checks if the requesting user has permission to view the profile using `profile.can_view_profile`. If not, raises a `PermissionDenied` exception.
- Adds the profile and `hide_email` setting (from `userena_settings.USERENA_HIDE_EMAIL`) to the `extra_context` dictionary.
- Renders the specified template with the updated context.

#### Extra Context {id=extra_context_13}

- `profile`: Instance of the currently viewed ``Profile``.
- `hide_email`: Boolean indicating whether the email should be hidden, based on `userena_settings.USERENA_HIDE_EMAIL`.

### `profile_list`

This function returns a paginated list of all public profiles. It can be disabled by setting `USERENA_DISABLE_PROFILE_LIST` to `True` in your settings. Here we quote its docstring:

> Returns a list of all profiles that are public.
>
> It's possible to disable this by changing ``USERENA_DISABLE_PROFILE_LIST`` to ``True`` in your settings.

#### Input Parameters {id=input_param_14}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `page`: Integer of the active page used for pagination. Defaults to the first page.
- `template_name`: String defining the name of the template that is used to render the list of all users. Defaults to ``userena/profile_list.html``.
- `paginate_by`: Integer defining the amount of displayed profiles per page. Defaults to 50 profiles per page.
- `extra_context`: Dictionary of variables that are passed on to the ``template_name`` template.

#### Behavior {id=behavior_14}

- Retrieves the current page number from the request's query parameters. If not provided or invalid, defaults to the value of the `page` parameter.
- If `USERENA_DISABLE_PROFILE_LIST` is `True` and the requesting user is not a staff member, raises an `Http404` error.
- Retrieves the list of visible profiles using `profile_model.objects.get_visible_profiles(request.user)`.
- Uses `ProfileListView` to paginate and render the list of profiles.
- Adds the `extra_context` dictionary to the template context.

#### Extra Context {id=extra_context_14}

- `profile_list`: A list of profiles.
- `is_paginated`: A boolean representing whether the results are paginated.

If the result is paginated, the following additional variables are included:

- `paginator`: An instance of ``django.core.paginator.Paginator``.
- `page_obj`: An instance of ``django.core.paginator.Page``.

#### Deprecation Warning

This function is deprecated. Use `ProfileListView` instead.

### `signupsample`

This function handles user sign-up, requiring a username, email, and password. After sign-up, the user receives an email with an activation link to activate their account. On successful sign-up, the user is redirected to `success_url`. Here we quote its docstring:

> Signup requiring a username, email, and password. After signup, a user gets an email with an activation link used to activate their account. After successful signup, redirects to ``success_url``.

#### Used Decorators {id=used_decorator_15}

<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>
<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>

#### Input Parameters {id=input_param_15}

We quote the docstring notes on the input parameters as they seem sufficient.

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .
- `signup_form`: Form that will be used to sign up a user. Defaults to userena's :class:`SignupFormExtra`.
- `template_name`: String containing the template name that will be used to display the signup form. Defaults to ``userena/signuphtml.html``.
- `success_url`: String containing the URI which should be redirected to after a successful signup. If not supplied, will redirect to ``userena_signup_complete`` view.
- `extra_context`: Dictionary containing variables which are added to the template context. Defaults to a dictionary with a ``form`` key containing the ``signup_form``.

#### Behavior {id=behavior_15}

- If signup is disabled (via `USERENA_DISABLE_SIGNUP`), the function raises a `PermissionDenied` exception.
- If `USERENA_WITHOUT_USERNAMES` is enabled and the default form is used, the function falls back to `SignupFormOnlyEmail`.
- On `POST` requests:
  - Validates the form data.
  - If the form is valid:
    - Saves the user and sends a `signup_complete` signal.
    - If a referral ID is present in the session, associates the new user with the referrer.
    - Logs out the current user if they are authenticated.
    - Logs in the new user if `USERENA_SIGNIN_AFTER_SIGNUP` is enabled and activation is not required.
    - Returns a JSON response with the cleaned form data.
  - If the form is invalid, returns a JSON response with the form errors and a `400` status code.
- On `GET` requests:
  - Renders the signup form using the specified `template_name`.
  - Adds the form to the `extra_context` dictionary for template rendering.

#### Extra Context {id=extra_context_15}

- `form`: Form supplied by ``signup_form``.

### `settings`

This function renders the settings page for the authenticated user.
It uses the [`settings.html`](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/accounts/templates/settings.html)
template and passes the user's context to the template.

#### Input Parameters {id=input_param_16}

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .


#### Behavior {id=behavior_16}

- Retrieves the user's context using the `get_user` function.
- Renders the [`settings.html`](https://github.com/smoghadamreza/xtrader/blob/main/xtrader/accounts/templates/settings.html)
template with the user's context.


### `get_telegram`

This function checks if the authenticated user has a Telegram ID associated with their profile. If not, it generates and returns an activation code for linking a Telegram account. Here we quote its behavior:

> Checks if the authenticated user has a Telegram ID. If not, generates and returns an activation code for linking a Telegram account.

#### Input Parameters {id=input_param_17}

- `request`: The incoming <include from="repeatable-texts.topic" element-id="http-request"/> .

#### Behavior {id=behavior_17}

- Retrieves the authenticated user from the request.
- If the user is not authenticated, returns a JSON response with the message `'not login'`.
- Retrieves the user's profile using `Profile.objects.filter(user=user).first()`.
- Constructs a result dictionary with the following keys:
  - `telegram_id`: `True` if the user has a Telegram ID linked to their profile, otherwise `False`.
  - `activation_code`: The activation code for linking a Telegram account if no Telegram ID is found, otherwise `False`.
- Returns the result as a JSON response.

### `new_deposit`

This function handles new deposit requests from an external service. It processes the deposit details, creates a deposit record, and sends a notification if the deposit is successful. Here we describe its behavior:

> Processes a new deposit request, creates a deposit record, and sends a notification if successful.

#### Used Decorators {id=used_decorator_18}

<include from="repeatable-texts.topic" element-id="csrf-exempt-decorator"></include>
<include from="repeatable-texts.topic" element-id="transaction-atomic-decorator"></include>

#### Behavior {id=behavior_18}

- Validates that the request method is `POST`. If not, returns a JSON response with the message `'bad request'`.
- Attempts to log the request details (GET, body, and POST data) for debugging purposes.
- Extracts the `nonce` from the request's query parameters.
- Parses the request body to extract deposit details (e.g., `address_in`, `address_out`, `txid_in`, `txid_out`, `value`, `coin`, etc.).
- Creates a deposit record using the `Deposit.create` method, passing the `nonce` and parsed parameters.
- If the deposit is successfully created:
  - Sends a Telegram notification with details of the deposit (e.g., amount and final value).
  - Returns a JSON response with the result of the deposit creation.
- If the deposit creation fails, returns a JSON response with the failure result.

#### Notes {id=notes_18}

- The function is designed to handle incoming deposit requests from an external service, such as a cryptocurrency payment gateway.
- The `Deposit.create` method is responsible for validating and saving the deposit details.
- The Telegram notification is sent asynchronously using a separate thread to avoid blocking the main request.

### `get_wallet`

This function retrieves the wallet details for the authenticated user. If the user does not have a wallet address, it returns a status indicating the issue. Here we describe its behavior:

> Retrieves the wallet details for the authenticated user. If no wallet address is found, returns a status indicating the issue.

#### Used Decorators {id=used_decorator_19}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_19}

- Validates that the request method is `GET`. If not, returns a JSON response with the message `'bad request'`.
- Retrieves the authenticated user from the request.
- Calls the `Wallet.get_wallet` method to fetch the wallet details for the user.
- If no wallet address is found, sets the status to `505`. Otherwise, sets the status to `200`.
- Returns a JSON response containing the wallet details and status.

#### Notes {id=notes_19}

- The function requires the user to be authenticated. If the user is not logged in, they are redirected to the `accounts:userena_signin` URL.
- The `Wallet.get_wallet` method is responsible for retrieving the wallet details, including the address.
- The status code `505` indicates that no wallet address was found for the user.

### `check_deposits`

This function checks for new deposits associated with the authenticated user's wallet. If no wallet is found, it returns an error message. Here we describe its behavior:

> Checks for new deposits associated with the authenticated user's wallet. If no wallet is found, returns an error message.

#### Used Decorators {id=used_decorator_20}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_20}

- Validates that the request method is `GET`. If not, returns a JSON response with the message `'bad request'` and a `403` status code.
- Retrieves the authenticated user from the request.
- Fetches the user's wallet using `Wallet.objects.filter(user=user).first()`.
- If no wallet is found, returns a JSON response with the message `'no wallet!'` and a `403` status code.
- If a wallet is found, calls the `wallet.check_deposit()` method to check for new deposits.
- Returns a JSON response with a `200` status code and the result of the deposit check under the key `'newDeposit'`.

#### Notes {id=notes_20}

- The function requires the user to be authenticated. If the user is not logged in, they are redirected to the `accounts:userena_signin` URL.
- The `wallet.check_deposit()` method is responsible for checking for new deposits associated with the wallet.
- The `403` status code is used to indicate errors, such as an invalid request method or a missing wallet.

### `get_deposits`

This function retrieves the deposit history associated with the authenticated user's wallet. If the request method is not `GET`, it returns an error message. Here we describe its behavior:

> Retrieves the deposit history associated with the authenticated user's wallet. If the request method is invalid, returns an error message.

#### Used Decorators {id=used_decorator_21}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_21}

- Validates that the request method is `GET`. If not, returns a JSON response with the message `'bad request'` and a `403` status code.
- Retrieves the authenticated user from the request.
- Fetches the user's wallet using `Wallet.objects.filter(user=user).first()`.
- Calls the `Deposit.get_deposits` method to retrieve the deposit history associated with the wallet.
- Returns a JSON response containing the deposit history under the key `'data'`.

#### Notes {id=notes_21}

- The function requires the user to be authenticated. If the user is not logged in, they are redirected to the `accounts:userena_signin` URL.
- The `Deposit.get_deposits` method is responsible for retrieving the deposit history for the specified wallet.
- The `403` status code is used to indicate an invalid request method.

### `account_status`

This function retrieves the status of the authenticated user's account, including whether they are following a pro trader, have an exchange linked, and have a Telegram account connected. Here we describe its behavior:

> Retrieves the status of the authenticated user's account, including following status, exchange linkage, and Telegram connection.

#### Used Decorators {id=used_decorator_22}

<include from="repeatable-texts.topic" element-id="login-required-decorator"></include>

#### Behavior {id=behavior_22}

- Retrieves the authenticated user from the request.
- Initializes a `status` dictionary with the following keys:
  - `following`: Indicates whether the user is following a pro trader.
  - `exchange`: Indicates whether the user has an exchange linked.
  - `telegram`: Indicates whether the user has a Telegram account connected.
- Checks if the user is following a pro trader using `Follow.objects.filter(follower=user).first()`:
  - If following, sets `status['following']` to `True` and includes the pro trader's brand name under `status['protrader']`.
- Checks if the user has an exchange linked using `Exchange.objects.filter(trader=user).first()`:
  - If an exchange is found, sets `status['exchange']` to `True`.
- Retrieves the user's profile using `Profile.objects.filter(user=user).first()`:
  - If the profile exists and has a `telegram_id`, sets `status['telegram']` to `True`.
- Returns a JSON response containing the `status` dictionary.

#### Notes {id=notes_22}

- The function requires the user to be authenticated. If the user is not logged in, they are redirected to the `accounts:userena_signin` URL.
- The `status` dictionary provides a summary of the user's account status, which can be used to customize the user experience.

### `SignoutView`

This function handles user sign-out operations. Here we quote its docstring:  

> Signs out the user and adds a success message ``You have been signed out.`` If next_page is defined you will be redirected to the URI. If  
> not the template in template_name is used.  

#### Used Decorators {id=used_decorator_23}  
<include from="repeatable-texts.topic" element-id="userena-secure-required-decorator"></include>  

#### Input parameters {id=input_param_23}  
We quote the docstring notes on the input parameters as they seem sufficient.  

- `next_page`: A string specifying the URI to redirect to. Defaults to `USERENA_REDIRECT_ON_SIGNOUT`.  
- `template_name`: String defining the template name to use. Defaults to ``userena/signout.html``.  

#### Behavior {id=behavior_23}  

- If the user is authenticated and `USERENA_USE_MESSAGES` is enabled:  
  - Adds a success message ("You have been signed out.") to the request.  
- Triggers the `account_signout` signal with the current user as an argument.  
- Calls the `Signout` function to terminate the user session.  
- Returns an empty `JsonResponse` (note: overrides the commented-out template/redirect behavior).  



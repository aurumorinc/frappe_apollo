

# OAuth 2.0 (Partners)

## Overview

Apollo supports the OAuth 2.0 authorization flow to build Apollo integrations. By using this flow, your app's users can enter their Apollo account credentials and grant you permission to retrieve data via Apollo's APIs.

## Preview the Authorization Flow for Your Users

Apollo supports the OAuth 2.0 authorization code grant type. Your app's users will follow these 3 steps when using their Apollo credentials to authenticate:

1. The user enters their Apollo credentials in your app. A new browser window opens.
2. The user can see your app name and logo, as well as the permissions you are requesting they authorize. After reviewing the requested permissions, the user grants your app access.
3. The user is redirected back to your app.

Unseen to your users, the redirect URL you provide to Apollo includes an authorization code in the query string. Your app sends a request to the OAuth 2.0 server to exchange the authorization code for an access token.

## Before You Start Building

The end users of your app or integration must have the appropriate permissions in their Apollo account to implement the authorization flow.

![Necessary Apollo permission](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i23.png)

> 🚧 Unauthorized Users
>
> To authorize your integration via OAuth, an Apollo end user must have the necessary permissions. For teams on an Apollo plan that enables custom permission profiles, the user needs to have the <b>Can authorize third-party apps/integrations via OAuth</b> permission enabled in Apollo. For teams on a plan that doesn't include custom permissions, the user must be assigned either the Admin or Billing and Seat Manager permission profile.
>
> If a user without this permission attempts to authorize, they will be redirected according to the OAuth redirect URL you will set later in this process. The following error code will be appended to the redirect URL:
>
> ```
> status\_code=403\&error\_message=You%20do%20not%20have%20permission%20to%20connect%20integrations.%20Please%20contact%20your%20Apollo%20admin%20to%20review%20and%20authorize%20this%20integration
> ```
>
> <b>Recommended handling:</b> You can choose to display a user-friendly message, such as a pop-up or other visual element, explaining the required permissions. If no message is configured, the user will only see the error message within the URL.

<br />

This authorization method supports only the API endpoints listed in Apollo's public API documentation. Ensure that the endpoints you need for your use case are available before implementing OAuth.

If you have the appropriate permissions and have confirmed the availability of endpoints, proceed to [step 1](https://docs.apollo.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo).

## Build OAuth Authorization Flow

### Step 1: Register Your App With Apollo

To set up an OAuth flow, you need to provide Apollo with details about the purpose of your organization using the flow. Once registration is approved, you can <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#optional-test-the-oauth-flow-before-building">use the Apollo playground</a> to test the OAuth flow before attempting to implement it.

To register your application with Apollo:

1. Launch Apollo and click **Settings** > **<a href="https://app.apollo.io/#/settings/integrations" target="_blank">Integrations</a>**.
2. Find the API option and click **Connect**.
3. Click **OAuth registration**, then enter the following information. When your users authenticate with an Apollo account, they will see the app name, app logo, and scopes you enter here.
   * **App Name**: The name of your app or product.
   * **App Logo**: Upload the logo for your app.
   * **OAuth Redirect URL**: The URL that the user will be redirected to after they authorize your app for the requested scopes. This URL must use `https`. To make multiple URLs available for use, add the URLs with each URL separated by a comma. Multiple redirect URLs enables you to implement different OAuth flows and redirect users based on the needs of each flow, such as flows for different types of users or flows for different areas of your product. You can add up to 4 redirect URLs.
   * **Scopes**: Set the scopes, or permissions, for your app. Each scope provides access to specific Apollo API endpoints. Only add scopes that are necessary for your app's functionality. By default, Apollo adds `read_user_profile`, which provides basic user info, and `app_scopes` for all selected scopes.

![Register as a partner](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i22.png)

<br />

> 🚧 Locked In
>
> In the future, if you edit these scopes, you need to repeat this entire authorization flow to set up OAuth again.

4. Click **Submit**.
5. Copy the client ID and secret to use in the next steps. <br /><br />The client ID is a public identifier for your app and is used to identify your app during the OAuth flow. It appears on the OAuth integration page of the Apollo developer portal. <br /><br />The client secret is a confidential key used to authenticate your app. It secures communication between your app and Apollo's OAuth server. The only time the secret is displayed is when it is generated. Store it in a secure location as it will not be shown again.

![alt text](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i3.png "Logo Title Text 1")

With the client ID and secret in hand, you are ready to <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-2-build-authorization-code-flow">build the authorization code flow</a>.

### Optional: Test the OAuth Flow Before Building

Once your app is registered with Apollo, the playground becomes available in the developer portal. The playground enables you to quickly test the OAuth flow before you attempt to implement it in your app.

To test the OAuth flow:

1. Click **OAuth Integration** > **Playground**.

![](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i16.png)

2. Enter a redirect URL, then click **Get authorization code**. Copy this code to use in the next step.

![](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i17.png)

3. Paste the authorization code from the previous playground step and the client secret that you generated when registering your app. Then, click **Get access token**. Copy the access token to use in the next step.

![](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i18.png)

4. Paste the access token from the previous playground step. Then, click **Fetch data**.

![](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i19.png)

If you're successful in retrieving data, proceed to building the OAuth flow in your app.

### Step 2: Build Authorization Code Flow

With your client ID and secret in hand from <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">step 1</a>, you're ready to build the authorization code flow. When sending users to Apollo's OAuth 2.0 server, the authorization URL identifies your app and defines the resources (scopes) it's requesting to access on behalf of users.

The following parameters can be used to build your authorization URL:

<table>
  <tr>
    <td>
      <strong>Parameter</strong>
    </td>

    <td>
      <strong>Required</strong>
    </td>

    <td>
      <strong>Description</strong>
    </td>

    <td>
      <strong>Example</strong>
    </td>
  </tr>

  <tr>
    <td>client\_id</td>
    <td>yes</td>

    <td>
      The client ID identifies your app. The client ID was generated in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      .
    </td>

    <td>
      <code>-FaKj9ikI5rafgwPKJId1DwbzhR1VHvQAe7UEAVH\_5k</code>
    </td>
  </tr>

  <tr>
    <td>redirect\_uri</td>
    <td>yes</td>

    <td>
      After a user authorizes your app for the requested scopes, they are
      redirected to this URL. This should be the same as 1 of the OAuth
      Redirect URLs you entered in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      .
    </td>

    <td>
      <code>[https://www.example.com/callback](https://www.example.com/callback)</code>
    </td>
  </tr>

  <tr>
    <td>response\_type</td>
    <td>yes</td>

    <td>
      This must be <code>code</code>
    </td>

    <td>
      <code>code</code>
    </td>
  </tr>

  <tr>
    <td>scope</td>
    <td>no</td>

    <td>
      To request specific permissions, you should include the scope
      parameter in your authorization request. If this parameter is not
      defined, the scopes you selected in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      {' '}

      are used.

      <p>
        Each scope you add needs to be separated by URL-encoded spaces.
      </p>

      If you're passing the scope parameter in the URL and need{' '}
      <code>read\_user\_profile</code> access, ensure you include it in the
      scope parameter.
    </td>

    <td>
      <code>contacts\_search%20person\_read</code>
    </td>
  </tr>

  <tr>
    <td>state</td>
    <td>no</td>

    <td>
      A unique string value that you can use to maintain the user's state
      when they are redirected back to your app. It ensures the response
      matches the initial request by including and verifying the state
      value during the redirection process.
    </td>

    <td>
      <code>WeHH\_yy2irpl8UYAvv-my</code>
    </td>
  </tr>
</table>

With your parameters in mind, call the following endpoint:

```
https://app.apollo.io/#/oauth/authorize?client_id=<your_client_id>&redirect_uri=<redirect_uri>&response_type=code&scope=contacts_search%20person_read&state=xxxxxxxx
```

This directs users to the Apollo log-in options. After the user submits valid Apollo log-in credentials, they can review the permissions you are requesting

If they authorize access, you receive an authorization code from Apollo, and the user is redirected to the redirect URL you provided to Apollo.

![alt text](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i13.png "Logo Title Text 1")

### Step 3: Exchange Authorization Codes for Access Tokens

With the authorization code from <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-2-build-authorization-code-flow">step 2</a>, you can obtain the access token and refresh token that will be used for subsequent requests to the Apollo API.

To retrieve access tokens, call the following endpoint using the following required parameters:

```http
POST https://app.apollo.io/api/v1/oauth/token
```

<table>
  <tr>
    <td>
      <strong>Parameter</strong>
    </td>

    <td>
      <strong>Description</strong>
    </td>

    <td>
      <strong>Example</strong>
    </td>
  </tr>

  <tr>
    <td>grant\_type</td>

    <td>
      This must be <code>authorization\_code</code>.
    </td>

    <td>
      <code>authorization\_code</code>
    </td>
  </tr>

  <tr>
    <td>code</td>

    <td>
      The authorization code received from the OAuth 2.0 server in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-2-build-authorization-code-flow">
        step 2
      </a>

      .
    </td>

    <td>
      <code>MUsgYj77Jc8r07qH2szUh125xqi2AV7eBhsfPnYOhmo</code>
    </td>
  </tr>

  <tr>
    <td>client\_id</td>

    <td>
      Your app's client ID. This was generated in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      .
    </td>

    <td>
      <code>vvZd-i\_3MsfI6gmktGJY7F-kTE42SrO1RB9W8avPp0h</code>
    </td>
  </tr>

  <tr>
    <td>client\_secret</td>

    <td>
      Your app's client secret. This was generated in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      .
    </td>

    <td>
      <code>N6CW\_m\_0FNl8hapshH4Wy4jr3uT8XqsERzdniY74Tw5</code>
    </td>
  </tr>

  <tr>
    <td>
      redirect\_uri (<i>optional</i>)
    </td>

    <td>
      Only utilize this parameter if you want to change the redirect URL
      to 1 of the redirect URLs you provided either in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      {' '}

      or as a scope in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-2-build-authorization-code-flow">
        step 2
      </a>

      .
    </td>

    <td>
      <code>[https://www.example.com/callback](https://www.example.com/callback)</code>
    </td>
  </tr>
</table>

The following is an example of a Python request:

```python
const formData = {
  grant_type: 'authorization_code',
  client_id: YOUR_CLIENT_ID,
  client_secret: YOUR_CLIENT_SECRET,
  redirect_uri: REDIRECT_URI,
  code: req.query.code
};

request.post('https://app.apollo.io/api/v1/oauth/token', { form: formData }, (err, data) => {
  // Handle the returned tokens
}
```

A successful response (JSON) delivers the access token and refresh token.

```json
{
   "access_token": "6vJtf0jt94Km1WxYsH29DE98xVgsNp8wCHFZMcIZdAg",
   "token_type": "Bearer",
   "expires_in": 2592000,
   "refresh_token": "mVml3fpNBkIpIe3_DWvQ4iP_5h_cvYxOp6pYpZwGz0o",
   "scope": "read_user_profile app_scopes opportunity_write",
   "created_at": 1718366695
}
```

<br />

> 📘 Token Expiration
>
> The access token expires after 30 days. The `expires_in` field of the response shows the equivalent of 30 days in seconds.
>
> Be sure to understand how to use the `refresh_token` to [refresh access tokens](https://docs.apollo.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-5-ongoing-refresh-access-tokens)  when building your authorization flow.

### Step 4: Use Access Tokens

Once the authorization code flow is completed, use the access tokens received in [step 3](https://docs.apollo.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-3-exchange-authorization-codes-for-access-tokens) to make requests for your app on behalf of your users. To do this, provide the access token as a bearer token in the authorization HTTP header.

The following example shows how to format the header in Postman to call the [Create a Task](https://docs.apollo.io/reference/create-task) endpoint. Review the [API reference docs](https://docs.apollo.io/reference/people-enrichment) to learn how to use other Apollo API functionality.

![alt text](https://storage.googleapis.com/apollo-public-assets/kb_images/use_oauth/i14.png "Logo Title Text 1")

### Step 5 (Ongoing): Refresh Access Tokens

Access tokens expire after 30 days. Your app can exchange the received refresh token for a new access token and refresh token by calling the following endpoint using the following parameters:

```http
POST https://app.apollo.io/api/v1/oauth/token
```

<table>
  <tr>
    <td>
      <strong>Parameter</strong>
    </td>

    <td>
      <strong>Description</strong>
    </td>

    <td>
      <strong>Example</strong>
    </td>
  </tr>

  <tr>
    <td>grant\_type</td>

    <td>
      This must be <code>refresh\_token</code>.
    </td>

    <td>
      <code>refresh\_token</code>
    </td>
  </tr>

  <tr>
    <td>refresh\_token</td>

    <td>
      The refresh token received when the user authorized your app in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-3-exchange-authorization-codes-for-access-tokens">
        step 3
      </a>

      .
    </td>

    <td>
      <code>MUsgYj77Jc8r07qH2szUh125xqi2AV7eBhsfPnYOhmo</code>
    </td>
  </tr>

  <tr>
    <td>client\_id</td>

    <td>
      Your app's client ID. This was generated in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      .
    </td>

    <td>
      <code>vvZd-i\_3MsfI6gmktGJY7F-kTE42SrO1RB9W8avPp0h</code>
    </td>
  </tr>

  <tr>
    <td>client\_secret</td>

    <td>
      Your app's client secret. This was generated in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      .
    </td>

    <td>
      <code>N6CW\_m\_0FNl8hapshH4Wy4jr3uT8XqsERzdniY74Tw5</code>
    </td>
  </tr>

  <tr>
    <td>
      redirect\_uri (<i>optional</i>)
    </td>

    <td>
      Only utilize this parameter if you want to change the redirect URL
      to 1 of the redirect URLs you provided either in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
        step 1
      </a>

      {' '}

      or as a scope in{' '}

      <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-2-build-authorization-code-flow">
        step 2
      </a>

      .
    </td>

    <td>
      <code>[https://www.example.com/callback](https://www.example.com/callback)</code>
    </td>
  </tr>

  <tr>
    <td>
      scope (<em>optional</em> )
    </td>

    <td>
      To reduce the scopes associated with an existing access token, you
      should include the desired scopes in the request to generate new
      access and refresh tokens.

      <p>
        However, the scope specified in this request must be included in
        the scopes you originally defined in{' '}

        <a href="https://apolloio.readme.io/docs/use-oauth-20-authorization-flow-to-access-apollo-user-information-partners#step-1-register-your-app-with-apollo">
          step 1
        </a>

        . This ensures that the new tokens have the appropriate level of
        access while maintaining security and compliance with the user's
        permissions.
      </p>
    </td>

    <td>
      <code>contacts\_search%20person\_read</code>
    </td>
  </tr>
</table>

The following is an example of a Python request:

A successful response (JSON) delivers a new access token and new refresh token.

```json
{
   "access_token": "IFuV6LMQoNGfzuvJTbqU-jY5DD9iJVTiCoqm3v5uZPU",
   "token_type": "Bearer",
   "expires_in": 2592000,
   "refresh_token": "OeV84CtgzB6NK5BJxA_INSau7svEjhp2IuYOzkZYgQg",
   "scope": "read_user_profile app_scopes opportunity_write",
   "created_at": 1718366832
}
```

The access token should be used to make calls on behalf of the user. When the access token expires, follow these same steps again to retrieve a new one.

> 📘 Revoked Tokens
>
> Once you use the refresh token to generate a new access and refresh token, the existing tokens are automatically revoked and are no longer valid.

### Get User Profile Info

If you need to retrieve a user's basic profile info to determine who owns an access token, call the following endpoint and provide the access token as a bearer token in the authorization HTTP header:

```http
GET https://app.apollo.io/api/v1/users/api_profile
```
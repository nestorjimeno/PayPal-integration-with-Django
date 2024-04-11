# PayPal-API-with-Python

This repository shows how to integrate the PayPal API with Python.


- [Prerrequisites](#prerrequisites)
  - [Get client ID and client secret](#get-client-id-and-client-secret)
  - [Get access token](#get-access-token)
  - [Get sandbox account credentials](#get-sandbox-account-credentials)
- [Make a REST API Request](#make-a-rest-api-request)
  - [HTTP request headers](#http-request-headers)
- [Pay with PayPal](#pay-with-paypal)
  - [Create an order](#create-an-order)
  - [Order request sample](#order-request-sample)
  - [Order response sample](#order-response-sample)
- [Real example](#real-example)


## Prerrequisites

### Get client ID and client secret

PayPal integrations use a client ID and client secret to authenticate API calls.

Here's how to get your client ID and client secret:

1. Select [Log in to Dashboard](https://developer.paypal.com/dashboard/) and log in or sign up.
2. Select **Apps & Credentials**.
3. New accounts come with a **Default Application** in the **REST API apps** section. To create a new project, select **Create App**.
4. Copy the client ID and client secret for your app.

### Get access token

PayPal REST APIs use [OAuth 2.0](https://oauth.net/2/) access tokens to authenticate requests.
To call a REST API in your integration, you'll need to exchange your client ID and client secret for an access token. The access token authenticates your app when calling PayPal REST APIs. Here you can see how get the access token with Python:

```python
import requests

url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
client_id = "TU_CLIENT_ID"
client_secret = "TU_CLIENT_SECRET"

data = {"grant_type": "client_credentials"}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
auth = (client_id, client_secret)

response = requests.post(url, data=data, headers=headers, auth=auth)

access_token = response["access_token"]
```

PayPal returns an access token and the number of seconds the access token is valid. When you make API calls, replace `ACCESS-TOKEN` with your access token in the authorization header: `headers = {"Authorization": "Bearer ACCESS-TOKEN"}`. When your access token expires, call /v1/oauth2/token again to request a new access token.


```json
{
  "scope": "https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller https://uri.paypal.com/services/payments/refund https://api-m.paypal.com/v1/vault/credit-card https://api-m.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://api-m.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks",
  "access_token": "A21AAFEpH4PsADK7qSS7pSRsgzfENtu-Q1ysgEDVDESseMHBYXVJYE8ovjj68elIDy8nF26AwPhfXTIeWAZHSLIsQkSYz9ifg",
  "token_type": "Bearer",
  "app_id": "APP-80W284485P519543T",
  "expires_in": 31668,
  "nonce": "2020-04-03T15:35:36ZaYZlGvEkV4yVSz8g6bAKFoGSEzuy3CQcz3ljhibkOHg"
}
```


### Get sandbox account credentials

The PayPal sandbox is a test environment that mirrors real-world transactions. By default, PayPal developer accounts have 2 sandbox accounts: a personal account for buying and a business account for selling. You'll get the login information for both accounts. Watch sandbox money move between accounts to test API calls.

Take the following steps to get sandbox login information for business and personal accounts:

1. Log into the [Developer Dashboard](https://developer.paypal.com/dashboard/).
2. Select **Testing Tools** > **Sandbox Accounts**. You can create more sandbox accounts by selecting **Create account**.
3. Locate the account you want to get credentials for and select ⋮
4. Select **View/Edit Account** to see mock information such as the account email and system-generated password.
5. Go to [sandbox.paypal.com/signin](https://sandbox.paypal.com/signin) and sign in with the personal sandbox credentials. In a separate browser, sign in with the business sandbox credentials.
6. Make API calls with your app's access token to see sandbox money move between personal and business accounts.

## Make a REST API Request

To make a REST API request, you combine the HTTP `GET`, `POST`, `PUT`, `PATCH`, or `DELETE` method, the URL to the API service, the URI to a resource to query, submit data to, update, or delete, and one or more HTTP request headers. The URL to the API service is either:
1. Sandbox. https://api-m.sandbox.paypal.com
2. Live. https://api-m.paypal.com

Optionally, you can include [query parameters](https://developer.paypal.com/api/rest/requests/#query-parameters) on `GET` calls to filter, limit the size of, and sort the data in the responses.Most `GET`, `POST`, `PUT`, and `PATCH` calls require a JSON request body.

### HTTP request headers

The commonly used HTTP request headers are:
1. Authorization: Required to make API calls, `Authorization: Bearer Access-Token`.
2. Content-Type: The request format, `Content-Type: application/json`.

You can see the complete list in the [PayPal Developers website](https://developer.paypal.com/api/rest/requests/#link-httprequestheaders).

## Pay with PayPal

An order represents a payment between two or more parties. Use the **Orders API** to create, update, retrieve, authorize, and capture orders.

### Create an order

You can create an order by making a POST request to Orders API. The endpoint to create an order is `https://api-m.paypal.com/v2/checkout/orders`.

### Order request sample

Here you have a sample for creating an order:

```python
import requests

headers = {
    'Content-Type': 'application/json',
    'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
    'Authorization': 'Bearer 6V7rbVwmlM1gFZKW_8QtzWXqpcwQ6T5vhEGYNJDAAdn3paCgRpdeMdVYmWzgbKSsECednupJ3Zx5Xd-g',
}

data = {
  "intent": "CAPTURE",
  "purchase_units": [
    {
      "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b",
      "amount": {
        "currency_code": "USD",
        "value": "100.00"
        }
    }
   ],
  "payment_source": {
    "paypal": {
      "experience_context": {
        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
        "brand_name": "EXAMPLE INC",
        "locale": "en-US",
        "landing_page": "LOGIN",
        "shipping_preference": "SET_PROVIDED_ADDRESS",
        "user_action": "PAY_NOW",
        "return_url": "https://example.com/returnUrl",
        "cancel_url": "https://example.com/cancelUrl"
        }
      }
    }
  }

response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, data=data)
```
The only required header parameters are:
1. Authorization: Required to make API calls, `Authorization: Bearer Access-Token`.
2. Content-Type: The request format, `Content-Type: application/json`.

The required data within body request are:
1. `purchase-units`: An array of purchase units. Each purchase unit establishes a contract between a payer and the payee. Each purchase unit represents either a full or partial order that the payer intends to purchase from the payee.
    1. Array of purchase units.
        1. `amount`: The total order amount with an optional breakdown that provides details.
            1. `currency_code`: The [three-character ISO-4217 currency code](https://developer.paypal.com/api/rest/reference/currency-codes/) that identifies the currency.
            2. `value`: The value, which might be an integer or a decimal fraction. For the required number of decimal places for a currency code, see [Currency Codes](https://developer.paypal.com/api/rest/reference/currency-codes/).
2. `intent`: The intent to either capture payment immediately or authorize a payment for an order after order creation. The allowed values are:
    1. `CAPTURE`: The merchant intends to capture payment immediately after the customer makes a payment.
    2. `AUTHORIZE`: The merchant intends to authorize a payment and place funds on hold after the customer makes a payment.
  
The `payment-source` is not a required parameter, but let's explain the above sample code:

1. `payment-source`: The payment source definition.
    1. `paypal`: Indicates that PayPal Wallet is the payment source. Main use of this selection is to provide additional instructions associated with this choice like vaulting.
        1. `experience_context`: Customizes the payer experience during the approval process for payment with PayPal.
            1. `payment_method_preference`: The merchant-preferred payment methods, `UNRESTRICTED` (default) or `IMMEDIATE_PAYMENT_REQUIRED`.
            2. `brand_name`: The label that overrides the business name in the PayPal account on the PayPal site. The pattern is defined by an external party and supports Unicode.
            3. `locale`: The merchant-preferred payment methods, `UNRESTRICTED` (default) or `IMMEDIATE_PAYMENT_REQUIRED`.
            4. `landing_page`: The type of landing page to show on the PayPal site for customer checkout, `LOGIN`, `GUEST_CHECKOUT` or `NO_PREFERENCE` (default).
            5. `shipping_preference`: The location from which the shipping address is derived, `GET_FROM_FILE`, `NO_SHIPPING` (default) or `SET_PROVIDED_ADDRESS`.   
            6. `user_action`: Configures a Continue or Pay Now checkout flow, `CONTINUE` (default) or `PAY_NOW`.
            7. `return_url`: The URL where the customer will be redirected upon approving a payment.
            7. `cancel_url`: The URL where the customer will be redirected upon cancelling the payment approval.

### Order response sample

Here you have a response sample after creating an order:

```json
{
  "id": "5O190127TN364715T",
  "status": "PAYER_ACTION_REQUIRED",
  "payment_source": {
    "paypal": {}
  },
  "links": [
    {
      "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
      "rel": "self",
      "method": "GET"
    },
    {
      "href": "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
      "rel": "payer-action",
      "method": "GET"
    }
  ]
}
```

Here you have the explanation of the response:

1. `id`: The ID of the order.
2. `status`: The order status, `CREATED`, `SAVED`, `APPROVED`, `VOIDED`, `COMPLETED`, `PAYER_ACTION_REQUIRED`.
3. `payment_source`: The payment source used to fund the payment.
4. `links`: An array of request-related HATEOAS links. To complete payer approval, use the `approve` link to redirect the payer.
    1. `href`: The complete target URL.
    2. `rel`: The link relation type, which serves as an ID for a link that unambiguously describes the semantics of the link. See [Link Relations](https://www.iana.org/assignments/link-relations/link-relations.xhtml).
    3. `method`: The HTTP method required to make the related call.

## Real example
  






 














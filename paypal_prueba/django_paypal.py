import os, requests, json
import base64
from dotenv import load_dotenv

load_dotenv()

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PORT = os.getenv("PORT", 8888)

base = "https://api-m.sandbox.paypal.com"



def generate_access_token():
    try:
        paypal_client_id = os.getenv("CLIENT_ID")
        paypal_client_secret = os.getenv("CLIENT_SECRET")
        if not paypal_client_id or not paypal_client_secret:
            raise Exception("MISSING_API_CREDENTIALS")
        
        auth = base64.b64encode(f"{paypal_client_id}:{paypal_client_secret}".encode()).decode("utf-8")
        response = requests.post(f"{base}/v1/oauth2/token", 
                                 data={"grant_type": "client_credentials"}, 
                                 headers={"Authorization": f"Basic {auth}"})
        
        data = response.json()
        return data.get("access_token")
    except Exception as e:
        print("Failed to generate Access Token:", e)



def create_order(cart):
    try:
        # Utiliza la información del carrito pasada desde el frontend para calcular los detalles de la unidad de compra
        print("Información del carrito de compras pasada desde el frontend create_order():", cart)
        
        access_token = generate_access_token()
        url = f"{base}/v2/checkout/orders"
        payload = {
            "intent": "CAPTURE",
            'items': [],
            "purchase_units": [                
                {
                    "amount": {
                        "currency_code": "",
                        "value": ""
                    }
                }]
        }
        suma = 0.0
        for item in cart:
            suma += float(item['price'])*float(item['quantity'])
            payload['items'].append(
                {
                    "name": item['id'],
                    "quantity": item['quantity'],
                    "unit_amount": {
                        "value": item['price'],
                        "currency_code": "USD"
                    },
                }
            )
            payload['purchase_units'][0]['amount']['currency_code'] = 'USD'
        payload['purchase_units'][0]['amount']['value'] = str(suma)
        print(payload)


        response = requests.post(url, 
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": f"Bearer {access_token}",
                                     # Descomenta una de estas líneas para forzar un error para pruebas negativas (solo en modo sandbox). Documentación:
                                     # https://developer.paypal.com/tools/sandbox/negative-testing/request-headers/
                                     # "PayPal-Mock-Response": '{"mock_application_codes": "MISSING_REQUIRED_PARAMETER"}'
                                     # "PayPal-Mock-Response": '{"mock_application_codes": "PERMISSION_DENIED"}'
                                     # "PayPal-Mock-Response": '{"mock_application_codes": "INTERNAL_SERVER_ERROR"}'
                                 },
                                 data=json.dumps(payload))
        
        return handle_response(response)
    except Exception as e:
        print("Failed to create order:", e)


def capture_order(order_id):
    try:
        access_token = generate_access_token()
        url = f"{base}/v2/checkout/orders/{order_id}/capture"
        
        response = requests.post(url, 
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": f"Bearer {access_token}",
                                     # Descomenta una de estas líneas para forzar un error para pruebas negativas (solo en modo sandbox). Documentación:
                                     # https://developer.paypal.com/tools/sandbox/negative-testing/request-headers/
                                     # "PayPal-Mock-Response": '{"mock_application_codes": "INSTRUMENT_DECLINED"}'
                                     # "PayPal-Mock-Response": '{"mock_application_codes": "TRANSACTION_REFUSED"}'
                                     # "PayPal-Mock-Response": '{"mock_application_codes": "INTERNAL_SERVER_ERROR"}'
                                 })
        
        return handle_response(response)
    except Exception as e:
        print("Failed to capture order:", e)


def handle_response(response):
    try:
        json_response = response.json()
        return {
            "json_response": json_response,
            "http_status_code": response.status_code
        }
    except Exception as e:
        error_message = response.text
        raise Exception(error_message)

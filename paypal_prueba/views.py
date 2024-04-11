from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import django_paypal
from dotenv import load_dotenv
import os, json
load_dotenv()

@csrf_exempt
def orders(request):
    try:
        if request.method == 'POST':
            # Utiliza la información del carrito pasada desde el frontend para calcular los detalles de la orden
            cart = json.loads(request.body)['cart']
            response_data = django_paypal.create_order(cart)
            return JsonResponse(response_data["json_response"], status=response_data["http_status_code"])
    except Exception as e:
        print("Failed to create order:", e)
        return JsonResponse({"error": "Failed to create order."}, status=500)

@csrf_exempt
def capture(request, order_id):
    try:
        if request.method == 'POST':
            response_data = django_paypal.capture_order(order_id)
            return JsonResponse(response_data["json_response"], status=response_data["http_status_code"])
    except Exception as e:
        print("Failed to capture order:", e)
        return JsonResponse({"error": "Failed to capture order."}, status=500)


def checkout_page(request):
    client_id = os.getenv("CLIENT_ID")
    print(client_id)
    return render(request, 'checkout.html', {"client_id":client_id})

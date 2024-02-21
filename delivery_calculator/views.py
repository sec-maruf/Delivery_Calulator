from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .calculations import calculate_fee

@csrf_exempt
@require_http_methods(["POST"])
def delivery_fee(request):
    try:
        data = json.loads(request.body)
        cart_value = data.get('cart_value')
        delivery_distance = data.get('delivery_distance')
        number_of_items = data.get('number_of_items')
        time_str = data.get('time')
        
        # Check if all required fields are received and are of the correct type
        if not all([isinstance(cart_value, int), isinstance(delivery_distance, int),
                    isinstance(number_of_items, int), isinstance(time_str, str)]):
            return JsonResponse({'error': 'Invalid data types for one or more fields.'}, status=400)

        # Calculate the delivery fee using the utility function
        fee = calculate_fee(cart_value, delivery_distance, number_of_items, time_str)
        
        # Return the delivery fee as a JSON response
        return JsonResponse({'delivery_fee': fee})
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        return JsonResponse({'error': 'Invalid data provided: ' + str(e)}, status=400)


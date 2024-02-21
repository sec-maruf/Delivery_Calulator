
from datetime import datetime
from decimal import Decimal

def calculate_fee(cart_value, delivery_distance, number_of_items, order_time_str):
    """
    Calculate the delivery fee based on the cart value, delivery distance,
    number of items, and order time.
    """
    # Convert the order time from ISO 8601 string format to a datetime object
    order_time = datetime.fromisoformat(order_time_str)
    
    # Initialize the base delivery fee
    fee = Decimal('2.00')  # Base delivery fee is €2
    
    # If the cart value is less than €10, add a surcharge to make up the difference
    if cart_value < 1000:  # cart_value is in cents
        fee += (Decimal('1000') - Decimal(cart_value)) / 100

    # Add €1 for every additional 500 meters or part thereof beyond the first 1000 meters
    if delivery_distance > 1000:
        additional_distance = delivery_distance - 1000
        fee += (additional_distance + 499) // 500  # This ensures that we round up to the next 500 meters

    # If there are more than 4 items, add a 50 cent surcharge for each additional item
    if number_of_items > 4:
        fee += (number_of_items - 4) * Decimal('0.50')
    
    # If there are more than 12 items, add an additional "bulk" surcharge
    if number_of_items > 12:
        fee += Decimal('1.20')

    # Apply a surge of 1.2x during the Friday rush hour (3 PM to 7 PM UTC)
    if order_time.weekday() == 4 and 15 <= order_time.hour < 19:  # 4 is Friday in the weekday enumeration
        fee *= Decimal('1.2')

    # The delivery is free if the cart value is €200 or more
    if cart_value >= 20000:  # cart_value is in cents
        fee = Decimal('0.00')

    # Cap the delivery fee at €15
    fee = min(fee, Decimal('15.00'))

    # Return the fee converted to cents
    return int(fee * 100)


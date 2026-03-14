from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def regional_price(context, price):
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return f"₹{price}"
    
    region = getattr(request.user, 'region', 'IND')
    
    # Conversion rates (Base is INR)
    conversions = {
        'IND': ('₹', 1.0),
        'USA': ('$', 0.012),
        'UK': ('£', 0.0095),
        'EUR': ('€', 0.011),
    }
    
    symbol, rate = conversions.get(region, ('₹', 1.0))
    converted_price = float(price) * rate
    
    return f"{symbol}{converted_price:.2f}"

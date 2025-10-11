from django import template

register = template.Library()

@register.filter
def get_total_price(book):
    price = book.get_price(book.room)
    return price
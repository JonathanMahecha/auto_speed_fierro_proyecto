from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from .models import Purchase
from ventas.models import Sale_product
from servicios.models import Producto_requerido_servicio

@receiver(post_save, sender=Sale_product)
def update_inventory_on_sale(sender, instance, created, request=None,**kwargs):
    if created:  # Only proceed if the Sale instance is newly created
        product = instance.product
        quantity_sold = instance.quantity_sold
        if product.quantity >= quantity_sold:  # Ensure there's enough quantity in stock
            product.quantity -= quantity_sold
            product.save()
        else:
            # Handle case where there's not enough quantity in stock
            pass

@receiver(post_save, sender=Purchase)
def update_inventory_on_purchase(sender, instance, created, **kwargs):
    if created:  # Only proceed if the Sale instance is newly created
        product = instance.product
        quantity = instance.quantity
        if quantity > 0:  # Ensure there's enough quantity in stock
            product.quantity += quantity
            product.save()
        else:
            # Handle case where there's not enough quantity in stock
            # This can include raising an exception, logging a warning, etc.
            pass

@receiver(post_save, sender=Producto_requerido_servicio)
def update_inventory_on_Producto_requerido_servicio(sender, instance, created, **kwargs):
    if created:  # Only proceed if the Sale instance is newly created
        #if instance.change_stock == 'Sí':  # Check if change_stock is 'Sí'
            product = instance.product
            quantity_used = instance.quantity_used
            if product.quantity >= quantity_used:  # Ensure there's enough quantity in stock
                product.quantity -= quantity_used
                product.save()
            else:
                # Handle case where there's not enough quantity in stock
                # This can include raising an exception, logging a warning, etc.
                pass
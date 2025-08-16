from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models import F
from django.db.models.functions import Coalesce
from django.conf import settings
from .models import Order, OrderItem

@receiver(post_save, sender = Order)
def send_order_mail(sender, instance, created, **kwargs):
    if created:
        subject = f"Order # {instance.id} Confirmation"
        message = f"Hi {instance.name},\n\n Your Order Has been received and is being processed."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender = OrderItem)
def produt_total_sold_increment(sender, instance, created, **kwargs):
    if created:
        Product = instance.product.__class__
        product_pk = instance.product.pk
        quantity_sold = instance.quantity
        Product.objects.filter(pk=product_pk).update(
            total_sold=Coalesce(F('total_sold'), 0) + quantity_sold
        )
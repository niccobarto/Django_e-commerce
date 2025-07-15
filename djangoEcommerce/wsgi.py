"""
WSGI config for djangoEcommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoEcommerce.settings")

application = get_wsgi_application()

# --- ESECUZIONE UNA TANTUM SCRIPT FIX ORDERITEMS ---
if os.environ.get("RUN_FIX_ORDERITEMS") == "true":
    try:
        from order.models import OrderItem
        from django.db import connection

        # Assicura che il DB sia pronto
        if connection.introspection.table_names():
            updated = 0
            for item in OrderItem.objects.all():
                if item.product:
                    item.price = item.product.price
                    item.save()
                    updated += 1
            logging.warning(f"[FIX_ORDERITEMS] Corretto price in {updated} OrderItem.")
    except Exception as e:
        logging.error(f"[FIX_ORDERITEMS] ERRORE: {e}")

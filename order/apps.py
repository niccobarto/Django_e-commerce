from django.apps import AppConfig
import os
import logging

class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"

    def ready(self):
        # Controllo di sicurezza: esegui solo se è settata una variabile
        if os.environ.get("RUN_FIX_ORDERITEMS", "false") == "true":
            from order.models import OrderItem  # importa il modello dentro ready()
            updated = 0

            for item in OrderItem.objects.all():
                if item.product:
                    item.price = item.product.price
                    item.save()
                    updated += 1

            logging.warning(f"[FIX_ORDERITEMS] Aggiornati {updated} OrderItem.")

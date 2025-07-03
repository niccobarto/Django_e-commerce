from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):
    help = 'Crea i gruppi Customer e Manager con i permessi definiti'

    def handle(self, *args, **kwargs):
        # Recupera i content types
        User = apps.get_model('auth', 'User')
        GroupModel = apps.get_model('auth', 'Group')
        Address = apps.get_model('accounts', 'UserAddress')  # se esiste
        CartItem = apps.get_model('cart', 'CartItem')  # o cambia con app corretta
        Order = apps.get_model('order', 'Order')
        OrderItem = apps.get_model('order', 'OrderItem')
        Product = apps.get_model('store', 'Product')
        Category = apps.get_model('store', 'Category')

        # ======= CUSTOMER =======
        customer_group, _ = Group.objects.get_or_create(name='Customer')

        customer_perms = []

        # User
        customer_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(User),
            codename__in=['add_user', 'change_user', 'view_user']
        )

        # Address (se esiste)
        if Address:
            customer_perms += Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Address),
                codename__in=['add_address', 'change_address', 'view_address', 'delete_address']
            )

        # CartItem
        customer_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(CartItem),
            codename__in=['add_cartitem', 'change_cartitem', 'view_cartitem', 'delete_cartitem']
        )

        # Order
        customer_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Order),
            codename__in=['add_order', 'view_order']
        )

        # OrderItem
        customer_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(OrderItem),
            codename__in=['add_orderitem', 'view_orderitem']
        )

        # Product
        customer_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Product),
            codename__in=['view_product']
        )

        # Category
        customer_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Category),
            codename__in=['view_category']
        )

        customer_group.permissions.set(customer_perms)
        self.stdout.write(self.style.SUCCESS('Permessi assegnati al gruppo Customer'))

        # ======= MANAGER =======
        manager_group, _ = Group.objects.get_or_create(name='Manager')

        manager_perms = list(customer_perms)  # eredita i permessi da Customer

        # Gruppi (solo view e change)
        manager_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(GroupModel),
            codename__in=['change_group', 'view_group']
        )

        # Product - permessi aggiuntivi
        manager_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Product),
            codename__in=['add_product', 'change_product', 'delete_product']
        )

        # Category - permessi aggiuntivi
        manager_perms += Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Category),
            codename__in=['add_category', 'change_category', 'delete_category']
        )

        manager_group.permissions.set(manager_perms)
        self.stdout.write(self.style.SUCCESS('Permessi assegnati al gruppo Manager'))

        self.stdout.write(self.style.SUCCESS('✅ Gruppi e permessi inizializzati correttamente'))

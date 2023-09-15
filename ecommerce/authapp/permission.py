from django.contrib.auth.models import Permission

# Create custom permissions
Admin_group_permissions = [
    Permission.objects.get(codename='change_customuser'),
    Permission.objects.get(codename='view_customuser'),
    Permission.objects.get(codename='add_customuser'),
    Permission.objects.get(codename='delete_customuser'),

    Permission.objects.get(codename='change_product'),
    Permission.objects.get(codename='view_product'),
    Permission.objects.get(codename='add_product'),
    Permission.objects.get(codename='delete_product'),
    # Permission.objects.get(codename='can_view_users_list'),
    # Permission.objects.get(codename='can_view_users_list'),
    # Permission.objects.get(codename='can_view_users_list'),
    # Permission.objects.get(codename='can_view_users_list'),
    # Permission.objects.get(codename='can_view_users_list'),
    # Permission.objects.get(codename='can_view_users_list'),

]


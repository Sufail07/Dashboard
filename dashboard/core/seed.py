def seed_default_admin(**kwargs):
    from core.models import Role, User

    admin_role, _ = Role.objects.get_or_create(
        name="Admin",
        defaults={
            "can_view_dashboard": True,
            "can_create_dashboard": True,
            "can_edit_dashboard": True,
            "can_delete_dashboard": True,
            "can_view_record": True,
            "can_create_record": True,
            "can_edit_record": True,
            "can_delete_record": True,
            "can_view_summary": True,
            "can_access_insights": True,
        },
    )

    username = "admin"
    password = "admin123"
    first_name = "System"
    last_name = "Admin"

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=admin_role,
            is_active=True,
        )

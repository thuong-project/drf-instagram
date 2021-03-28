from rest_access_policy import AccessPolicy

from users.models import User


class PostAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create", "partial_update", "update", "destroy"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["(is_owner or in_admin_group)"]
        },
        {
            "action": ["retrieve", "list"],
            "principal": "authenticated",
            "effect": "allow",
        },
    ]

    def in_admin_group(self, request, view, action) -> bool:
        return request.user.groups.filter(name='admin').exists()

    def is_owner(self, request, view, action) -> bool:
        return request.user.id == int(view.kwargs['user_pk'])


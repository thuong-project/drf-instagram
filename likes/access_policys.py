from rest_access_policy import AccessPolicy

from users.models import User


class LikeAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create", "list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["destroy"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["(is_owner or in_admin_group)"]
        }
    ]

    def in_admin_group(self, request, view, action) -> bool:
        return request.user.groups.filter(name='admin').exists()

    def is_owner(self, request, view, action) -> bool:

        return view.get_object().user_id == request.user.id




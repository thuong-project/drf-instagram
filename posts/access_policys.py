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
            "action": ["retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["(has_user_pk or in_admin_group)"]
        },
    ]

    def in_admin_group(self, request, view, action) -> bool:
        return request.user.groups.filter(name='admin').exists()

    def is_owner(self, request, view, action) -> bool:
        if action == "create":
            if 'user_pk' in view.kwargs:
                return request.user.id == int(view.kwargs['user_pk'])
            else:
                return True
        else:
            return view.get_object().user_id == request.user.id

    def has_user_pk(self, request, view, action):
        if 'user_pk' in view.kwargs:
            return True
        else:
            return False
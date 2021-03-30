from rest_access_policy import AccessPolicy


class UserAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["retrieve", "me", "list"],
            "principal": "authenticated",
            "effect": "allow"
        },
        {

            "action": ["update", "partial_update", "destroy"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["(is_owner or in_admin_group)"]
        }
    ]

    def in_admin_group(self, request, view, action) -> bool:
        return request.user.groups.filter(name='admin').exists()

    def is_owner(self, request, view, action) -> bool:
        return view.get_object() == request.user

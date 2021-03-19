from rest_access_policy import AccessPolicy


class UserProfileAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["retrieve", "me"],
            "principal": "authenticated",
            "effect": "allow"
        },
        {

            "action": ["update", "partial_update", "destroy"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["(is_owner or in_admin_group)"]
        },
        {
            "action": ["list"],
            "principal": "group:admin",
            "effect": "allow",
        }
    ]

    def in_admin_group(self, request, view, action) -> bool:
        return request.user.groups.filter(name='admin').exists()

    def is_owner(self, request, view, action) -> bool:
        return view.get_object() == request.user

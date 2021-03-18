from rest_access_policy import AccessPolicy

NON_SAFE_METHODS = ["update", "partial_update", "destroy"]
SAFE_METHODS = ["create", "retrieve"]


class UserProfileAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": SAFE_METHODS,
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": NON_SAFE_METHODS,
            "principal": ["*"],
            "effect": "allow",
            "condition": "is_owner_or_in_admin_group"
        },
        {
            "action": ["list"],
            "principal": ["group:admin"],
            "effect": "allow"
        }
    ]

    def is_owner_or_in_admin_group(self, request, view, action) -> bool:
        return view.get_object() == request.user or request.user.groups.filter(name='admin').exists()

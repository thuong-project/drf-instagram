from rest_access_policy import AccessPolicy

from users.models import User


class CommentAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["has_commentable_pk"]
        },
        {
            "action": ["partial_update", "update", "destroy"],
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
            "condition": ["(has_commentable_pk or in_admin_group)"]
        },
    ]

    def in_admin_group(self, request, view, action) -> bool:
        return request.user.groups.filter(name='admin').exists()

    def is_owner(self, request, view, action) -> bool:

        return view.get_object().user_id == request.user.id

    def has_commentable_pk(self, request, view, action):
        if 'post_pk' in view.kwargs or 'comment_pk' in view.kwargs:
            return True
        else:
            return False



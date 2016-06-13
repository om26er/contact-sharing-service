from contact_share_service.models import User


class UserHelpers:
    def __init__(self, **kwargs):
        self.user = User.objects.get(**kwargs)

    def is_active(self):
        return self.user.is_active

    def is_admin(self):
        return self.user.is_admin

    def set_password_reset_key(self, key):
        self.user.password_reset_key = int(key)
        self.user.save()

    def get_password_reset_key(self):
        return self.user.password_reset_key

    def _reset_password_reset_key(self):
        self.user.password_reset_key = -1
        self.user.save()

    def is_password_reset_key_valid(self, key):
        return self.get_password_reset_key() == int(key)

    def change_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()
        self._reset_password_reset_key()

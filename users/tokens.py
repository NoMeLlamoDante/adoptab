from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.profile.email_confirmed)
        )


user_activation_token = UserActivationTokenGenerator()

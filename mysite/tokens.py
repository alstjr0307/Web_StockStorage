from django.contrib.auth.tokens import PasswordResetTokenGenerator
<<<<<<< HEAD

import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
=======
import six
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
>>>>>>> f64f7a8d0b9819a4a2822b323c99e833a7085ee2
        )

account_activation_token = AccountActivationTokenGenerator()
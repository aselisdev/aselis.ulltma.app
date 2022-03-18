from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from ulltma.models import Profile

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	"""docstring for AccountActivationTokenGenerator"""
	def _make_hash_value(self, user, timestamp):
		profile = Profile.objects.filter(user=user)[0]
		return(
			six.text_type(user.pk) + six.text_type(timestamp) + 
			six.text_type(profile.email_confirmed)
		)

account_activation_token = AccountActivationTokenGenerator()


# Include this line at the beginning of every script.
import environment

from crowdclass.models import UserSession

for user in UserSession.objects.all():
	print user.user
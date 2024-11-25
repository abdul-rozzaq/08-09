import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()



from django.contrib.auth import get_user_model
from project.models import Forum, Comment
from guardian.shortcuts import get_objects_for_user, get_perms, assign_perm


User=  get_user_model()


user = User.objects.get(pk=3)
forum = Forum.objects.get(pk=6)


for perm in get_perms(user, Forum):
    print(perm)
from django.contrib.auth import get_user_model

User = get_user_model()

random_ =User.objects.last()

#my_followers
random_.profiles.followers.all()

#who i follow
random_.is_following.all() # ==> random_.profile.following.all()
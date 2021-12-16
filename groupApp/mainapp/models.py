from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime    


class Hobby(models.Model):
    hobby = models.CharField(max_length=255)

    def __str__(self):
        return str(self.hobby)

    def to_dict(self):
        return {
            'hobby': self.hobby
        }

class User(AbstractUser):
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    city = models.CharField(max_length=255, blank=True)
    dob = models.DateField(default=datetime.now, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    friends = models.ManyToManyField("User", blank=True)

    def __str__(self):
        return str(self.username)

    def to_dict(self):
        hobbies = list(self.hobbies.values_list())
        friends = list(self.friends.values_list())
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'dob': self.dob,
            'image': self.image.url,
            'city': self.city,
            'hobbies': hobbies,
            'friends': friends
        }

class FriendRequest(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)
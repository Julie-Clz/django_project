from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class Hometeam(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_pics')

    def __str__(self):
        return self.name

class Match(models.Model):
    match_date = models.DateTimeField()
    goal_hometeam = models.PositiveIntegerField(blank=True, null=True)
    goal_awayteam = models.PositiveIntegerField(blank=True, null=True)
    done = models.BooleanField(default=False)
    winner = models.CharField(max_length=50, blank=True, null=True)
    hometeam = models.ForeignKey(Hometeam, on_delete=models.CASCADE, related_name='hometeam')

    def __str__(self):
        return  "{}: {}, done: {}".format(str(self.id), str(self.match_date.strftime('%d/%m/%Y %H:%M')), self.done)
   
    def get_absolute_url(self):
        return reverse('match-detail', kwargs={'pk': self.pk})


class Awayteam(models.Model):
    hometeam = models.ForeignKey(Hometeam, on_delete=models.CASCADE, related_name='awayteam')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match')

    def __str__(self):
        return "{} : {} - {}".format(str(self.match.match_date.strftime('%d/%m/%Y %H:%M')), self.match.hometeam.name, self.hometeam.name)

class Bet(models.Model):
    prono_hometeam = models.PositiveIntegerField(blank=True, null=True)
    prono_awayteam = models.PositiveIntegerField(blank=True, null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hometeam = models.ForeignKey(Hometeam, on_delete=models.CASCADE)
    awayteam = models.ForeignKey(Awayteam, on_delete=models.CASCADE)
    point = models.PositiveIntegerField(default=0)
    winner =models.CharField(max_length=100, blank=True, null=True)
    tab = models.BooleanField(default=False)
    
    def __str__(self):
        return "{}, {} : {} - {}".format(str(self.id), self.user.username, self.hometeam.name, self.awayteam.hometeam.name)

    # def get_absolute_url(self):
    #     return reverse('bet-detail', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('bet-update', kwargs={'pk': self.pk})


CROP_SETTINGS = {'size': (300, 300), 'crop': 'smart'}

class Userteam(models.Model):
    name = models.CharField(max_length=20, unique=True)
    image = ThumbnailerImageField(default='profile_pics/default.jpg', upload_to='userteam_pics', resize_source=CROP_SETTINGS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('userteam-detail', kwargs={'pk': self.pk})


class UserteamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member")
    userteam = models.ForeignKey(Userteam, on_delete=models.CASCADE, related_name="team")

    def __str__(self):
        return "{} : {}".format(self.user.username,self.userteam.name)

    def get_absolute_url(self):
        return reverse('userteam-quit', kwargs={'pk': self.pk})
        
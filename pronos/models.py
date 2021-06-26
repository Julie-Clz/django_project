from django.db import models
from django.contrib.auth.models import User


class Hometeam(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_pics')

    def __str__(self):
        return self.name

class Match(models.Model):
    match_date = models.DateTimeField()
    goal_hometeam = models.IntegerField()
    goal_awayteam = models.IntegerField()
    hometeam = models.ForeignKey(Hometeam, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id, self.hometeam.name

class Awayteam(models.Model):
    hometeam = models.ForeignKey(Hometeam, on_delete=models.CASCADE)
    match = models.OneToOneField(Match, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.hometeam.name

class Bet(models.Model):
    prono_hometeam = models.IntegerField()
    prono_awayteam = models.IntegerField()
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometeam = models.OneToOneField(Hometeam, on_delete=models.CASCADE)
    awayteam = models.OneToOneField(Awayteam, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user.name, self.id

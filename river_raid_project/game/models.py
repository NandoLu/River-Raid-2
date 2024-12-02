from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.player.name} - {self.score}"

from django.db import models
from django.utils import timezone

# Create your models here.


class Event(models.Model):
    TYPE_CHOICES = [
        ("UFC", "UFC"),
        ("Fight Night", "Fight Night"),
        # Add more types as needed
    ]

    location = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    link = models.CharField(max_length=500)
    event_id = models.CharField(max_length=64, unique=True)
    upcoming = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Fighter(models.Model):
    STANCE_CHOICES = [
        ("Orthodox", "Orthodox"),
        ("Southpaw", "Southpaw"),
        # Add more stances as needed
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=5, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    reach = models.CharField(max_length=20, blank=True, null=True)
    stance = models.CharField(
        max_length=20, choices=STANCE_CHOICES, blank=True, null=True
    )
    belt = models.BooleanField(default=False)
    win = models.IntegerField()
    loss = models.IntegerField()
    draw = models.IntegerField()
    link = models.CharField(max_length=500)
    fighter_id = models.CharField(max_length=64, unique=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "height": self.height,
            "weight": self.weight,
            "reach": self.reach,
            "stance": self.stance,
            "belt": self.belt,
            "win": self.win,
            "loss": self.loss,
            "draw": self.draw,
            "link": self.link,
            "fighter_id": self.fighter_id,
            "photo_url": self.photo_url,
        }


class Fight(models.Model):
    WIN_LOSE_CHOICES = [
        ("W", "Win"),
        ("L", "Loss"),
        ("NC", "No Contest"),
        ("DRAW", "Draw"),
        # Add more types as needed
    ]

    WEIGHT_CLASS_CHOICES = [
        ("Heavyweight", "Heavyweight"),
        ("Light Heavyweight", "Light Heavyweight"),
        ("Middleweight", "Middleweight"),
        ("Welterweight", "Welterweight"),
        ("Lightweight", "Lightweight"),
        ("Featherweight", "Featherweight"),
        ("Bantamweight", "Bantamweight"),
        ("Flyweight", "Flyweight"),
        ("Women's Featherweight", "Women's Featherweight"),
        ("Women's Bantamweight", "Women's Bantamweight"),
        ("Women's Flyweight", "Women's Flyweight"),
        ("Women's Strawweight", "Women's Strawweight")
        # Add more weight classes as needed
    ]

    METHOD_CHOICES = [
        ("U-DEC", "Unanimous Decision"),
        ("S-DEC", "Split Decision"),
        ("M-DEC", "Majority Decision"),
        ("KO/TKO", "Knockout/Technical Knockout"),
        ("CNC", "Could Not Continue"),
        ("SUB", "Submission"),
        ("Overturned", "Overturned"),
        ("DQ", "Disqualification"),
        # Add more methods as needed
    ]

    BONUS_CHOICES = [
        ("Fight", "Fight of the Night"),
        ("Perf", "Performance of the Night"),
        ("Sub", "Submission of the Night"),
        ("KO", "Knockout of the Night"),
        # Add more bonuses as needed
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fight_id = models.CharField(max_length=64, unique=True)
    link = models.CharField(max_length=500)
    fighter_one = models.ForeignKey(
        Fighter, on_delete=models.CASCADE, related_name="fighter1"
    )
    fighter_two = models.ForeignKey(
        Fighter, on_delete=models.CASCADE, related_name="fighter2"
    )
    wl_fighter_one = models.CharField(
        max_length=4, choices=WIN_LOSE_CHOICES, blank=True, null=True
    )
    wl_fighter_two = models.CharField(
        max_length=4, choices=WIN_LOSE_CHOICES, blank=True, null=True
    )
    weight_class = models.CharField(max_length=50, choices=WEIGHT_CLASS_CHOICES)
    belt = models.BooleanField(default=False)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    round = models.IntegerField()
    time = models.CharField(max_length=5)
    bonus = models.CharField(
        max_length=20, choices=BONUS_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.fighter_one} vs {self.fighter_two}"

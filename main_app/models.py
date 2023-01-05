from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

TIMESOFDAY = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)

class Dog(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dogs_detail", kwargs={"pk": self.id})
    

class Chewtoy(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    dogs = models.ManyToManyField(Dog)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"chewtoy_id": self.id})

    def clean_for_today(self):
        return self.cleaning_set.filter(date=date.today()).count()>=len(TIMESOFDAY)    
    
class Cleaning(models.Model):
    date = models.DateField('cleaning date')
    timeofday = models.CharField(max_length=1, choices=TIMESOFDAY, default=TIMESOFDAY[0][0])

    chewtoy = models.ForeignKey(Chewtoy, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_timeofday_display()} on {self.date}"

    class Meta:
        ordering = ['date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    chewtoy = models.ForeignKey(Chewtoy, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for chewtoy_id: {self.chewtoy_id} @{self.url}"
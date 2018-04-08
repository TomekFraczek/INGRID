from django.db import models

# Create your models here.


class Wetsuit(models.Model):

    genders = (("M", "Mens"),
               ("W", "Womens"),
               ("U", "Unisex"))
    sizes = ("XL", "L", "M", "S", "XS")

    rfid = models.CharField(max_length=10, unique=True)
    gender = models.CharField(choices=genders)
    size = models.CharField(choices=sizes)

    def __str__(self):
        return "{} {} wetsuit".format(self.size, self.gender)


class Locker(models.Model):

    locker_id = models.CharField(primary_key=True)
    wetsuit = models.ForeignKey(to=Wetsuit, on_delete=models.CASCADE)
    has_suit = models.BooleanField(default=True)



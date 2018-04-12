from django.db import models

# from .control import HangerSensor, Lock

# Create your models here.


class Wetsuit(models.Model):

    genders = (("M", "Mens"),
               ("W", "Womens"),
               ("U", "Unisex"))
    sizes = (("XXL", "XX Large"), ("XL", "Extra Large"), ("L", "Large"), ("M", "Medium"), ("S", "Small"))
    # TODO: include women's sizes, (even numbers 2-14)

    rfid = models.CharField(max_length=10, unique=True)
    gender = models.CharField(choices=genders, max_length=1)
    size = models.CharField(choices=sizes, max_length=4)
    img_path = models.FilePathField(default='ingrid/placeholder_wetsuit.jpg')

    def __str__(self):
        return "{} {} wetsuit".format(self.size, self.gender)

    @property
    def description(self):
        return str(self)


class Locker(models.Model):

    locker_id = models.IntegerField(primary_key=True)
    wetsuit = models.OneToOneField(to=Wetsuit, on_delete=models.CASCADE)

    #: Field to keep track of the expected value of has_suit
    should_have_suit = models.BooleanField(default=True)

    # lock = Lock(locker_id)
    # hanger_sensor = HangerSensor(locker_id)

    #@property
    #def has_suit(self):
    #    return self.hanger_sensor.is_active

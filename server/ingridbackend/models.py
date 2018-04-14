from django.db import models

from .control import HangerSensor, Lock


class Wetsuit(models.Model):

    genders = (("M", "Mens"),
               ("W", "Womens"),
               ("U", "Unisex"))
    sizes = (("XXL", "XX Large"), ("XL", "Extra Large"), ("L", "Large"), ("M", "Medium"), ("S", "Small"))
    # TODO: include women's sizes, (even numbers 2-14)

    rfid = models.CharField(max_length=10, unique=True)
    gender = models.CharField(choices=genders, max_length=1)
    size = models.CharField(choices=sizes, max_length=4)
    img_path = models.FilePathField(default='ingridbackend/placeholder_wetsuit.jpg')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {} wetsuit ({})".format(self.get_gender_display(), self.size, self.date_added)

    @property
    def description(self):
        return "{} {} wetsuit".format(self.get_gender_display(), self.size)


class Locker(models.Model):

    locker_id = models.IntegerField(primary_key=True)
    wetsuit = models.OneToOneField(to=Wetsuit, on_delete=models.CASCADE)

    #: Field to keep track of the expected value of has_suit
    should_have_suit = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        self.lock = Lock(self.locker_id)
        self.hanger_sensor = HangerSensor(self.locker_id)
        super(Locker, self).__init__(*args, **kwargs)


    def get_locker_int(self):
        """Method to allow django to handle the field -> int conversion"""
        return getattr(self, "locker_id")

    def get_lock(self):
        return self.lock

    def get_hanger_sensor(self):
        return self.hanger_sensor

    @property
    def has_suit(self):
        return self.hanger_sensor.is_active

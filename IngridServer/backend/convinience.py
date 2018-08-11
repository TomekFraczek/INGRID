from .models import Wetsuit


def is_model_rfid(rfid, model_class):
    try:
        model_class.objects.get(rfid=rfid)
    except model_class.DoesNotExist:
        return False
    else:
        return True


def is_wetsuit_rfid(rfid):
    is_model_rfid(rfid, Wetsuit)


def is_member_rfid(rfid):
    # TODO: Make this actually do a check
    return True

from .models import Result
from utils.custom_exceptions import *

'''
Operation of Entity Result
'''


def get_result_by(raise_exception=True, with_deleted=False, **kwargs):
    if with_deleted:
        result = Result.objects.all_with_deleted().filter(**kwargs).first()
    else:
        result = Result.objects.all().filter(**kwargs).first()
    if not result and raise_exception:
        raise ObjectNotFound
    return result

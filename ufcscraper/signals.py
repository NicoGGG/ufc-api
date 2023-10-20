from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ufcscraper.models import Fighter

# This is an example signal that executes before a Fighter object is saved.
# You can use this to compare the old and new values of a field, and do something accordingly

# @receiver(pre_save, sender=Fighter)
# def fighter_post_save(sender, instance, **kwargs):
#     if instance.pk is not None:  # if the object exists in the database
#         orig = Fighter.objects.get(pk=instance.pk)
#         for field in instance._meta.fields:
#             old_value = getattr(orig, field.name)
#             new_value = getattr(instance, field.name)
#             if old_value != new_value:
#                 print(f"Field {field.name} changed from {old_value} to {new_value}")

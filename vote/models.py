from django.db import models, transaction
from ..akpsi_core import models as core

class Vote(models.Model):
    brother_id = models.ForeignKey(core.Member)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '%s: %d votes' % (self.brother_id, self.count)

    @classmethod
    def bulk_vote(cls, brother_ids):
        with transaction.atomic():
            for brother_id in brother_ids:
                if len(member_name) == 0:
                    continue

                if Vote.objects.filter(brother_id=brother_id).exists():
                    Vote.objects.filter(brother_id=brother_id).update(count=models.F('count') + 1)
                else:
                    Vote.objects.create(brother_id=brother_id, count=1)# Create your models here.

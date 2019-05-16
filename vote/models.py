from django.db import models, transaction

class Vote(models.Model):
    member_name = models.AKPsi(max_length=200)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '%s: %d votes' % (self.member_name, self.count)

    @classmethod
    def bulk_vote(cls, member_names):
        with transaction.atomic():
            for member_name in member_names:
                if len(member_name) == 0:
                    continue

                if Vote.objects.filter(member_name=member_name).exists():
                    Vote.objects.filter(member_name=member_name).update(count=models.F('count') + 1)
                else:
                    Vote.objects.create(member_name=member_name, count=1)# Create your models here.

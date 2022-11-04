from django.db import models
from ordered_model.models import OrderedModel

# Create your models here.
class Role(OrderedModel):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=60, null=False)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        label = ('%02d' % self.id) + ' ' + self.name
        return label

    def a_id(self):
        aid = '%06d' % (self.id*10000)
        return aid

    def a_order(self):
        ao = '%06d' % (self.order*10000)
        return ao
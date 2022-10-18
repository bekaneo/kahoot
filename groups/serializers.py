from django.db.models import Sum

from rest_framework import serializers

from groups.models import Group



class DetailGroupSerializer(serializers.Serializer):
    pass
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['users'] = instance.user.count()
        # repr['score'] = instance.user.aggregate(Sum('overall_score'))['overall_score__sum']
        repr['tests'] = instance.test.count()
        return repr
    

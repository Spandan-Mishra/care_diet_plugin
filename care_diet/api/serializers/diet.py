from rest_framework import serializers
from care_diet.models.diet import Diet

class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'

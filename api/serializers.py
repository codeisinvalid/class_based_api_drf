from rest_framework import serializers
from .models import Student
import re


# Validators
def start_with_s(value):
    if value[0].lower() != 's':
        raise serializers.ValidationError('Name should start with "S"')


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100, validators = [start_with_s])
    roll = serializers.IntegerField()
    grade = serializers.CharField(max_length = 100)
    city = serializers.CharField(max_length = 100)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.roll = validated_data.get('roll', instance.roll)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance
    
    def validate_roll(self, value):
        if value>=200:
            raise serializers.ValidationError("Seats Full. No admissions available currently.")
        return value
    
    def validate_name(self, value):
        pattern = r'^[a-zA-Z\s]+$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Name must only contain alpnabets or space")
        return value
        

    def validate(self, data):
        nm = data['name']
        ct = data['city']
        if nm.lower() == 'sujan' and ct.lower() != 'pokhara':
            raise serializers.ValidationError("The city must be Pokhara")
        return data
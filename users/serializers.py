from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User, Patients, Payments


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'confirm_password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super(SignUpSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if username and User.objects.filter(username=username).exists():
            raise ValidationError({'success': False, 'message': 'Username already exists'})

        if password != confirm_password:
            raise ValidationError({'success': False, 'message': 'Passwords do not match'})

        if len(password) < 8:
            raise ValidationError({'success': False, 'message': 'Password is minimum length 8 characters'})

        return data

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'created_at', 'updated_at')

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class PatientsSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)
    class Meta:
        model = Patients
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'address',
            'phone',
            'rengen_number',
            'patient_history',
            'payments',
        ]
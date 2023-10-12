from rest_framework import serializers
from customer.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "date_of_birth",
            "profile_picture",
            "aadhar_card_file",
            "pan_card_file",
        ]

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive")
        data["user"] = {
            "id": user.id,
            "name": f"{user.first_name} {user.last_name}",
            "role": user.role.name
        }
        return data
    

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    throttle_scope = "login"

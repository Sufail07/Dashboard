from rest_framework import serializers

from core.models import FinancialRecord, Role, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["created_at", "modified_at"]
        
        
        
class FinancialRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = "__all__"
        read_only_fields = ["created_at", "modified_at"]
        

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["created_at", "modified_at"]

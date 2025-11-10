from decimal import Decimal
from rest_framework import serializers
class TransferSerializer(serializers.Serializer):
    to_account_number = serializers.CharField(min_length=10, max_length=10)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2,
                                      min_value=Decimal("0.01"))

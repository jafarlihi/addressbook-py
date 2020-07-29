from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'user', 'name', 'value')


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = ('id', 'user', 'name', 'contacts')

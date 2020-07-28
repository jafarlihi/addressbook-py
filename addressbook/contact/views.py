from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

import jwt

from .serializers import ContactSerializer
from .models import Contact


class ContactView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        authorization = request.headers.get('Authorization')
        token = authorization.split()[1]
        tokenDecoded = jwt.decode(token, verify=False)
        queryset = Contact.objects.filter(user__id=tokenDecoded["user_id"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

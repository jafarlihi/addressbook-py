from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import jwt

from .serializers import ContactSerializer
from .models import Contact
from .decorators import parse_token_user_id


class ContactView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @parse_token_user_id
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id != kwargs['user_id']:
            raise PermissionDenied
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @parse_token_user_id
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user.id != kwargs['user_id']:
            raise PermissionDenied
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @parse_token_user_id
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id != kwargs['user_id']:
            raise PermissionDenied
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @parse_token_user_id
    def list(self, request, *args, **kwargs):
        queryset = Contact.objects.filter(user__id=kwargs['user_id'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @parse_token_user_id
    def create(self, request, *args, **kwargs):
        request.data["user"] = kwargs['user_id']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

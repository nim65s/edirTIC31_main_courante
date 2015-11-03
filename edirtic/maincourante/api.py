from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.http import Http404

from tastypie.resources import ModelResource, Resource
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie import fields

import json

from .models import *


__all__ = ['IndicatifResource', 'MessageResource', 'EvenementResource']


class BaseAuthentication(Authentication):
    """
    On redéfinie la vérification de l’authentification,
    mais sans vérifier les CSRF.
    À virer si un token CSRF peut être récupéré coté js.
    """

    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()


class EvenementResource(ModelResource):

    class Meta:
        resource_name = 'evenement'
        queryset = Evenement.objects.all()
        allowed_methods = ['get']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()

class Message:

    def __init__(self, thread):
        self.pk = thread.pk
        self.evenement = thread.evenement
        self.sender = thread.expediteur.nom
        self.receiver = thread.recipiendaire.nom
        last_version = thread.get_last_version()
        self.body = last_version.corps
        self.timestamp = last_version.cree

class MessageResource(Resource):

    evenement = fields.ToOneField(EvenementResource, 'evenement')
    sender = fields.CharField(attribute='sender')
    receiver = fields.CharField(attribute='receiver')
    body = fields.CharField(attribute='body')
    timestamp = fields.DateTimeField(attribute='timestamp')

    class Meta:
        resource_name = 'message'
        collection_name = 'messages'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()

    def detail_uri_kwargs(self, bundle):
        return {
            'pk': bundle.obj.pk,
        }

    def get_object_list(self, request):

        threads = MessageThread.objects.all()
        messages = [Message(thread) for thread in threads]

        return messages

    def obj_get_list(self, bundle, **kwargs):

        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):

        try:
            pk = int(kwargs['pk'])
        except ValueError:
            raise Http404
        thread = get_object_or_404(MessageThread, pk=pk)
        message = Message(thread)

        return message

    def obj_create(self, bundle, **kwargs):

        try:
            evenement = bundle.data['evenement']
            sender = bundle.data['sender']
            receiver = bundle.data['receiver']
            body = bundle.data['body']
        except KeyError:
            raise ImmediateHttpResponse(response=HttpBadRequest())

        evenement = get_object_or_404(Evenement, slug=evenement)

        try:
            sender = Indicatif.objects.get(nom=sender)
        except Indicatif.DoesNotExist:
            sender = Indicatif(evenement=evenement, nom=sender)
            sender.save()
        try:
            receiver = Indicatif.objects.get(nom=receiver)
        except Indicatif.DoesNotExist:
            receiver = Indicatif(evenement=evenement, nom=receiver)
            receiver.save()

        thread = MessageThread(evenement=evenement,
                expediteur=sender, recipiendaire=receiver)
        thread.save()

        user = bundle.request.user
        event = MessageEvent(thread=thread,
                operateur=user, corps=body)
        event.save()

        bundle.obj = Message(thread)

        return bundle

    def obj_update(self, bundle, **kwargs):

        try:
            pk = int(kwargs['pk'])
        except ValueError:
            raise Http404
        thread = get_object_or_404(MessageThread, pk=pk)

        last_version = thread.get_last_version()

        body = bundle.data.get('body')
        if body and body != last_version.corps and not thread.deleted:
            user = bundle.request.user
            event = MessageEvent(thread=thread,
                    operateur=user, corps=body,
                    type=MessageEvent.TYPE.modification.value)
            event.save()

        bundle.obj = Message(thread)

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        pass

    def obj_delete(self, bundle, **kwargs):

        try:
            pk = int(kwargs['pk'])
        except ValueError:
            raise Http404
        thread = get_object_or_404(MessageThread, pk=pk)

        try:
            reason = bundle.request.GET['reason']
        except KeyError:
            raise ImmediateHttpResponse(response=HttpBadRequest())

        if not thread.deleted:
            user = bundle.request.user
            event = MessageEvent(thread=thread,
                    operateur=user, corps=reason,
                    type=MessageEvent.TYPE.suppression.value)
            event.save()

    def rollbacks(self, bundles):
        pass


class IndicatifResource(ModelResource):

    class Meta:
        queryset = Indicatif.objects.all()
        allowed_methods = ['get']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()

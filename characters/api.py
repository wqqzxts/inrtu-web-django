from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from characters.models import Team, Position, Skills, Content, ContentType, Character
from characters.serializers import TeamSerializer, PositionSerializer, SkillsSerializer, ContentSerializer, ContentTypeSerializer, CharacterSerializer

class TeamViewset(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PositionViewset(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class SkillsViewset(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer

class ContentTypeViewset(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

class ContentViewset(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class CharactersViewset(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
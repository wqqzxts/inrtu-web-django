from rest_framework import serializers

from characters.models import Team, Position, Skills, Content, ContentType, Character

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"

class ContentSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Content
        fields = "__all__"

class CharacterSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    # def create(self, validated_data): 
    #     # когда в api создается сериалайзер, 
    #     # то заполняется специальное поле сериалайзера которое называется context
    #     # в него добавляется инфомрация по запросе, и доступна эта инфа
    #     # через self.context['request'], в частности там есть информация о пользовате
    #     if 'request' in self.context:
    #         # заполняем validated_data который используется для создания сущности в БД
    #         # данными из запроса
    #         validated_data['user'] = self.context['request'].user
            
    #     return super().create(validated_data)

    class Meta:
        model = Character
        fields = "__all__"
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        request = self.context["request"]
        usr = request.user
        if request.method == "POST":
            open_count = Advertisement.objects.filter(creator=usr, status="OPEN").count()
            if open_count >= 10:
                raise serializers.ValidationError(f'У пользователя "{usr}" не может быть более 10 открытых обьявлений')
        elif request.method in {"PUT", "PATCH"}:
            id = self.instance.id
            open_count = Advertisement.objects.filter(creator=usr, status="OPEN").filter(~Q(id=id)).count()
            if open_count >= 10 and data.get("status") == "OPEN":
                raise serializers.ValidationError(f'У пользователя "{usr}" не может быть более 10 открытых обьявлений')

        return data

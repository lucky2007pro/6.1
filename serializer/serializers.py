from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Ism kamida 3 ta belgidan iborat bo'lishi kerak!")
        return value

    def validate_tel(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Telefon faqat raqamlardan iborat bo'lishi kerak!")

        qs = User.objects.filter(tel=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Bu telefon raqamda mavjud!")

        return value

    def validate_card(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Karta faqat raqamlardan iborat bo'lishi kerak!")

        if len(value) != 16:
            raise serializers.ValidationError("Karta raqami 16 ta bo'lishi kerak!")

        qs = User.objects.filter(card=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Bu karta raqamda mavjud!")

        return value

    def validate_yosh(self, value):
        if value < 18:
            raise serializers.ValidationError("Yosh 18 dan katta yoki teng bo'lishi kerak!")

        if value > 100:
            raise serializers.ValidationError("Yaroqli yosh kiriting.")

        return value

    def validate(self, attrs):
        name = attrs.get('name', getattr(self.instance, 'name', None))
        tel = attrs.get('tel', getattr(self.instance, 'tel', None))

        if name and tel and name == tel:
            raise serializers.ValidationError("Name va telefon bir xil bo'lishi mumkin emas!")

        return attrs

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.card = validated_data.get('card', instance.card)
        instance.yosh = validated_data.get('yosh', instance.yosh)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['card'] = f"**** **** **** {data['card'][-4:]}"
        return data

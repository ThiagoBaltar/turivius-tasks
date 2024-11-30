from rest_framework import serializers

from .models import UserTask


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ('uuid', 'title', 'description', 'finished')
        read_only_fields = ('uuid', 'finished')


class FinishUserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ('uuid', 'title', 'description', 'finished')
        read_only_fields = ('uuid', 'title', 'description', 'finished')

    def update(self, instance: UserTask, validated_data):
        instance.finished = True
        instance.save()

        return instance


class ResumeUserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ('uuid', 'title', 'description', 'finished')
        read_only_fields = ('uuid', 'title', 'description', 'finished')

    def update(self, instance: UserTask, validated_data):
        instance.finished = False
        instance.save()

        return instance

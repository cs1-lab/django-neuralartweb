from rest_framework import serializers
from neuralartcms.models import Material, Result

import json

class MaterialDetailSerializer(serializers.ModelSerializer):
    """
    Materialのが画像などを取得する
    """
    id = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()

    #content_image = serializers.SerializerMethodField()
    #content_segmap = serializers.SerializerMethodField()
    #style_image = serializers.SerializerMethodField()
    #style_segmap = serializers.SerializerMethodField()

    parameters = serializers.SerializerMethodField()
    start_at = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = ('id', 'material_name',
                  'content_image', 'content_segmap', 'style_image', 'style_segmap',
                  'parameters', 'start_at')

    def get_id(self, instance):
        return instance.id

    def get_material_name(self, instance):
        return instance.material_name

    def get_content_image(self, instance):
        return instance.content_image.url

    def get_content_segmap(self, instance):
        return instance.content_segmap.url

    def get_style_image(self, instance):
        return instance.style_image.url

    def get_style_segmap(self, instance):
        return instance.style_segmap.url

    def get_parameters(self, instance):
        return json.loads(instance.parameters)

    def get_start_at(self, instance):
        return instance.start_at


class ResultSetSerializer(serializers.ModelSerializer):
    """
    resultを登録するためのserializer
    """
    class Meta:
        model = Result
        fields = ("result_image", 'iteration', 'result_info',)

    def create(self, validated_data):
        """
        保存
        :param validated_data:
        :return:
        """
        material = self.context["material"]
        result = Result(
            material=material,
            iteration=validated_data["iteration"],
            result_image=validated_data["result_image"],
            result_info=validated_data["result_info"],
        )
        result.save()
        return result

    def validate(self, attrs):
        """
        全体のバリデーション
        :param attrs:
        :return:
        """
        material = self.context.get('material')

        if material is False:
            raise serializers.ValidationError("Material does not exit.")

        return attrs

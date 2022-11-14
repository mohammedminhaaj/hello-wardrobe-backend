from rest_framework import serializers
from product.models import Product, PrimaryCategory, SecondaryCategory, Size, Tag


class PrimaryCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return 'primary'

    class Meta:
        model = PrimaryCategory
        fields = ['id', 'name', 'category']


class SecondaryCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return 'secondary'

    class Meta:
        model = SecondaryCategory
        fields = ['id', 'name', 'category']


class SizeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return 'size'

    class Meta:
        model = Size
        fields = ['id', 'name', 'category']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'category']


class ProductSerializer(serializers.ModelSerializer):

    # primary_category = PrimaryCategorySerializer()
    # secondary_category = SecondaryCategorySerializer()
    # size = SizeSerializer(read_only=True, many=True)
    # tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

from rest_framework import serializers
from product.models import Product, PrimaryCategory, SecondaryCategory, Size, Tag


class PrimaryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryCategory
        fields = ['name']


class SecondaryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryCategory
        fields = ['name']


class SizeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return 'size'

    class Meta:
        model = Size
        fields = ['id', 'name','category']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'category']


class ProductSerializer(serializers.ModelSerializer):

    primary_category = PrimaryCategorySerializer()
    secondary_category = SecondaryCategorySerializer()
    size = SizeSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'primary_category',
                  'secondary_category', 'size', 'tags']

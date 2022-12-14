from rest_framework import serializers
from product.models import Product, PrimaryCategory, SecondaryCategory, Size, Tag, TagMaster


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
        return {'name':'size'}

    class Meta:
        model = Size
        fields = ['id', 'name', 'category']


class TagMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagMaster
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    category = TagMasterSerializer()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'category']

class FilterSerializer(serializers.Serializer):
    primary_category_details = PrimaryCategorySerializer(many = True)
    secondary_category_details = SecondaryCategorySerializer(many = True)
    size_details = SizeSerializer(many = True)
    filter_labels = TagMasterSerializer(many = True)
    filter_details = TagSerializer(many = True)

class ProductListSerializer(serializers.ModelSerializer):

    # primary_category = PrimaryCategorySerializer()
    # secondary_category = SecondaryCategorySerializer()
    # size = SizeSerializer(read_only=True, many=True)
    # tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'url_name']


class ProductOverviewSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = ['primary_category', 'secondary_category',
                   'tags', 'created_on', 'updated_on']

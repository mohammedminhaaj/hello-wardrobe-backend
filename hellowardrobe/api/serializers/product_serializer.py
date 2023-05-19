from rest_framework import serializers
from product.models import Product, PrimaryCategory, SecondaryCategory, Size, Tag, TagMaster, SortMenu


class PrimaryCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return 'primary'

    class Meta:
        model = PrimaryCategory
        fields = ['id', 'display_name', 'category']


class SecondaryCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return 'secondary'

    class Meta:
        model = SecondaryCategory
        fields = ['id', 'display_name', 'category']


class SizeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return {'display_name':'size'}

    class Meta:
        model = Size
        fields = ['id', 'display_name', 'category']

class SortMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortMenu
        fields = ['id', 'display_name', 'field_name']


class TagMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagMaster
        fields = ['id', 'display_name']


class TagSerializer(serializers.ModelSerializer):
    category = TagMasterSerializer()

    class Meta:
        model = Tag
        fields = ['id', 'display_name', 'category']

class FilterSerializer(serializers.Serializer):
    primary_category_details = PrimaryCategorySerializer(many = True)
    secondary_category_details = SecondaryCategorySerializer(many = True)
    size_details = SizeSerializer(many = True)
    filter_labels = TagMasterSerializer(many = True)
    filter_details = TagSerializer(many = True)
    sort_menu = SortMenuSerializer(many = True)

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'url_name']


class ProductOverviewSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = ['primary_category', 'secondary_category',
                   'tags', 'created_at', 'created_by', "modified_at", "modified_by", "deleted_by"]

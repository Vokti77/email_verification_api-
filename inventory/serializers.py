from rest_framework import serializers
from .models import Category, Sub_Category, Clothe

class Sub_CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Sub_Category 
        fields = ('id', 'name', 'category', 'category_name', 'create_at', 'update_at')


class CategotySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'
        

class ClotheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothe
        fields = '__all__'


class ClothesSerializer(serializers.Serializer):
    # category_name = serializers.ReadOnlyField(source='category.category_name')
    # sub_category_name = serializers.ReadOnlyField(source='sub_category.sub_category_name')
    category_name = serializers.ReadOnlyField(source='category.name')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    
    image1 = serializers.ListField(child=serializers.FileField())
    image2 = serializers.ListField(child=serializers.FileField(), required=False)
    image3 = serializers.ListField(child=serializers.FileField(), required=False)

    class Meta:
        model = Clothe
        fields = '__all__'


class ClothesDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothe
        fields = '__all__'


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class SubCategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Category
        fields = ('id', 'name')
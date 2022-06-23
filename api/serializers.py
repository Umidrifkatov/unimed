from pyexpat import model
from rest_framework import serializers
from core.models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(source='manufacturer.name')
    category_name = serializers.CharField(source='category.name')
    parent_category = serializers.CharField(source='category.parent.name')
    img_url = serializers.SerializerMethodField('get_image_url')
    
    def get_image_url(self , instance):
        return ProductImage.objects.filter(belongs_to=instance).values_list('image_file',flat=True)

    class Meta:
        model = Product
        fields = ['img_url', 'name', 'name_search', 'manufacturer_name', 
                'category_name', 'parent_category','short_description',
                'long_description', 'technical_details', 'standard_of_equipment',
                'commercial_proposal_file', 'is_used','brochure', ]
    
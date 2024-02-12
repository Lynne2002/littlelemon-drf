from rest_framework import serializers
from .models import MenuItem
from .models import Category
from decimal import Decimal

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory']

""" class MenuItemsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=255, decimal_places=2)
    inventory = serializers.IntegerField() """

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id', 'slug','title']
        
# Easier way:
class MenuItemsSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.StringRelatedField()
    # More efficient:
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
     
     # OPTION 1: Validation of price field
    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    stock = serializers.IntegerField(source='inventory')

    # OPTION 3: Using validate_field() method
    def validate_price(self,value):
        if(value < 2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        
    def validate_stock(self, value):
        if(value < 0):
            raise serializers.ValidationError("Stock cannot be negative") 
    
    # OPTION 4: Using the validate() method
    """ def validate(self, attrs):
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.00')
        if(attrs['stock']<0):
            raise serializers.ValidationError('Stock cannot be a negative value')
        return super().validate(attrs) """

    # HYPERLINK RELATED FIELD
    """ category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category-detail'
    ) """
    class Meta:
        model = MenuItem
        fields =['id', 'title', 'price', 'stock','price_after_tax', 'category', 'category_id']
        # OR to display categories
        #depth = 1

        # OPTION 2 - validation of price field
        """ extra_kwargs = {
        'price': {'min_value': 2},
        'stock':{'source':'inventory', 'min_value': 0}
         } """
       


    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)

# Alt for HyperlinksSerializer
class MenuHyperItemsSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    class Meta:
        model = MenuItem
        fields =['id', 'title', 'price', 'stock','price_after_tax', 'category']
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)

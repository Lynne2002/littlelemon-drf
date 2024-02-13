from rest_framework import generics
from .models import MenuItem
from .models import Category
from .serializers import MenuItemSerializer, MenuItemsSerializer, CategorySerializer, MenuHyperItemsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

# TemplateHTMLRenderer & StaticHTMLRenderer
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes

# YAML Renderer
from rest_framework_yaml.renderers import YAMLRenderer

# CSV Renderer
from rest_framework_csv.renderers import CSVRenderer

# Pagination
from django.core.paginator import Paginator, EmptyPage

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer

@api_view()
def menu_items(request):
    items = MenuItem.objects.select_related('category').all()
    # add context for hyperlinks display
    serialized_item = MenuHyperItemsSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)

@api_view()
def single_item(request,id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemsSerializer(item)
    return Response(serialized_item.data)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#Hyperlink Related field
@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

# DESERIALIZATION
@api_view(['GET', 'POST'])
def menu_items_des(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        # Filtering menu items
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')

        # Search menu items
        search = request.query_params.get('search')

        # Order menu items
        ordering = request.query_params.get('ordering')

        # Pagination
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

# Use 2 underscores -> linked to category model and linked to menu model
        if category_name:
            items = items.filter(category__title=category_name)
        # if price = to_price -> equal price
        if to_price:
            items = items.filter(price__lte=to_price)#lte means price is less than or equal to a value
         
         # Starts with 
        """  if search:
            items = items.filter(title__startswith=search) """
        
         # Starts with - case insensitive
        """  if search:
            items = items.filter(title__istartswith=search) """

        # Present anywhere in title
        """ if search:
            items = items.filter(title__contains=search) """
        
         # Present anywhere in title -case insensitive
        if search:
            items = items.filter(title__icontains=search)
        
        # Ordering by price only
        """ if ordering:
            items = items.order_by(ordering) """
        
        # Ordering by price then inventory
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        
        # Pagination
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items =[]


        serialized_item =MenuItemsSerializer(items, many=True)
        return Response(serialized_item.data)
    
    elif request.method == 'POST':
        serialized_item = MenuItemsSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    

# TemplateHTMLRenderer
@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemsSerializer(items, many=True)
    return Response({'data': serialized_item.data}, template_name='menu-item.html')

# StaticHTMLRenderer
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome to LittleLemon API Project</h1></body></html>'
    return Response(data)

# CSVRenderer
@api_view()
@renderer_classes([CSVRenderer])
def menu_items_csv(request):
    items = MenuItem.objects.select_related('category').all()
    # add context for hyperlinks display
    serialized_item = MenuHyperItemsSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)

# YAMLRenderer
@api_view()
@renderer_classes([YAMLRenderer])
def menu_items_yaml(request):
    items = MenuItem.objects.select_related('category').all()
    # add context for hyperlinks display
    serialized_item = MenuHyperItemsSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)
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

# CSV Renderer
from rest_framework_csv.renderers import CSVRenderer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

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
        serialized_item = MenuItemsSerializer(items, many=True)
        return Response(serialized_item.data)
    
    if request.method == 'POST':
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

#CSVRenderer
@api_view()
@renderer_classes([CSVRenderer])
def menu_items_csv(request):
    items = MenuItem.objects.select_related('category').all()
    # add context for hyperlinks display
    serialized_item = MenuHyperItemsSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)
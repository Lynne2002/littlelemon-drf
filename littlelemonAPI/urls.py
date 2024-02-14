from django.urls import path
from . import views

urlpatterns =[
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu', views.menu_items),
    path('menu/<int:id>', views.single_item),
    path('categories', views.CategoriesView.as_view()),
    # For hyperlink display
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('menu-items-des/', views.menu_items_des),
    path('menuhtml', views.menu),
    path('welcome', views.welcome),
    path('menu-items-csv', views.menu_items_csv),
    path('menu-items-yaml', views.menu_items_yaml),
    #Viewsets
    path('menu-items-view', views.MenuItemsViewSet.as_view({'get': 'list'})),
    path('menu-items-view/<int:pk>', views.MenuItemsViewSet.as_view({'get': 'retrieve'})),
]
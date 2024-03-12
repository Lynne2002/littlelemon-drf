from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

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
    path('secret/', views.secret),
    #generating tokens
    path('api-token-auth/', obtain_auth_token),
    # Manager view
    path('manager-view/',views.manager_view),
    # Throttle check
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
    path('menu-items-throttle', views.MenuItemsViewSetThrottle.as_view({'get': 'list'})),
    path('menu-items-throttle/<int:pk>', views.MenuItemsViewSetThrottle.as_view({'get':'retrieve'})),

    path('groups/manager/users', views.managers)
]
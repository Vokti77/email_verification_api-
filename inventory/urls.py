
from django.urls import path
from .views import CategoryListCreateView, ClothesDetailView, ClothesListView, CategoryRetrieveUpdateDeleteView, SubCategoryListCreateView, SubCategoryRetrieveUpdateDeleteView, ClothesViewAPI, ClotheCountPerCategory, ClotheCountPerSubCategory, ClotheCreateView

urlpatterns = [
    # path('output/', views.output, name='output'),
    path('categories', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>', CategoryRetrieveUpdateDeleteView.as_view(), name='category-detail'),
    path('subcategories', SubCategoryListCreateView.as_view(), name='subcategory-list-create'),
    path('subcategories/<int:pk>', SubCategoryRetrieveUpdateDeleteView.as_view(), name='subcategory-detail'),
    path('clothes/', ClothesViewAPI.as_view(), name='clothes'),
    path('clothes_list', ClothesListView.as_view(), name='clothes-list'),
    path('clothe/<int:pk>', ClothesDetailView.as_view(), name='clothes-detail'),
    path('clothe-count-per-category/', ClotheCountPerCategory.as_view(), name='clothe-count-per-category'),
    path('clothe-count-per-subcategory/', ClotheCountPerSubCategory.as_view(), name='clothe-count-per-subcategory'),
    path('create/', ClotheCreateView.as_view(), name='clothe-create'),
 
]
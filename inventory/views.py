from rest_framework import generics
from .models import Category, Sub_Category, Clothe
from django.views.generic.edit import FormView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from inventory.serializers import CategotySerializer, Sub_CategorySerializer, ClothesDetailsSerializer, ClothesSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategotySerializer

class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategotySerializer

class SubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = Sub_Category.objects.all()
    serializer_class = Sub_CategorySerializer

class SubCategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sub_Category.objects.all()
    serializer_class = Sub_CategorySerializer



class ClothesViewAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ClothesSerializer(data=request.data)

        if serializer.is_valid():
            image1 = serializer.validated_data['image1']
            image2 = serializer.validated_data.get('image2', [])
            image3 = serializer.validated_data.get('image3', [])

            for idx in range(min(len(image1), len(image2), len(image3))):

                Clothe.objects.create(
                    clothes_orginal=image1[idx],
                    clothes=image2[idx] if idx < len(image2) else None,
                    clothes_mask=image3[idx] if idx < len(image3) else None,
                )

            return Response({'message': 'Files uploaded successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

# class ClothesViewAPI(ListCreateAPIView):
#     queryset = Clothe.objects.all()
#     serializer_class = ClothesSerializer

#     def get_queryset(self):
#         return Clothe.objects.select_related('category', 'sub_category')

class ClothesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clothe.objects.all()
    serializer_class = ClothesDetailsSerializer

class ClothesListView(ListAPIView):
    queryset = Clothe.objects.all()
    serializer_class = ClothesDetailsSerializer


class ClotheCountPerCategory(APIView):
    def get(self, request):
        categories = Category.objects.all()
        category_counts = []
        for category in categories:
            count = Clothe.objects.filter(category=category).count()
            category_counts.append({
                'category': category.name,
                'count': count
            })
        return Response(category_counts)

class ClotheCountPerSubCategory(APIView):
    def get(self, request):
        subcategories = Sub_Category.objects.all()
        subcategory_counts = []
        for subcategory in subcategories:
            count = Clothe.objects.filter(sub_category=subcategory).count()
            subcategory_counts.append({
                'subcategory': subcategory.name,
                'count': count
            })
        return Response(subcategory_counts)
    

from .serializers import ClotheSerializer
from rest_framework.generics import CreateAPIView

class ClotheCreateView(CreateAPIView):
    queryset = Clothe.objects.all()
    serializer_class = ClotheSerializer
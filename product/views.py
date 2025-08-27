from collections import OrderedDict
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsModeratorPermission
from .models import Category, Product, Review
from product.serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer
)
from common.validators import validate_age
from common.permissions import IsOwner, IsAnonymous
from rest_framework.permissions import BasePermission



PAGE_SIZE = 5

from rest_framework.permissions import BasePermission

class IsOwnerOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == "POST" and request.user.is_authenticated:
            from common.validators import validate_age
            try:
                validate_age(request.user)
                return True
            except:
                return False

        if request.method in ["GET", "HEAD", "OPTIONS"] and request.user.is_authenticated:
            return True

        return False

class CustomPagination(PageNumberPagination):
    page_size = PAGE_SIZE

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("total", self.page.paginator.count),
            ("next", self.get_next_link()),
            ("previous", self.get_previous_link()),
            ("results", data)
        ]))


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    permission_classes = [IsModeratorPermission]

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(**serializer.validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"
    permission_classes = [IsModeratorPermission]

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get("name")
        category.save()
        return Response(CategorySerializer(category).data)



class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrSuperuser]

    def post(self, request, *args, **kwargs):
        validate_age(request.user)  

        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = Product.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            category=serializer.validated_data['category'],
            owner=request.user,
        )
        return Response(ProductSerializer(product).data, status=201)

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    permission_classes = [IsModeratorPermission]

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(product, field, value)
        product.save()
        return Response(ProductSerializer(product).data)


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    permission_classes = [IsModeratorPermission]

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(**serializer.validated_data)
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"
    permission_classes = [IsModeratorPermission]

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(review, field, value)
        review.save()
        return Response(ReviewSerializer(review).data)

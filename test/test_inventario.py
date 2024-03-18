# import pytest
# from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError
# from inventario.models import Product, Category

# # def category():
# #     return Category.objects.create(name='Test Category')

# @pytest.mark.django_db
# def test_create_product(category):
#     product = Product.objects.create(
#         name='Test Product',
#         brand='Test Brand',
#         description='Test Description',
#         category=category,
#         price=10.5,
#         quantity=5,
#         image='product/test_image.jpg'
#     )
#     assert product.name == 'Test Product'
#     assert product.brand == 'Test Brand'
#     assert product.description == 'Test Description'
#     assert product.category == category
#     assert product.price == 10.5
#     assert product.quantity == 5
#     assert str(product.image) == 'product/test_image.jpg'

# @pytest.mark.django_db
# def test_price_validation():
#     with pytest.raises(ValidationError):
#         Product.objects.create(
#             name='Test Product',
#             brand='Test Brand',
#             description='Test Description',
#             category=Category.objects.create(name='Test Category'),
#             price=-5,  # Negative price should raise a validation error
#             quantity=5,
#             image='product/test_image.jpg'
#         )

# @pytest.mark.django_db
# def test_quantity_default():
#     product = Product.objects.create(
#         name='Test Product',
#         brand='Test Brand',
#         description='Test Description',
#         category=Category.objects.create(name='Test Category'),
#         price=10.5,
#         image='product/test_image.jpg'
#     )
#     assert product.quantity == 0

# @pytest.mark.django_db
# def test_unique_name():
#     Product.objects.create(
#         name='Test Product',
#         brand='Test Brand',
#         description='Test Description',
#         category=Category.objects.create(name='Test Category'),
#         price=10.5,
#         quantity=5,
#         image='product/test_image.jpg'
#     )
#     # Creating a product with the same name should raise IntegrityError
#     with pytest.raises(IntegrityError):
#         Product.objects.create(
#             name='Test Product',
#             brand='Test Brand',
#             description='Another Test Description',
#             category=Category.objects.create(name='Another Test Category'),
#             price=20.0,
#             quantity=3,
#             image='product/another_test_image.jpg'
#         )

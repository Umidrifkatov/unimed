from core.models import *

for product in Product.objects.all():
    manufacturer_name = product.name.split(' - ')[0]
    manufacturer = ProductManufacturer.objects.get_or_create(name=manufacturer_name)[0]
    product.manufacturer = manufacturer
    product.save()
    print(product.manufacturer.name)
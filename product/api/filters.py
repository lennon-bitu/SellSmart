from dj_rql.filter_cls import AutoRQLFilterClass, FilterLookups
from product.models import Brand, Category, Product


class BrandFilterClass(AutoRQLFilterClass):
    MODEL = Brand


class CategoryFilterClass(AutoRQLFilterClass):
    MODEL = Category


class ProductFilterClass(AutoRQLFilterClass):
    MODEL = Product
    FILTER = [
        {
            'fitler': 'brand',
            'source': 'brand__name'
        },
        {
            'fitler': 'category',
            'source': 'category__name'
        },

    ]
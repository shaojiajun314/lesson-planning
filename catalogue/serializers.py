# from sorl import thumbnail
from rest_framework import serializers

from education.catalogue.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'path', 'depth', 'numchild', 'name', 'image', 'image_name')
    # image = serializers.SerializerMethodField()
    #
    # def get_image(self, obj):
    #     im = thumbnail.get_thumbnail(obj.image,
    #         '375x208', crop='bottom', upscale=False)
    #     try:
    #         return im.url
    #     except:
    #         return ''



# class ProductImageSerializer(serializers.ModelSerializer):
#
#     thumb = serializers.SerializerMethodField()
#     original = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ProductImage
#         fields = ('original', 'display_order', 'thumb')
#
#     def get_original(self, obj):
#         im = thumbnail.get_thumbnail(obj.original,
#             '375x375', crop='center', upscale=False)
#         return im.url
#
#     def get_thumb(self, obj):
#         im = thumbnail.get_thumbnail(obj.original,
#             '132x132', crop='center', upscale=False)
#         return im.url
#
# class ProductDetailImageSerializer(serializers.ModelSerializer):
#
#     def get_original(self, obj):
#         im = thumbnail.get_thumbnail(obj.original,
#             '375x375', crop='center', upscale=False)
#         return im.url
#
#     class Meta:
#         model = ProductDetailImage
#         fields = ('original', 'display_order')
#
#
# class StockRecordSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = StockRecord
#         fields = ('price_retail', 'num_in_stock', 'original_price')
#
# class ProductListSerializer(serializers.ModelSerializer):
#
#     images = ProductImageSerializer(many=True, read_only=True)
#     # XXX:
#     # stockrecords = StockRecordSerializer(many=True, read_only=True)
#     stockrecords = serializers.SerializerMethodField()
#
#     children_stockrecords = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'description', 'images', 'stockrecords', 'store_id', 'structure', 'children_stockrecords')
#
#     def get_children_stockrecords(self, obj):
#         stock_list = []
#         for child in obj.children.all():
#             stock_list.append(list(child.stockrecords.all().values('price_retail', 'num_in_stock', 'product_id')))
#         return stock_list
#
#     def get_stockrecords(self, obj):
#         stockrecords = obj.stockrecords.all()
#         if stockrecords:
#             return StockRecordSerializer(stockrecords, many=True).data
#             # return list(stockrecords.values('price_retail', 'num_in_stock', 'original_price'))
#         else:
#             s = obj.children.all()[0].stockrecords.all()[0]
#             for i in obj.children.all():
#                 s_tmp = i.stockrecords.all()[0]
#                 if s.price_retail > s_tmp.price_retail:
#                     s = s_tmp
#             return [StockRecordSerializer(s, many=False).data]
#
#             # return list(obj.children.all()[0].stockrecords.all().values('price_retail', 'num_in_stock','original_price'))
#
# class ProductAttributeValuesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttributeValue
#         fields = '__all__'
#
# class ChildrenProductSerializer(serializers.ModelSerializer):
#
#     images = ProductImageSerializer(many=True, read_only=True)
#     stockrecords = StockRecordSerializer(many=True, read_only=True)
#     attribute_values = ProductAttributeValuesSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'description', 'images', 'stockrecords',
#         'store_id', 'structure', 'cate_value', 'attribute_values')
#
# class ProductStrategySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductStrategy
#         fields = ('limit_num_per', 'limit_lv')
#
# class ProductDetailSerializer(ProductListSerializer):
#
#     detail_images = ProductDetailImageSerializer(many=True, read_only=True)
#     children = ChildrenProductSerializer(many=True, read_only=True)
#
#     attribute = serializers.SerializerMethodField()
#     attribute_values = ProductAttributeValuesSerializer(many=True, read_only=True)
#     strategy = ProductStrategySerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'description', 'images',
#             'stockrecords', 'detail_images', 'store_id',
#             'children', 'type', 'attribute', 'attribute_values', 'strategy')
#
#     def get_attribute(self, obj):
#         return list(obj.product_class.attributes.all().values('id', 'name'))

from haystack import indexes

from education.catalogue.models import Example


# XXX:  oscar modify class
class ExampleIndex(indexes.SearchIndex, indexes.Indexable):
    # Search text
    text = indexes.CharField(document=True,
        use_template=True)

    content = indexes.CharField(model_attr='content')
    difficulty = indexes.CharField(model_attr='difficulty')
    category = indexes.MultiValueField(null=True, faceted=True)
    answer = indexes.MultiValueField(null=True, faceted=True)


    def get_model(self):
        return Example

    def index_queryset(self, using=None):
        # Only index browsable products (not each individual child product)
        return self.get_model().objects.order_by('-date_created')

    def prepare_category(self, obj):
        categories = obj.categories.all()
        if len(categories) > 0:
            return [category.name for category in categories]

    def prepare_answer(self, obj):
        answers = obj.answers.all()
        if len(answers) > 0:
            return [answer.answer for answer in answers]



    # upc = indexes.CharField(model_attr="upc", null=True)
    # status = indexes.CharField(model_attr="status", null=True)
    # type = indexes.CharField(model_attr="type", null=True)
    # title = indexes.EdgeNgramField(model_attr='title', null=True)
    # title_exact = indexes.CharField(model_attr='title', null=True, indexed=False)
    #
    # # Fields for faceting
    # product_class = indexes.CharField(null=True, faceted=True)
    # category = indexes.MultiValueField(null=True, faceted=True)
    # price = indexes.FloatField(null=True, faceted=True)
    # num_in_stock = indexes.IntegerField(null=True, faceted=True)
    # rating = indexes.IntegerField(null=True, faceted=True)
    #
    # # Spelling suggestions
    # suggestions = indexes.FacetCharField()
    #
    # date_created = indexes.DateTimeField(model_attr='date_created')
    # date_updated = indexes.DateTimeField(model_attr='date_updated')
    #
    # _strategy = None

    # def read_queryset(self, using=None):
    #     return self.get_model().browsable.base_queryset()
    #
    # def prepare_product_class(self, obj):
    #     return obj.get_product_class().name
    #
    # def prepare_category(self, obj):
    #     categories = obj.categories.all()
    #     if len(categories) > 0:
    #         return [category.full_name for category in categories]
    #
    # def prepare_rating(self, obj):
    #     if obj.rating is not None:
    #         return int(obj.rating)
    #
    # # Pricing and stock is tricky as it can vary per customer.  However, the
    # # most common case is for customers to see the same prices and stock levels
    # # and so we implement that case here.
    #
    # def get_strategy(self):
    #     if not self._strategy:
    #         self._strategy = Selector().strategy()
    #     return self._strategy
    #
    # def prepare_price(self, obj):
    #     strategy = self.get_strategy()
    #     result = None
    #     if obj.is_parent:
    #         result = strategy.fetch_for_parent(obj)
    #     elif obj.has_stockrecords:
    #         result = strategy.fetch_for_product(obj)
    #
    #     if result:
    #         if result.price.is_tax_known:
    #             return result.price.incl_tax
    #         return result.price.excl_tax
    #
    # def prepare_num_in_stock(self, obj):
    #     strategy = self.get_strategy()
    #     if obj.is_parent:
    #         # Don't return a stock level for parent products
    #         return None
    #     elif obj.has_stockrecords:
    #         result = strategy.fetch_for_product(obj)
    #         return result.stockrecord.net_stock_level
    #
    # def prepare(self, obj):
    #     prepared_data = super(ProductIndex, self).prepare(obj)
    #
    #     # We use Haystack's dynamic fields to ensure that the title field used
    #     # for sorting is of type "string'.
    #     if is_solr_supported():
    #         prepared_data['title_s'] = prepared_data['title']
    #
    #     # Use title to for spelling suggestions
    #     prepared_data['suggestions'] = prepared_data['text']
    #
    #     return prepared_data
    #
    # def get_updated_field(self):
    #     """
    #     Used to specify the field used to determine if an object has been
    #     updated
    #
    #     Can be used to filter the query set when updating the index
    #     """
    #     return 'date_updated'

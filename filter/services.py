from .documents import ProductDocument

def create_product(data):
    existing = ProductDocument.search().filter('term', id=data['id']).execute()
    if existing.hits.total.value > 0:
        raise ValueError(f"The product with id={data['id']} already exists!")
    doc = ProductDocument(**data)
    doc.meta.id = data['id']
    doc.save()
    return doc.to_dict()

def search_products(filters=None, sort_by=None, sort_order="asc"):
    s = ProductDocument.search()
    if filters:
        category = filters.get('category')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')
        name = filters.get('name')
        description = filters.get('description')


        if category:
            s = s.filter('term', category=category)

        price_range = {}
        if min_price is not None:
            try:
                price_range['gte'] = float(min_price)
            except ValueError:
                pass
        if max_price is not None:
            try:
                price_range['lte'] = float(max_price)
            except ValueError:
                pass
        if price_range:
            s = s.filter('range', price=price_range)

        if name:
            s = s.query("match_phrase", name=name)

        if description:
            s = s.query("match", description=description)

    if sort_by:
        sort_field = sort_by
        s = s.sort({sort_field: {"order": sort_order}})
        
            
    return [hit.to_dict() for hit in s.execute()]
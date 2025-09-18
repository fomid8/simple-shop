from .documents import *
from elasticsearch_dsl import Q
from datetime import datetime

def create_product(data):
    existing = ProductDocument.search().filter('term', id=data['id']).execute()
    if existing.hits.total.value > 0:
        raise ValueError(f"The product with id={data['id']} already exists!")
    
    category_name = data.get('category', '').lower()
    category = CategoryDocument.get(id=category_name, ignore=404)
    if not category:
        raise ValueError(f"Category '{data.get('category')}' does not exist!")
    
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
        allowed_sort_fields = ['price', 'created_at', 'name']
        if sort_by in allowed_sort_fields:
            s = s.sort({sort_by: {"order": sort_order}})
            
    return [hit.to_dict() for hit in s.execute()]


def create_category(data):
    existing = CategoryDocument.search().filter('term', _id=data['name']).execute()
    if existing.hits.total.value > 0:
        raise ValueError(f"The category with name={data['name']} already exists!")
    
    doc = CategoryDocument(**data)
    doc.meta.id = data['name'].lower()
    doc.save()
    return doc.to_dict()

def search_categories(query=None):
    s = CategoryDocument.search()
    if query:
        s = s.query(
            'multi_match',
            query=query,
            fields=['name', 'description']
        )
    return [hit.to_dict() for hit in s.execute()]


def create_order(data):
    doc = OrderedProductDocument(**data)
    doc.meta.id = data['id']
    doc.save()

    cart_search = CartDocument.search().filter('term', user_id=data['user_id']).execute()
    if cart_search.hits.total.value > 0:
        cart_doc = cart_search[0]
        cart_dict = cart_doc.to_dict()
        product_ids = cart_dict.get('product_ids', [])
        numbers = cart_dict.get('numbers', [])
        if data['product_id'] in product_ids:
            index = product_ids.index(data['product_id'])
            numbers[index] += data['number']
        else:
            product_ids.append(data['product_id'])
            numbers.append(data['number'])
        total_price = (cart_dict.get('total_price') or 0.0) + (data['price'] * data['number'])
        cart_doc.update(
            product_ids=product_ids,
            numbers=numbers,
            total_price=total_price,
            state = "open",
            updated_at=datetime.now()
        )

    else:
        total_price = data['price'] * data['number']
        cart_doc = CartDocument(
            user_id=data['user_id'],
            product_ids=[data['product_id']],
            numbers=[data['number']],
            total_price=total_price,
            state="open",
            updated_at=datetime.now()
        )
        cart_doc.save()

    return doc.to_dict()

def search_orders(filters=None, sort_by=None, sort_order="asc"):
    s = OrderedProductDocument.search()
    if filters:
        user = filters.get('user')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')
        product = filters.get('product')
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')

        if user:
            s = s.filter('term', user_id=user)

        if product:
            product_search = ProductDocument.search().query(
                'match_phrase_prefix', name=product
            )
            product_ids = [hit.id for hit in product_search.execute()]
            if product_ids:
                s = s.filter('terms', product_id=product_ids)
            else:
                return [] 

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

        if start_date or end_date:
            date_range = {}
            if start_date:
                date_range['gte'] = start_date
            if end_date:
                date_range['lte'] = end_date
            s = s.filter('range', ordered_at=date_range)


    if sort_by:
        allowed_sort_fields = ['price', 'number', 'product_id', 'ordered_at']
        if sort_by in allowed_sort_fields:
            s = s.sort({sort_by: {"order": sort_order}})
            
    return [hit.to_dict() for hit in s.execute()]

# def get_orders(user_id):
#     s = OrderedProductDocument.search().filter('term', user_id=user_id)
#     return [hit.to_dict() for hit in s.execute()]


def search_carts(filters=None, sort_by=None, sort_order="asc"):
    s = CartDocument.search()
    if filters:
        state = filters.get('state')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')
        product = filters.get('product')
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')

        if state:
            s = s.filter('term', state=state)

        if product:
            product_search = ProductDocument.search().query(
                'match_phrase_prefix', name=product
            )
            product_ids = [hit.id for hit in product_search.execute()]
            if product_ids:
                s = s.filter('terms', product_ids=product_ids)
            else:
                return [] 

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
            s = s.filter('range', total_price=price_range)

        if start_date or end_date:
            date_range = {}
            if start_date:
                date_range['gte'] = start_date
            if end_date:
                date_range['lte'] = end_date
            s = s.filter('range', updated_at=date_range)


    if sort_by:
        allowed_sort_fields = ['total_price', 'updated_at']
        if sort_by in allowed_sort_fields:
            s = s.sort({sort_by: {"order": sort_order}})
            
    return [hit.to_dict() for hit in s.execute()]



def get_cart(user_id):
    try:
        s = CartDocument.search().filter('term', user_id=user_id)
        res = s.execute()
        if res.hits.total.value > 0:
            return res.hits[0]
        return None
    except Exception:
        return None

def clear_cart(user_id):
    cart = get_cart(user_id)
    if cart:
        cart.product_ids = []
        cart.numbers = []
        cart.updated_at = datetime.now()
        cart.state = "close"
        cart.total_price = 0.0
        cart.save()
        return True
    return False

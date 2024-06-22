from utils.discount_handler import DiscountHandler


async def format_product_data(product_data: dict) -> dict:
        
        discount_handler = DiscountHandler()        
        product_info = {
            "product_name": "",
            "value": 0,
            "original": 0,
            "product_id": "",
            "product_image_url": "",
            "product_link": "",
            "is_in_stock": True,
            "is_limited_quantity": False,
            "service_type": "",
            "discount": 0
        }

        # Get image sizes safely
        image_sizes = product_data.get('media', {}).get('images', [{}])[0].get('sizes', [])

        # Populate product_info with values using .get() method
        product_info['product_name'] = product_data.get('identifiers', {}).get('productLabel', '')
        product_info['product_link'] = 'https://www.homedepot.com' + product_data.get('identifiers', {}).get('canonicalUrl', '')
        product_info['product_id'] = product_data.get('itemId', '')
        product_info['product_image_url'] = product_data.get('media', {}).get('images', [{}])[0].get('url', '').replace("<SIZE>", image_sizes[-1] if image_sizes else '')
        product_info['value'] = product_data.get('pricing', {}).get('value', 0)
        product_info['original'] = product_data.get('pricing', {}).get('original', 0)
        product_info['service_type'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('type', '')
        product_info['is_in_stock'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('locations', [{}])[0].get('inventory', {}).get('isInStock', True)
        product_info['is_limited_quantity'] = product_data.get('fulfillment', {}).get('fulfillmentOptions', [{}])[0].get('services', [{}])[0].get('locations', [{}])[0].get('inventory', {}).get('isLimitedQuantity', False)
        product_info['discount'] = await discount_handler.find_product_discount(
            prev_price=product_info['original'], curr_price=product_info['value']
        )
        return product_info

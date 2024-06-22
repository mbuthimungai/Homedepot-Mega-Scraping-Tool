class DiscountHandler:
    def __init__(self) -> None:
        pass
    
    async def find_product_discount(self, prev_price: float,
                                    curr_price: float) -> float:
        """Calculates the product discount"""
        discount = (curr_price * 100) / prev_price
        return discount

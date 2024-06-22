class SearchModel:
    def __init__(self) -> None:
        pass

    async def create_search_model_query(self, category_code: str, page_size: int, 
                                        start_index: int) -> dict:
        data = {}
        data['operationName'] = "searchModel"
        data['variables'] = {}
        # data['variables']['itemIds'] = skus
        data['variables']['storeId'] = "3004"
        data['variables']['navParam'] = category_code  # Add $ before navParam
        data["variables"]["pageSize"] = page_size
        data["variables"]["startIndex"] = start_index
        data['query'] = """
        query searchModel($storeId: String, $zipCode: String, $startIndex: Int, $pageSize: Int, $orderBy: ProductSort, $keyword: String, $storefilter: StoreFilter = ALL, $channel: Channel = DESKTOP, $navParam: String) {
        searchModel(keyword: $keyword, storefilter: $storefilter, storeId: $storeId, channel: $channel, navParam: $navParam) {
            products(startIndex: $startIndex, pageSize: $pageSize, orderBy: $orderBy) {
            identifiers {
                canonicalUrl
                brandName
                itemId
                productLabel
                modelNumber
            }
            itemId
            media {
                images {
                url
                sizes
                }
            }
            pricing(storeId: $storeId) {
                value
                original
            }
            info {
                categoryHierarchy 
            }
            fulfillment(storeId: $storeId, zipCode: $zipCode) {
                fulfillmentOptions {
                type
                fulfillable
                services {
                    type
                    locations {
                    inventory {
                        isOutOfStock
                        isInStock
                        isLimitedQuantity
                        isUnavailable
                        quantity
                    }
                    type
                    }
                }
                }
            }
            reviews {
                ratingsReviews {
                totalReviews
                averageRating
                __typename
                }
                __typename
            }
            }
            id
            searchReport {
            totalProducts
            }
        }
        }
        """
        return data
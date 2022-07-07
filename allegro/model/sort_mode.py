from enum import Enum


class SortMode(Enum):
 ASCENDING_PRICE = "+price"
 DESCENDING_PRICE = "-price"
 RELEVANCE = "relevance"
 WITH_DELIVERY_PRICE_ASCENDING = "+withDeliveryPrice"
 WITH_DELIVERY_PRICE_DESCENDING = "-withDeliveryPrice"
 START_TIME = "+startTime"
 END_TIME = "-endTime"

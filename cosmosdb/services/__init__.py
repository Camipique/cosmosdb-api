from .ItemService import ItemService, item_type
from .UserService import UserService, user_type
from .StoreService import StoreService, store_type

SERVICES = [
    ItemService,
    UserService,
    StoreService
]

TYPES = {
    'Item': item_type,
    'User': user_type,
    'Store': store_type
}

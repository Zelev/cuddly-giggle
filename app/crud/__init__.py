from .crud_item import item
from .crud_user import user
from .crud_role import role
from .crud_biosignal import biosignal
from .crud_lead import lead
from .crud_insight import insight

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.biosignal import Biosignal  # noqa
from app.models.insight import Insight  # noqa
from app.models.item import Item  # noqa
from app.models.lead import Lead  # noqa
from app.models.role import Role  # noqa
from app.models.user import User  # noqa

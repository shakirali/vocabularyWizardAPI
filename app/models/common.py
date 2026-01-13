import uuid

from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.core.config import settings

# UUID type compatible with both PostgreSQL and SQLite
if "postgresql" in settings.DATABASE_URL:
    UUIDType = PostgresUUID(as_uuid=True)
else:

    class GUID(TypeDecorator):
        impl = CHAR
        cache_ok = True

        def load_dialect_impl(self, dialect):
            return dialect.type_descriptor(CHAR(36))

        def process_bind_param(self, value, dialect):
            if value is None:
                return value
            elif isinstance(value, uuid.UUID):
                return str(value)
            else:
                return str(uuid.UUID(value))

        def process_result_value(self, value, dialect):
            if value is None:
                return value
            else:
                return uuid.UUID(value)

    UUIDType = GUID

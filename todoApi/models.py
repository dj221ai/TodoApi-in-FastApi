from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    # priority = Column(Integer)
    complete = Column(Boolean, default=True)



# The three biggest are:
# .dict() function is now renamed to .model_dump()
# schema_extra function within a Config class is now renamed to json_schema_extra
# Optional variables need a =None example: id: Optional[int] = None   

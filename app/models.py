from . import db
from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)   

from sqlalchemy import (
    String,
    ForeignKey
)

# ----------------------- START BASE CLASS -----------------------

class BaseModel(db.Model):
    __abstract__ = True
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    def __repr__(self):
        attrs = [f"{col.name}={getattr(self, col.name)}" for col in self.__table__.columns]
        return f"<{self.__getClassName__()}({', '.join(attrs)})>"
    
    def get_json(self,include_relationships: bool = False):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
    
        if include_relationships:
            for rel in self.__mapper__.relationships:
                val = getattr(self, rel.key)
                if isinstance(val, list):
                    data[rel.key] = [item.get_json() for item in val]
                elif val is not None:
                    data[rel.key] = val.get_json()
                else:
                    data[rel.key] = None
                    
        return data

    def __getClassName__(self):
        return type(self).__name__


class BaseCreatable(BaseModel):
    __abstract__ = True
    
    name:Mapped[str]
    version:Mapped[str]
    is_homebrew:Mapped[bool]
    description:Mapped[Optional[str]]
    
# ----------------------- END BASE CLASS -----------------------

# ----------------------- START AUTH CLASS -----------------------

class User(BaseModel):
    username:Mapped[str] = mapped_column(String(20),unique=True)
    password:Mapped[str]
    
    auth_level:Mapped[int]
    
    spell_creation:Mapped["UserSpell"] = relationship("UserSpell",back_populates="user")
    user_session:Mapped["UserSession"] = relationship("UserSession",back_populates="user")
    
    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},username={self.username}>"
    
    def __get_secrets__(self,include_relationships = None):
        return {
            "id":self.id,
            "username":self.username,
            "password":self.password,
            "auth_level":self.auth_level
        }
        
    def get_json(self,include_relationships = None):
        return {
            "id":self.id,
            "username":self.username,
        }
        
class UserSession(BaseModel):
    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"),unique=True)
    user:Mapped["User"] = relationship("User",back_populates="user_session")
    
    session:Mapped[str]
    
    expires_at:Mapped[int]

# ----------------------- END AUTH CLASS -----------------------

# ----------------------- START MAIN CLASS -----------------------

class SpellSchool(BaseCreatable):
    spell_stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="spell_school")
    

class Spell(BaseCreatable):
    id_stats:Mapped[int] = mapped_column(ForeignKey("spell_stats.id"))
    stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="spell")
    
    user_creation:Mapped["UserSpell"] = relationship("UserSpell",back_populates="spell")

# ----------------------- END MAIN CLASS -----------------------

# ----------------------- START RELATIONSHIP WITH USER CLASS -----------------------

class UserSpell(BaseModel):
    id_spell:Mapped[int] = mapped_column(ForeignKey("spell.id"),unique=True)
    spell:Mapped["Spell"] = relationship("Spell",back_populates="user_creation")
    
    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped["User"] = relationship("User",back_populates="spell_creation")

# ----------------------- END RELATIONSHIP WITH USER CLASS -----------------------


# ----------------------- START RELATIONSHIP CLASS -----------------------

class SpellStats(BaseModel):
    spell:Mapped["Spell"] = relationship("Spell",back_populates="stats")
    
    level:Mapped[int]
    is_ritual:Mapped[bool]
    
    casting_time:Mapped[int]
    casting_action_type:Mapped[str]
    casting_description:Mapped[str]
    
    duration_time:Mapped[int]
    duration_time_type:Mapped[str]
    duration_type:Mapped[str]
    
    range_distance:Mapped[str]
    range_type:Mapped[str]
    
    area_distance:Mapped[Optional[str]]
    area_type:Mapped[Optional[str]]
    
    id_spell_school:Mapped[int] = mapped_column(ForeignKey("spell_school.id"))
    spell_school:Mapped["SpellSchool"] = relationship("SpellSchool",back_populates="spell_stats")
    
    id_components:Mapped[int] = mapped_column(ForeignKey("spell_components.id"),unique=True)
    components:Mapped["SpellComponents"] = relationship("SpellComponents",back_populates="spell_stats")
    
    id_scaling:Mapped[Optional[int]] = mapped_column(ForeignKey("spell_scaling.id"),unique=True)
    scaling:Mapped["SpellScaling"] = relationship("SpellScaling",back_populates="spell_stats")
    
    
class SpellComponents(BaseModel):
    spell_stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="components")

    verbal:Mapped[bool]
    somantic:Mapped[bool]
    material:Mapped[bool]
    special:Mapped[bool]
    
    description:Mapped[Optional[str]]
    
class SpellScaling(BaseModel):
    spell_stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="scaling")
    description:Mapped[Optional[str]]
    
# ----------------------- END RELATIONSHIP CLASS -----------------------

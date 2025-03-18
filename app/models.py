from . import db
from flask_login import UserMixin
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
        return f"<{self.__getClassName__()}(id={self.id})>"
    
    def get_dict(self):
        return {
            "id":self.id
        }

    def __getClassName__(self):
        return type(self).__name__


class BaseCreatable(BaseModel):
    __abstract__ = True
    
    name:Mapped[str]
    version:Mapped[str]
    is_homebrew:Mapped[bool]
    description:Mapped[Optional[str]]
    
    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},name={self.name},version={self.version},is_homebrew={self.is_homebrew},description={self.description})>"
    
    def get_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "version":self.version,
            "is_homebrew":self.is_homebrew,
            "description":self.description,
        }
        
        
# ----------------------- END BASE CLASS -----------------------

# ----------------------- START AUTH CLASS -----------------------

class User(BaseModel,UserMixin):
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(20),unique=True)
    password:Mapped[str]
    
    auth_level:Mapped[int]
    
    spell_creation:Mapped["UserSpell"] = relationship("UserSpell",back_populates="user")
    
    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},username={self.username}>"
    
    def __get_secrets__(self):
        return {
            "id":self.id,
            "username":self.username,
            "password":self.password,
            "auth_level":self.auth_level
        }
        
    def get_dict(self):
        return {
            "id":self.id,
            "username":self.username,
        }

# ----------------------- END AUTH CLASS -----------------------

# ----------------------- START MAIN CLASS -----------------------

class SpellSchool(BaseCreatable):
    spell_stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="spell_school")
    

class Spell(BaseCreatable):
    id_stats:Mapped[int] = mapped_column(ForeignKey("spell_stats.id"))
    stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="spell")
    
    user_creation:Mapped["UserSpell"] = relationship("UserSpell",back_populates="spell")
    
    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},name={self.name},version={self.version},is_homebrew={self.is_homebrew},description={self.description},id_stats={self.id_stats})>"

    
    def get_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "version":self.version,
            "is_homebrew":self.is_homebrew,
            "description":self.description,
            "stats":self.stats.get_dict(),
        }

# ----------------------- END MAIN CLASS -----------------------

# ----------------------- START RELATIONSHIP WITH USER CLASS -----------------------

class UserSpell(BaseModel):
    id_spell:Mapped[int] = mapped_column(ForeignKey("spell.id"),unique=True)
    spell:Mapped["Spell"] = relationship("Spell",back_populates="user_creation")
    
    id_user:Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:Mapped["User"] = relationship("User",back_populates="spell_creation")
    
    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},id_user={self.id_user},id_spell={self.id_spell})>"
    
    def get_dict(self):
        return {
            "id":self.id,
            "user":self.user.get_dict(),
            "spell":self.spell.get_dict()
        }

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
    
    def __repr__(self):
        
        r =f"<{self.__getClassName__()}(id={self.id},level={self.level},is_ritual={self.is_ritual},casting_time={self.casting_time},casting_action_type={self.casting_action_type},"
        r += f"casting_description={self.casting_description},duration_time={self.duration_time},duration_time_type={self.duration_time_type},duration_type={self.duration_type},"
        r += f"range_distance={self.range_distance},range_type={self.range_type},area_distance={self.area_distance},area_type={self.area_type},id_spell_school={self.id_spell_school},"
        r += f"id_components={self.id_components},id_scaling={self.id_scaling}"
        r += ")>"
        
        return r
    
    def get_dict(self):
        return {
            "id":self.id,
            "level":self.level,
            "is_ritual":self.is_ritual,
            "casting_time":self.casting_time,
            "casting_action_type":self.casting_action_type,
            "casting_description":self.casting_description,
            "duration_time":self.duration_time,
            "duration_time_type":self.duration_time_type,
            "duration_type":self.duration_type,
            "range_distance":self.range_distance,
            "range_type":self.range_type,
            "area_distance":self.area_distance,
            "area_type":self.area_type,
            "spell_school":self.spell_school.get_dict(),
            "components":self.components.get_dict(),
            "scaling":self.scaling.get_dict()
        }
    
    
class SpellComponents(BaseModel):
    spell_stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="components")

    verbal:Mapped[bool]
    somantic:Mapped[bool]
    material:Mapped[bool]
    special:Mapped[bool]
    
    description:Mapped[Optional[str]]

    
    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},verbal={self.verbal},somantic={self.somantic},material={self.material},special={self.special},description={self.description})>"
    
    def get_dict(self):
        return {
            "id":self.id,
            "verbal":self.verbal,
            "somantic":self.somantic,
            "material":self.material,
            "special":self.special,
            "description":self.description
        }
    
class SpellScaling(BaseModel):
    spell_stats:Mapped["SpellStats"] = relationship("SpellStats",back_populates="scaling")

    description:Mapped[Optional[str]]

    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},description={self.description})>"
    
    def get_dict(self):
        return {
            "id":self.id,
            "description":self.description
        }
    
# ----------------------- END RELATIONSHIP CLASS -----------------------

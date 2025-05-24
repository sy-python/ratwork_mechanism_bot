from .debug import DebugCog
from .menace import MenaceCog

development_cogs = (DebugCog, MenaceCog)
production_cogs = (MenaceCog,)

__all__ = ("development_cogs", "production_cogs")

import logging
from data.pipelines.EntityPipeline import EntityPipeline
from data.entities.PropertyEntityHandler import PropertyEntityHandler
from data.entities.EntityHandler import EntityHandler


class PropertyPipeline(EntityPipeline):
    def _get_entity_handler(self) -> EntityHandler:
        return PropertyEntityHandler()

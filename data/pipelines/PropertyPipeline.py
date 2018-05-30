import logging
from data.pipelines.EntityPipeline import EntityPipeline
from data.entities import PropertyEntityHandler, EntityHandler


class PropertyPipeline(EntityPipeline):
    def _get_entity_handler(self) -> EntityHandler:
        return PropertyEntityHandler()

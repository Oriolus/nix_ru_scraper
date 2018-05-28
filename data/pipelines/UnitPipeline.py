import logging
from data.pipelines.EntityPipeline import EntityPipeline
from data.entities.UnitEntityHandler import UnitEntityHandler


class UnitPipeline(EntityPipeline):

    def _get_entity_handler(self):
        return UnitEntityHandler()

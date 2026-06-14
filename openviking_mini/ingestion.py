from typing import Optional

from openviking_mini.adapters import AbstractGenerator, FirstLineAbstractGenerator, FirstLinesOverviewGenerator, OverviewGenerator
from openviking_mini.context_store import ContextLayer, ContextStoreError


class DeterministicIngestor:
    def __init__(
        self,
        abstract_generator: Optional[AbstractGenerator] = None,
        overview_generator: Optional[OverviewGenerator] = None,
    ) -> None:
        self._abstract_generator = abstract_generator or FirstLineAbstractGenerator()
        self._overview_generator = overview_generator or FirstLinesOverviewGenerator()

    def ingest(self, content: str) -> ContextLayer:
        details = content.strip()
        if not details:
            raise ContextStoreError("resource content must not be blank.")

        abstract = self._abstract_generator.generate(details)
        overview = self._overview_generator.generate(details)
        return ContextLayer(abstract=abstract, overview=overview, details=details)

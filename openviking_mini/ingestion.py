from openviking_mini.context_store import ContextLayer, ContextStoreError


class DeterministicIngestor:
    def ingest(self, content: str) -> ContextLayer:
        details = content.strip()
        if not details:
            raise ContextStoreError("resource content must not be blank.")

        lines = [line.strip() for line in details.splitlines() if line.strip()]
        abstract = lines[0]
        overview = " ".join(lines[:2])
        return ContextLayer(abstract=abstract, overview=overview, details=details)

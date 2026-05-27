from pydantic import BaseModel, Field
from typing import List, Optional

class PaperReference(BaseModel):
    """Estructura para representar un artículo científico indexado en PubMed o OpenAlex."""
    pmid: str = Field(description="Identificador único (PMID o DOI) del artículo")
    title: str = Field(description="Título completo del artículo científico")
    authors: str = Field(description="Autores principales o primer autor et al.")
    relevance_score: float = Field(description="Nivel de relevancia del artículo para la hipótesis (0.0 a 1.0)")
    key_finding: str = Field(description="Hallazgo principal del artículo relevante para nuestro contexto")

class Hypothesis(BaseModel):
    """Estructura de una propuesta o hipótesis de descubrimiento científico."""
    title: str = Field(description="Título conciso, informativo y elegante de la hipótesis")
    mechanism: str = Field(description="Descripción detallada del mecanismo biológico o molecular propuesto")
    evidence: List[PaperReference] = Field(default=[], description="Lista de artículos científicos de respaldo real")
    confidence_level: str = Field(description="Nivel de certidumbre científica sustentada en literatura: HIGH, MEDIUM o LOW")

class TournamentRating(BaseModel):
    """Resultado estructurado de la arena de debate/torneo Elo entre hipótesis."""
    winner_title: str = Field(description="Título de la hipótesis declarada ganadora del debate")
    loser_title: str = Field(description="Título de la hipótesis vencida o descartada")
    elo_rating: float = Field(description="Rating Elo recalculado para la hipótesis ganadora tras el debate")
    critique_summary: str = Field(description="Resumen de las refutaciones socráticas del Reflection Agent")
    alternative_pathways: List[str] = Field(default=[], description="Líneas de investigación alternativas propuestas ante vacíos de datos")

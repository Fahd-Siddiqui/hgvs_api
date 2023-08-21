from typing import List, Optional

import pydantic


class AnnotatedTranscript(pydantic.BaseModel):
    transcript: str
    gene: Optional[str] = None
    hgvs_c: Optional[str] = None
    hgvs_p: Optional[str] = None
    error: Optional[str] = None


class Variant(pydantic.BaseModel):
    chromosome: Optional[str]
    accession: str
    position: int
    position_end: int
    ref_allele: str
    alt_allele: str

    variant_type: str
    hgvs_g: str
    transcripts: List[AnnotatedTranscript]

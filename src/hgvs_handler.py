import functools
import logging
from enum import Enum
from typing import Dict, List, Optional

import hgvs.assemblymapper
import hgvs.dataproviders.uta
import hgvs.parser
from hgvs.exceptions import HGVSUsageError
from hgvs.sequencevariant import SequenceVariant

from src.models import AnnotatedTranscript, Variant


class Assembly(Enum):
    GRCh38 = "GRCh38"
    GRCh37 = "GRCh37"

    @classmethod
    def _missing_(cls, name: str) -> Optional["Assembly"]:  # type: ignore[override]
        found = next(
            (member for member in cls if member.name.lower() == name.lower()),
            None,
        )

        return found


class HgvsHandler:
    logger = logging.getLogger(__name__)

    @functools.cached_property
    def hgvs_parser(self) -> hgvs.parser.Parser:
        return hgvs.parser.Parser()

    @functools.cached_property
    def assembly_mapper(self) -> Dict[Assembly, hgvs.assemblymapper.AssemblyMapper]:
        hgvs_data_provider = hgvs.dataproviders.uta.connect()
        assembly_mapper = {
            assembly: hgvs.assemblymapper.AssemblyMapper(
                hgvs_data_provider,
                assembly_name=assembly.value,
                alt_aln_method="splign",
                replace_reference=True,
                add_gene_symbol=False,
            )
            for assembly in Assembly
        }

        return assembly_mapper

    @functools.cached_property
    def data_version(self) -> str:
        return self.assembly_mapper[Assembly.GRCh38].hdp.data_version()

    @staticmethod
    def normalize(assembly_mapper: hgvs.assemblymapper.AssemblyMapper, variant: SequenceVariant) -> SequenceVariant:
        return assembly_mapper._norm.normalize(variant)

    def get_annotation_from_hgvs_g(self, hgvs_g: str, assembly: Assembly) -> Variant:
        variant_hgvs_g: SequenceVariant = self.hgvs_parser.parse(hgvs_g)
        assembly_mapper = self.assembly_mapper[assembly]
        variant_hgvs_g = self.normalize(assembly_mapper, variant_hgvs_g)
        transcripts = assembly_mapper.relevant_transcripts(variant_hgvs_g)

        accession = variant_hgvs_g.ac
        chromosome = assembly_mapper.hdp.get_assembly_map(assembly_mapper.assembly_name).get(accession)

        simple_position = variant_hgvs_g.posedit
        annotated_transcripts = self._get_annotated_transcripts(transcripts, assembly_mapper, variant_hgvs_g)

        alt_allele = None
        if hasattr(simple_position.edit, "alt"):
            alt_allele = simple_position.edit.alt

        variant = Variant(
            chromosome=chromosome,
            accession=accession,
            position=simple_position.pos.start.base,
            position_end=simple_position.pos.end.base,
            ref_allele=simple_position.edit.ref,
            alt_allele=alt_allele,
            hgvs_g=str(variant_hgvs_g),
            variant_type=simple_position.edit.type,
            transcripts=annotated_transcripts,
        )

        return variant

    @staticmethod
    def _get_annotated_transcripts(
        transcripts: List[str], assembly_mapper: hgvs.assemblymapper.AssemblyMapper, variant_hgvs_g: SequenceVariant
    ) -> List:
        annotated_transcripts = []

        for transcript in transcripts:
            try:
                variant_hgvs_c = assembly_mapper.g_to_c(variant_hgvs_g, transcript)
                variant_hgvs_p = assembly_mapper.c_to_p(variant_hgvs_c)
                gene = variant_hgvs_p.gene or variant_hgvs_c.gene or variant_hgvs_g.gene
                annotated_transcripts.append(
                    AnnotatedTranscript(
                        transcript=transcript,
                        hgvs_c=str(variant_hgvs_c),
                        hgvs_p=str(variant_hgvs_p),
                        gene=gene,
                    )
                )
            except HGVSUsageError as e:
                logging.getLogger(__name__).error(f"Exception: {e}")
                annotated_transcripts.append(AnnotatedTranscript(transcript=transcript, error=str(e)))

        return annotated_transcripts

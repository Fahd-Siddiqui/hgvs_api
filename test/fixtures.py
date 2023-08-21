import json
from pathlib import Path
from unittest.mock import MagicMock


def load_test_data():
    test_data_path = (Path(__file__) / ".." / "test_data.json").resolve()
    with open(test_data_path, "r") as file:
        return json.load(file)


class AssemblyMapperFixture:

    def __init__(self):
        self.test_data = load_test_data()
        self.mocked_annotated_transcripts = self.test_data["transcripts"]
        self.assembly_name = "GRCh38"

    def g_to_c(self, variant_hgvs_g, transcript: str):
        variant_hgvs = next(
            (
                annotated_transcript["hgvs_c"]
                for annotated_transcript in self.mocked_annotated_transcripts
                if annotated_transcript["transcript"] == transcript
            )
        )

        variant_hgvs_c = MagicMock()
        variant_hgvs_c.__str__ = lambda _: variant_hgvs
        variant_hgvs_c.gene = None
        return variant_hgvs_c

    def relevant_transcripts(self, *args, **kwargs):
        relevant_transcripts = [
            annotated_transcript["transcript"]
            for annotated_transcript in self.mocked_annotated_transcripts
        ]
        return relevant_transcripts

    def c_to_p(self, variant_hgvs_c, *args, **kwargs):
        variant_hgvs = next(
            (
                annotated_transcript["hgvs_p"]
                for annotated_transcript in self.mocked_annotated_transcripts
                if annotated_transcript["hgvs_c"] == str(variant_hgvs_c)
            )
        )
        variant_hgvs_p = MagicMock()
        variant_hgvs_p.__str__ = lambda _: variant_hgvs
        variant_hgvs_p.gene = None
        return variant_hgvs_p

    @property
    def hdp(self):
        hdp = MagicMock()
        hdp.get_assembly_map = lambda *args: {
            self.test_data["accession"]: self.test_data["chromosome"]
        }
        return hdp


class HgvsParserFixture:
    def __init__(self):
        self.test_data = load_test_data()

    def parse(self, hgvs_g):
        simple_position = MagicMock()
        simple_position.pos.start.base = self.test_data["position"]
        simple_position.pos.end.base = self.test_data["position_end"]
        simple_position.edit.ref = self.test_data["ref_allele"]
        simple_position.edit.alt = self.test_data["alt_allele"]
        simple_position.edit.type = self.test_data["variant_type"]

        variant_hgvs_g = MagicMock()
        variant_hgvs_g.__str__ = lambda _: self.test_data["hgvs_g"]
        variant_hgvs_g.ac = self.test_data["accession"]
        variant_hgvs_g.posedit = simple_position
        variant_hgvs_g.gene = None

        return variant_hgvs_g

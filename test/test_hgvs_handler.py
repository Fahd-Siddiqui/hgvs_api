import unittest
from test.fixtures import AssemblyMapperFixture, HgvsParserFixture, load_test_data
from unittest.mock import patch

from src.hgvs_handler import Assembly, HgvsHandler
from src.utils import Utils


@patch.object(HgvsHandler, "assembly_mapper", {Assembly.GRCh38: AssemblyMapperFixture()})
@patch.object(HgvsHandler, "hgvs_parser", HgvsParserFixture())
class TestHgvs(unittest.TestCase):
    def test_get_annotation_from(self):
        self.maxDiff = None
        test_data = load_test_data()
        test_data.pop("vid")

        hgvs_g = Utils.vcf_to_hgvs_g(
            accession=test_data["accession"],
            position=test_data["position"],
            ref_allele=test_data["ref_allele"],
            alt_allele=test_data["alt_allele"],
        )
        hgvs_handler = HgvsHandler()
        result = hgvs_handler.get_annotation_from_hgvs_g(hgvs_g, Assembly("GRCH38"))

        self.assertDictEqual(result.model_dump(exclude_none=True, exclude_unset=True), test_data)

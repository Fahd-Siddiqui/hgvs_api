import pytest

from src.hgvs_handler import Assembly
from src.utils import ChromosomeUtils, Utils


class TestUtils:
    @pytest.mark.parametrize(
        "accession, position, position_end, ref_allele, alt_allele, expected_hgvs_g",
        [
            (
                    "NC_000009.11", 5066679, 5066679, "ATGGATTTTGCCATTAGTAAACTGAAGA", "A",
                    "NC_000009.11:g.5066679_5066679delATGGATTTTGCCATTAGTAAACTGAAGAinsA"
            ),
            (
                    "NC_000009.11", 5066679, None, "ATGGATTTTGCCATTAGTAAACTGAAGA", "A",
                    "NC_000009.11:g.5066679_5066706delATGGATTTTGCCATTAGTAAACTGAAGAinsA"
            )
        ]
    )
    def test_vcf_to_hgvs_g(self, accession, position, position_end, ref_allele, alt_allele, expected_hgvs_g):
        hgvs_g = Utils.vcf_to_hgvs_g(
            accession=accession,
            position=position,
            position_end=position_end,
            ref_allele=ref_allele,
            alt_allele=alt_allele
        )

        assert hgvs_g == expected_hgvs_g


class TestChromosomeUtils:
    @pytest.mark.parametrize(
        "chromosome, expected_accession",
        [
            ("1", "NC_000001.11"),
            ("chr1", "NC_000001.11"),
            ("ChR1", "NC_000001.11"),
            ("NC_000001", "NC_000001.11"),

            ("MT", "NC_012920.1"),
            ("chrM", "NC_012920.1"),
            ("Y", "NC_000024.10"),
            ("chrY", "NC_000024.10"),

        ]
    )
    def test_get_accession(self, chromosome, expected_accession):
        assembly_map = {
            "NC_000001.11": "1",
            "NC_000024.10": "Y",
            "NC_012920.1": "MT"
        }
        assert ChromosomeUtils.get_accession(chromosome, assembly_map) == expected_accession


class TestAssembly:
    @pytest.mark.parametrize(
        "assembly, expected_assembly",
        [
            ("GRCh38", "GRCh38"), ("grCh38", "GRCh38"),
            ("GRCh37", "GRCh37"), ("GrCh37", "GRCh37"),
            ("GRCh39", None), ("T2T", None),
        ]
    )
    def test_assembly(self, assembly, expected_assembly):
        if expected_assembly:
            assert Assembly(assembly).value == expected_assembly
            return

        with pytest.raises(ValueError):
            Assembly(assembly)


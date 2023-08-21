from typing import Dict, Optional


class Utils:
    @staticmethod
    def vcf_to_hgvs_g(
        accession: str,
        position: int,
        ref_allele: str,
        alt_allele: str,
        position_end: Optional[int] = None,
    ) -> str:
        if not position_end:
            position_end = position + len(ref_allele) - 1

        return (
            f"{accession}:"
            f"g.{position}"
            f"_"
            f"{position_end}"
            f"del"
            f"{ref_allele.upper()}"
            f"ins"
            f"{alt_allele.upper()}"
        )


class ChromosomeUtils:
    @classmethod
    def get_accession(cls, chromosome: str, assembly_map: Dict[str, str]):
        accession_map = cls._get_accession_map(assembly_map)
        fixed_chromosome = cls.__fix_chr(chromosome)
        fixed_chromosome = cls.__remove_version(fixed_chromosome)
        return accession_map[fixed_chromosome]

    @staticmethod
    def __remove_version(accession: str):
        return accession.split(".")[0]

    @staticmethod
    def __fix_chr(chromosome: str) -> str:
        if chromosome[0:3].lower() == "chr":
            chromosome = f"chr{chromosome[3:]}"

        return chromosome

    @classmethod
    def _get_accession_map(cls, assembly_map: Dict[str, str]) -> Dict[str, str]:
        accession_map = {}

        for key, value in assembly_map.items():
            acc_without_version = cls.__remove_version(key)
            chr_value = f"chr{value}"
            if chr_value == "chrMT":
                chr_value = "chrM"

            accession_map[value] = key
            accession_map[chr_value] = key
            accession_map[acc_without_version] = key

        return accession_map

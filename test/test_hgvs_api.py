from test.fixtures import AssemblyMapperFixture, HgvsParserFixture, load_test_data
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.hgvs_api import app
from src.hgvs_handler import Assembly, HgvsHandler

client = TestClient(app)


@patch.object(HgvsHandler, "assembly_mapper", {Assembly.GRCh38: AssemblyMapperFixture()})
@patch.object(HgvsHandler, "hgvs_parser", HgvsParserFixture())
class TestApi:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["result"] == {
            "message": "Connection successful. "
                       "Navigate to /docs to find out how to use this API."
        }

    def test_get_hgvsg_annotation(self):
        query = "assembly=GRCh38&" \
                "hgvs_g=NC_000009.11%3Ag.5066679_5066706delinsA"
        response = client.get(f"/hgvsg/?{query}")
        assert response.status_code == 200
        assert response.json()["result"] == load_test_data()

    def test_get_vcf_annotation(self):
        query = "assembly=GRCh38&" \
                "chromosome=NC_000009.11&" \
                "position=5066679&" \
                "ref_allele=ATGGATTTTGCCATTAGTAAACTGAAGA&" \
                "alt_allele=A"
        response = client.get(f"/vcf/?{query}")
        assert response.status_code == 200
        assert response.json()["result"] == load_test_data()

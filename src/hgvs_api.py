import os
import time
from typing import Any, Dict

import pydantic
from fastapi import FastAPI

from src.hgvs_handler import Assembly, HgvsHandler
from src.utils import ChromosomeUtils, Utils

app = FastAPI(title="HGVS API")

hgvs_handler = HgvsHandler()


class MessageResponse(pydantic.BaseModel):
    message: str


def response_template(result: pydantic.BaseModel) -> Dict[str, Any]:
    response: Dict[str, Any] = {
        "timestamp": int(time.time()),
        "data_version": hgvs_handler.data_version,
        "local_uta": bool(os.environ.get("UTA_DB_URL")),
    }

    if result:
        response["result"] = result.model_dump(exclude_none=True, exclude_unset=True)

    return response


@app.get("/")
async def root():
    message = MessageResponse(message="Connection successful. " "Navigate to /docs to find out how to use this API.")
    return response_template(message)


@app.get("/vcf/")
async def get_vcf_annotation(
    assembly: Assembly,
    chromosome: str,
    position: int,
    ref_allele: str,
    alt_allele: str,
):
    assembly_map = hgvs_handler.assembly_mapper[assembly].hdp.get_assembly_map(assembly.value)
    accession = ChromosomeUtils.get_accession(chromosome, assembly_map)

    hgvs_g = Utils.vcf_to_hgvs_g(
        accession=accession,
        position=position,
        ref_allele=ref_allele,
        alt_allele=alt_allele,
    )

    result = hgvs_handler.get_annotation_from_hgvs_g(hgvs_g, assembly)
    return response_template(result)


@app.get("/hgvsg/")
async def get_hgvs_annotation(assembly: Assembly, hgvs_g: str):
    result = hgvs_handler.get_annotation_from_hgvs_g(hgvs_g, assembly)
    return response_template(result)

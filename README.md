# BIOCOMMONS HGVS API

## Docker Quick Start

```shell
make docker
```

Run

```
docker compose up
```

Wait for the data to download. After which, open the browser and point
to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Database Backend

Edit the [docker-compose.yaml](docker-compose.yml) file and comment out the following:

`UTA_DB_URL=postgresql://anonymous@uta_db:5432/uta/uta_20210129`

to use biocommons web database instead of the included docker database.

## Non-Docker

Note non-Docker relies on Biocommons database backend and might be slow to annotate

To prepare venv and install requirements

```shell
make install
``` 

Start the application

```shell
python -m uvicorn src.hgvs_api:app --reload --port 8001
```

Open the browser and point to [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## Example:

### GET Request

[http://127.0.0.1:8000/vcf/?assembly=GRCh38&chromosome=9&position=5066679&ref_allele=ATGGATTTTGCCATTAGTAAACTGAAGA&alt_allele=A](http://127.0.0.1:8000/vcf/?assembly=GRCh38&chromosome=9&position=5066679&ref_allele=ATGGATTTTGCCATTAGTAAACTGAAGA&alt_allele=A
)

### Results:

```json
{
  "timestamp": 1692410793,
  "data_version": "uta_20210129",
  "local_uta": true,
  "result": {
    "chromosome": "9",
    "accession": "NC_000009.12",
    "position": 5066679,
    "position_end": 5066706,
    "ref_allele": "ATGGATTTTGCCATTAGTAAACTGAAGA",
    "alt_allele": "A",
    "variant_type": "delins",
    "hgvs_g": "NC_000009.12:g.5066679_5066706delinsA",
    "transcripts": [
      {
        "transcript": "NM_001322199.2",
        "hgvs_c": "NM_001322199.2:c.2_28del",
        "hgvs_p": "NP_001309128.1:p.Met1?"
      },
      {
        "transcript": "NM_001322194.1",
        "hgvs_c": "NM_001322194.1:c.1217_1243del",
        "hgvs_p": "NP_001309123.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_001322198.1",
        "hgvs_c": "NM_001322198.1:c.2_28del",
        "hgvs_p": "NP_001309127.1:p.Met1?"
      },
      {
        "transcript": "NM_001322204.2",
        "hgvs_c": "NM_001322204.2:c.770_796del",
        "hgvs_p": "NP_001309133.1:p.(Met257_Lys265del)"
      },
      {
        "transcript": "NM_001322195.1",
        "hgvs_c": "NM_001322195.1:c.1217_1243del",
        "hgvs_p": "NP_001309124.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_004972.3",
        "hgvs_c": "NM_004972.3:c.1217_1243del",
        "hgvs_p": "NP_004963.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_001322196.1",
        "hgvs_c": "NM_001322196.1:c.1217_1243del",
        "hgvs_p": "NP_001309125.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_001322204.1",
        "hgvs_c": "NM_001322204.1:c.770_796del",
        "hgvs_p": "NP_001309133.1:p.(Met257_Lys265del)"
      },
      {
        "transcript": "NM_004972.4",
        "hgvs_c": "NM_004972.4:c.1217_1243del",
        "hgvs_p": "NP_004963.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_001322194.2",
        "hgvs_c": "NM_001322194.2:c.1217_1243del",
        "hgvs_p": "NP_001309123.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_001322195.2",
        "hgvs_c": "NM_001322195.2:c.1217_1243del",
        "hgvs_p": "NP_001309124.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NM_001322199.1",
        "hgvs_c": "NM_001322199.1:c.2_28del",
        "hgvs_p": "NP_001309128.1:p.Met1?"
      },
      {
        "transcript": "NM_001322196.2",
        "hgvs_c": "NM_001322196.2:c.1217_1243del",
        "hgvs_p": "NP_001309125.1:p.(Met406_Lys414del)"
      },
      {
        "transcript": "NR_169764.1",
        "error": "CDS is undefined for NR_169764.1; cannot map to c. coordinate (non-coding transcript?)"
      },
      {
        "transcript": "NR_169763.1",
        "error": "CDS is undefined for NR_169763.1; cannot map to c. coordinate (non-coding transcript?)"
      },
      {
        "transcript": "NM_001322198.2",
        "hgvs_c": "NM_001322198.2:c.2_28del",
        "hgvs_p": "NP_001309127.1:p.Met1?"
      }
    ]
  }
}
```

## Development

Developed using

1. Python 3.10
2. Fast Api
3. Pydantic

Ensure linting and tests pass:

### local environment

```shell
make install
``` 

### Test

```shell
make requirements-test
make lint
make test
```

## Attributions

Thanks to Biocommons :)

[https://github.com/biocommons/hgvs](https://github.com/biocommons/hgvs)
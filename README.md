# template.python.package

Template to help quickly make python packages

TODO: Add Todo generator for root of repo
TODO: Add licensee checker

```bash
export $(grep -v '^#' .env | xargs)
```

```bash
python3 src/hungovercoders_workflow_doc_gen/cli.py --org griff182uk0203 --project hungovercoders --pat D0OnwzrQcRMaSiiHytO7c4bhXCf2ykvi6NAMBm2YTrfGXpcLI8HPJQQJ99BFACAAAAAAAAAAAAASAZDO239r --output okr_report.md

python3 src/hungovercoders_workflow_doc_gen/cli.py --org griff182uk0203 --project hungovercoders --pat $AZURE_DEVOPS_PAT_TOKEN --output okr_report.md --format markdown

python3 src/hungovercoders_workflow_doc_gen/cli.py --org griff182uk0203 --project hungovercoders --pat $AZURE_DEVOPS_PAT_TOKEN --output okr_raw.json --format raw-json


python3 -m logging -c "import logging; logging.basicConfig(level=logging.DEBUG)" src/hungovercoders_workflow_doc_gen/cli.py --org griff182uk0203 --project hungovercoders --pat $AZURE_DEVOPS_PAT_TOKEN --output okr_raw.json --format raw-json

```

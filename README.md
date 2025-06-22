# workflow.doc.generator

```bash
export $(grep -v '^#' .env | xargs)
```

```bash
pip install -e .
```

## Json

```bash
workflow-doc-gen json --input tests/example_input/okr_summary.example.json --format markdown

workflow-doc-gen json --input tests/example_input/okr_summary.example.json --format doc

workflow-doc-gen json --input tests/example_input/okr_summary.example.json --format pdf
```

## Azure Devops

```bash
workflow-doc-gen azure_devops --org griff182uk0203 --project hungovercoders --pat $AZURE_DEVOPS_PAT_TOKEN --format markdown

workflow-doc-gen azure_devops --org griff182uk0203 --project hungovercoders --pat $AZURE_DEVOPS_PAT_TOKEN --format doc

workflow-doc-gen azure_devops --org griff182uk0203 --project hungovercoders --pat $AZURE_DEVOPS_PAT_TOKEN --format pdf
```

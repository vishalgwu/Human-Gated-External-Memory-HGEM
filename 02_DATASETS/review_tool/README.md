# HGEM Constraint Review Tool

This local web app helps review generated constraint JSON files against the matching pilot/main problem record.

Run from the repository root:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\review_tool\app.py
```

Then open:

```text
http://127.0.0.1:8765
```

What it can do:

- list pilot, main, or all constraint files;
- filter by benchmark and review status;
- load a constraint JSON file;
- show the matching problem text and solution text from the split files;
- show linked draft adversarial claims;
- edit constraints, reviewer, date, confidence, and review status;
- save the JSON back to the same constraint folder;
- preview an uploaded constraint JSON and cross-check it against the local split record.

The tool does not commit anything to Git. Generated constraint files are local-only because `02_DATASETS/constraints/**` is ignored by `.gitignore`.

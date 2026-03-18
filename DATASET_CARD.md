---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- algoshift
- computational-economics
- labor-economics
- emerging-terminology
pretty_name: Algoshift Economics Dataset
size_categories:
- n<1K
---

# Algoshift Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Algoshift` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Labor Economics research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique worker-period id
- `week`: Synthetic week index
- `demand_uncertainty`: Demand prediction uncertainty
- `algorithmic_control`: Algorithmic control intensity
- `shift_variability`: Week-to-week shift volatility
- `worker_autonomy`: Worker schedule autonomy
- `schedule_notice_hours`: Average advance notice for shifts
- `income_volatility`: Within-worker earnings volatility
- `turnover_risk`: Predicted worker churn risk
- `algoshift_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Algoshift applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{algoshift2026,
title={{Algoshift Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}

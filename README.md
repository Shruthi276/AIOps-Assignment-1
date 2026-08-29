# AIOps — Module 1 Assignment: Experiment Management & Reproducibility


This repository contains the deliverables, code, and documentation for **Question 1** (Conceptual: Technical Debt Diagnosis), **Question 2** (Applied: MLflow Experiment Comparison), and **Question 3** (Applied: DVC Data Versioning & Rollback).



## Table of Contents
1. [AI Disclosure & Code of Conduct](#-ai-disclosure--code-of-conduct)
2. [Repository Structure & Navigation](#-repository-structure--navigation)
3. [Environment Setup & Installation](#-environment-setup--installation)
4. [Question 1: Technical Debt Diagnosis](#-question-1-technical-debt-diagnosis)
5. [Question 2: Applied MLflow Experiment Comparison](#-question-2-applied-mlflow-experiment-comparison)
6. [Question 3: Applied DVC Data Versioning & Rollback](#-question-3-applied-dvc-data-versioning--rollback)
7. [Question 4: Capstone Drill (Status)](#-question-4-capstone-drill-status)

---

##  AI Disclosure & Code of Conduct

In accordance with the **Code of Conduct for Fair and Responsible Use of AI in AIOps Coursework**, all AI assistance utilized in this repository is disclosed below:

- **AI Tools Used:** Claude
- **Usage Details:**
  - **Question 2:** Used Claude to clarify which hyperparameters are relevant for scikit-learn's `MLPClassifier` (e.g., `hidden_layer_sizes`, `learning_rate_init`, `batch_size`, `max_iter`, `solver`, `activation`) and to verify syntax for MLflow logging calls (`mlflow.log_param` and `mlflow.log_metric`).
  - **Question 3:** Used Claude for step-by-step guidance on creating an AWS S3 bucket and configuring/authenticating it as a remote storage backend for DVC (`dvc remote add -d myremote s3://...`).
- **Impact on Final Submission:** The AI served as a syntax reference and pair-programming assistant to streamline standard boilerplate and CLI configuration. All model training, experiment logging, data versioning commits, and rollbacks were executed directly and verified manually.


---

##  Repository Structure & Navigation

| Deliverable / Question | File / Path | Description |
| :--- | :--- | :--- |
| **Q1: Technical Debt Diagnosis** | [`question_1.pdf`](./question_1.pdf) | 1-page write-up diagnosing 3 technical debt scenarios and proposing specific mitigations. |
| **Q2: MLflow Run Comparison Table** | [`question_2/mlflow_comparison_table.png`](./question_2/mlflow_comparison_table.png) | Screenshot of the MLflow UI comparison table displaying all 6 MLP runs on MNIST. |
| **Q2: Written Analysis** | [`question_2/written_analysis_Q2.pdf`](./question_2/written_analysis_Q2.pdf) | Short written analysis (150–250 words) evaluating best runs, overfitting, and hyperparameter impact. |
| **Q2: MLflow Logging Code** | [`question_2/log_param_metric_code.py`](./question_2/log_param_metric_code.py) | Python snippet containing exact `mlflow.log_param` and `mlflow.log_metric` statements. |
| **Q3: DVC Tracking Files** | [`question_3/file_list.csv.dvc`](./question_3/file_list.csv.dvc), [`question_3/data.dvc`](./question_3/data.dvc) | DVC metadata tracking dataset versions. |
| **Q3: Dataset File List** | [`question_3/file_list.csv`](./question_3/file_list.csv) | Tracked dataset CSV containing file records (v1 = 1801 lines, v2 = 2801 lines). |
| **Q3: Rollback Proof** | [`question_3/rollback_ss.png`](./question_3/rollback_ss.png) | Terminal screenshot/output demonstrating rollback to v1 via `git checkout` + `dvc checkout` and row count validation. |
| **DVC Configuration** | [`.dvc/config`](./.dvc/config) | Remote storage configuration pointing to S3. |

---

##  Environment Setup & Installation

### 1. Prerequisites
- Python 3.9+
- Git
- DVC (with S3 support: `dvc[s3]`)

### 2. Clone the Repository
```bash
git clone https://github.com/Shruthi276/AIOps-Assignment-1.git
cd AIOps-Assignment-1
```

### 3. Create and Activate Virtual Environment
```bash
# Using venv
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install mlflow scikit-learn pandas numpy "dvc[s3]"
```

---

##  Question 1: Technical Debt Diagnosis

- **File Location:** [`question_1.pdf`](./question_1.pdf)
- **Topics Covered:**
  - **Scenario (a):** Hidden feedback loop / undeclared upstream feature dependencies impacting the "favorite restaurants" model when "estimated delivery time" rounding logic changed.
  - **Scenario (b):** Hidden consumer / data debt (marketing dashboard silently reading raw model output table without a formalized data contract or API boundary).
  - **Scenario (c):** Pipeline jungle / glue code technical debt (14 undocumented shell scripts without an orchestration framework).
  - **Mitigation:** Comprehensive mitigation plan detailing concrete tooling (e.g., Apache Airflow / Prefect for pipeline orchestration, formal schema validation, feature stores, and versioned APIs).

---

##  Question 2: Applied MLflow Experiment Comparison

- **Directory:** [`question_2/`](./question_2/)
- **Summary:**
  - Migrated the baseline classifier from `RandomForest` to a Multi-Layer Perceptron (`MLPClassifier`) and trained on the **MNIST** dataset.
  - Conducted **six systematic experiment runs** varying key hyperparameters:
    - **Hidden layer sizes:** e.g., `(50,)`, `(100,)`, `(100, 50)`
    - **Initial learning rate (`learning_rate_init`):** e.g., `0.0005`, `0.001`, `0.01`
    - **Batch size:** e.g., `32`, `64`, `128`
    - **Max iterations (`max_iter`):** e.g., `20`, `30`, `50`
- **Logged Parameters & Metrics:**
  - Parameters: `hidden_layer_sizes`, `learning_rate_init`, `batch_size`, `max_iter`, `solver`, `activation`
  - Metrics: `train_loss`, `val_loss`, `val_accuracy`, `val_f1_macro`
- **Source Code Snippet:** View [`question_2/log_param_metric_code.py`](./question_2/log_param_metric_code.py)
- **Comparison Table:** View [`question_2/mlflow_comparison_table.png`](./question_2/mlflow_comparison_table.png)
- **Written Analysis:** View [`question_2/written_analysis_Q2.pdf`](./question_2/written_analysis_Q2.pdf)

### How to Launch the MLflow Tracking Server
To view the experiment runs and compare results via the MLflow UI, start the tracking server using:
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```
Open `http://localhost:5000` in your web browser to interact with the run comparison table and metric charts.

---

## Question 3: Applied DVC Data Versioning & Rollback

- **Directory:** [`question_3/`](./question_3/)
- **Summary:**
  - **v1 Dataset (Tag: `q3-v1`):** Created `file_list.csv` from `data.zip` containing **1800 rows + 1 header row (1801 lines total)**. Tracked with DVC and tagged commit as `q3-v1`.
  - **Remote Setup:** Configured an S3 remote backend (`s3://q4-capstone/dvcstore`) and pushed v1 data with `dvc push`.
  - **v2 Update (Tag: `q3-v2`):** Added new rows from `new_labels.zip` to update `file_list.csv` to **2800 rows + 1 header row (2801 lines total)**. Re-tracked with `dvc add`, committed v2 to Git, and tagged as `q3-v2`.
  - **Rollback Demonstration:** Checked out tag `q3-v1` with `git checkout q3-v1` followed by `dvc checkout`, and verified that the row count returned to exactly 1801 lines.

### Reproducing the DVC Rollback

#### 1. Check current v2 state (2801 lines):
```bash
wc -l question_3/file_list.csv
# Expected output: 2801 question_3/file_list.csv
```

#### 2. Roll back to v1 using tag `q3-v1`:
```bash
# Switch Git state to tag q3-v1
git checkout q3-v1

# Restore the v1 dataset from DVC
dvc checkout
```

#### 3. Verify row count matches v1 (1801 lines):
```bash
wc -l question_3/file_list.csv
# Expected output: 1801 question_3/file_list.csv
```

#### 4. Switch back to v2 using tag `q3-v2` (or `main`):
```bash
git checkout q3-v2
dvc checkout
```

- **Rollback Verification Screenshot:** View [`question_3/rollback_ss.png`](./question_3/rollback_ss.png)

---

##  Question 4: Capstone Drill (Status)

> [!NOTE]
> **Question 4 (End-to-End Reproducibility Protocol & Partner Drill)** will be added and documented in this section upon completion of the collaborative experiment with the assigned partner.
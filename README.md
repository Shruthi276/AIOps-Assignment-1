# AIOps — Module 1 Assignment: Experiment Management & Reproducibility

This repository contains the deliverables, code, and documentation for **Question 1** (Conceptual: Technical Debt Diagnosis), **Question 2** (Applied: MLflow Experiment Comparison), **Question 3** (Applied: DVC Data Versioning & Rollback), and links to the dedicated repository for **Question 4** (Capstone: End-to-End Reproducibility Drill).

---

##  Table of Contents
1. [Repository Structure & Navigation](#-repository-structure--navigation)
2. [Environment Setup & Installation](#-environment-setup--installation)
3. [Question 1: Technical Debt Diagnosis](#-question-1-technical-debt-diagnosis)
4. [Question 2: Applied MLflow Experiment Comparison](#-question-2-applied-mlflow-experiment-comparison)
5. [Question 3: Applied DVC Data Versioning & Rollback](#-question-3-applied-dvc-data-versioning--rollback)
6. [Question 4: Capstone — End-to-End Reproducibility Drill](#-question-4-capstone--end-to-end-reproducibility-drill)
7. [AI Disclosure & Code of Conduct](#-ai-disclosure--code-of-conduct)

---

##  Repository Structure & Navigation

| Deliverable / Question | File / Path | Description |
| :--- | :--- | :--- |
| **Q1 & Q2: Written Report** | [`report.pdf`](./report.pdf) | 1-page write-up covering Q1 Technical Debt Diagnosis and Q2 MLflow Experiment Analysis. |
| **Q2: MLflow Run Comparison Table** | [`question_2/mlflow_comparison_table.png`](./question_2/mlflow_comparison_table.png) | Screenshot of the MLflow UI comparison table displaying all 6 MLP runs on MNIST. |
| **Q2: MLflow Logging Code** | [`question_2/log_param_metric_code.py`](./question_2/log_param_metric_code.py) | Python snippet containing exact `mlflow.log_param` and `mlflow.log_metric` statements. |
| **Q3: DVC Tracking Files** | [`question_3/file_list.csv.dvc`](./question_3/file_list.csv.dvc), [`question_3/data.dvc`](./question_3/data.dvc) | DVC metadata tracking dataset versions. |
| **Q3: Dataset File List** | [`question_3/file_list.csv`](./question_3/file_list.csv) | Tracked dataset CSV containing file records (v1 = 1801 lines, v2 = 2801 lines). |
| **Q3: Rollback Proof** | [`question_3/rollback_ss.png`](./question_3/rollback_ss.png) | Terminal screenshot/output demonstrating rollback to v1 via `git checkout` + `dvc checkout` and row count validation. |
| **Q4: Capstone Drill Repository** | [reproducibility_capstone](https://github.com/Shruthi276/reproducibility_capstone) | Dedicated  repository containing the full end-to-end reproducibility protocol. |
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

- **File Location:** Included in [`report.pdf`](./report.pdf) (Question 1)
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
- **Written Analysis:** Included in [`report.pdf`](./report.pdf) (Question 2: Written Analysis)

### How to Launch the MLflow Tracking Server
To view the experiment runs and compare results via the MLflow UI, start the tracking server using:
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```
Open `http://localhost:5000` in your web browser to interact with the run comparison table and metric charts.

---

##  Question 3: Applied DVC Data Versioning & Rollback

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

##  Question 4: Capstone — End-to-End Reproducibility Drill

The complete implementation and collaborative reproducibility protocol for Question 4 is hosted in a dedicated repository:

🔗 **GitHub Repository:** [https://github.com/Shruthi276/reproducibility_capstone](https://github.com/Shruthi276/reproducibility_capstone)

### Protocol Overview & Role (Partner A):
1. **Model Training & MLflow Logging:** Trained the model, logged all parameters, metrics, random seed, `git_commit` tag, and artifacts to MLflow.
2. **Data Versioning:** Versioned the dataset using DVC and committed code changes and `.dvc` metadata files atomically in the same Git commit.
3. **Model Registry:** Registered the trained model in the MLflow Model Registry and transitioned the model stage to **"Staging"**.
4. **Partner Handoff & Independent Reproduction:** Provided the repository to Partner B to reproduce the complete pipeline independently using only:
   ```bash
   git clone https://github.com/Shruthi276/reproducibility_capstone.git
   git checkout <commit>
   dvc checkout
   # Environment activation & script re-run
   ```
5. **Verification & Metric Matching:** Partner B verified reproduced metrics against logged results within stated tolerance and documented notes directly in the MLflow run.

*For complete reproduction instructions, commit history, and logs, please visit the [reproducibility_capstone](https://github.com/Shruthi276/reproducibility_capstone) repository.*

---

##  AI Disclosure & Code of Conduct

In accordance with the **Code of Conduct for Fair and Responsible Use of AI in AIOps Coursework**, all AI assistance utilized across this assignment is disclosed below:

- **AI Tools Used:** Claude
- **Usage Details:**
  - **Question 2:** Used Claude to clarify which hyperparameters are relevant for scikit-learn's `MLPClassifier` (e.g., `hidden_layer_sizes`, `learning_rate_init`, `batch_size`, `max_iter`, `solver`, `activation`) and to verify syntax for MLflow logging calls (`mlflow.log_param` and `mlflow.log_metric`).
  - **Question 3:** Used Claude for steps for  creating an AWS S3 bucket and configuring/authenticating it as a remote storage backend for DVC (`dvc remote add -d myremote s3://...`).
  - **Question 4 (Capstone):** i was Partner A and used Claude to set up the boilerplate project file structure for the  repository, as well as for troubleshoot and fix errors encountered during the  reproduction workflow.
- **Impact on Final Submission:** The AI was utilized strictly as a learning assistant, boilerplate generator, and debugging tool. All model training runs, metric evaluations, DVC remote pushes, Git tagging, and reproduction drills were independently executed, validated, and verified.

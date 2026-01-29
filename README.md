# 🚀 GitHub Clone on Cloud Run with GCS FUSE

Welcome to the **GitHub Clone** project! This is a high-performance, scalable file management system mimicking GitHub's core repository storage features, built with **Python FastAPI** and deployed on **Google Cloud Run**.

What makes this project "epic" is its storage layer: it leverages **Google Cloud Storage (GCS) FUSE** to mount an object storage bucket as a local file system, allowing the application to interact with cloud storage using standard file I/O operations.

## 🏗 Architecture

- **Backend**: Python FastAPI (High performance, easy to use)
- **Server**: Gunicorn with Uvicorn workers
- **Storage**: Google Cloud Storage (GCS) mounted via `gcsfuse`
- **Deployment**: Google Cloud Run (Serverless container platform)

### How it works

1. The application starts up.
2. The `entrypoint.sh` script mounts your specified GCS bucket to `/mnt/gcs` (or your configured mount point).
3. FastAPI reads and writes to `/mnt/gcs` as if it were a local disk.
4. Changes are immediately reflected in your GCS bucket.
5. Cloud Run scales the application instance down to zero when not in use, but the data persists in GCS.

## 🛠 Local Development

### Prerequisites

- Python 3.10+
- Google Cloud SDK (gcloud) installed
- A GCS Bucket created

### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-dir>
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Locally (Mocking GCS):**
   Since you might not have `gcsfuse` locally on Mac/Windows easily, the app will fallback to using a local directory.

   ```bash
   export BUCKET_NAME="" # Empty to skip mounting
   export MOUNT_POINT="./local_storage"
   mkdir local_storage
   uvicorn app.main:app --reload
   ```

   Visit `http://localhost:8000/docs` to see the API Swagger UI.

## ☁️ Deployment to Google Cloud Run

### 1. Enable APIs

```bash
gcloud services enable run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com
```

### 2. Create a GCS Bucket

```bash
export BUCKET_NAME=my-github-clone-storage
gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1
```

### 3. Build and Deploy

You can deploy directly from source using Cloud Build.

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export SERVICE_NAME=github-clone

# Submit build to Artifact Registry (or Container Registry)
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --execution-environment gen2 \
    --set-env-vars BUCKET_NAME=$BUCKET_NAME
```

**Note:** We use `--execution-environment gen2` which is recommended for file system operations.

### 4. Permissions

The Cloud Run service account needs permission to access the GCS bucket.

```bash
# Get the service account
SERVICE_ACCOUNT=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(spec.template.spec.serviceAccountName)')

# Grant Storage Object Admin
gcloud storage buckets add-iam-policy-binding gs://$BUCKET_NAME \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/storage.objectAdmin
```

## 🔌 API Endpoints

- **GET /api/v1/repositories**: List all repositories.
- **POST /api/v1/repositories**: Create a new repository.
- **GET /api/v1/repositories/{repo_name}/files**: List files in a repository.

## 📂 Project Structure

```
.
├── app/
│   ├── api/            # API routes and models
│   ├── core/           # Configuration
│   ├── services/       # Business logic (Storage operations)
│   └── main.py         # App entry point
├── scripts/
│   └── entrypoint.sh   # Startup script for mounting GCS
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 📝 Notes on GCS FUSE

- **Latency**: File system operations on GCS are slower than local disk.
- **Consistency**: GCS is strongly consistent, but `gcsfuse` caching might introduce delays.
- **Pricing**: You are charged for GCS storage, operations, and network egress.

---

Built with ❤️ by Jules.

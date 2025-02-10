# API Backend for IBD Fatigue ML Model

## Introduction

This FastAPI project serves a TensorFlow model designed to predict fatigue in IBD patients. The API offers a seamless integration between advanced machine learning techniques and modern web services, ensuring optimized predictions and easy deployment.

## Requirements

Install the following dependencies:

- fastapi[standard]==0.115.8
- keras==3.8.0
- shap==0.46.0
- pandas==2.2.3
- tensorflow==2.18.0
- matplotlib==3.10.0
- scikit-learn==1.5.2
- gunicorn==23.0.0

You can also install them using pip:

```bash
pip install -r requirements.txt
```

## Project Structure

```plaintext
main.py                # Entry point for the FastAPI application

src/
├── constants.py       # Project-wide constants
├── models.py          # Machine learning model loading and inference logic
└── utils.py           # Utility functions used across the application

source_model/
├── fatigue_model.keras    # Trained TensorFlow model
├── scaler.pkl             # Data scaler used for preprocessing
├── shap_explainer.pkl     # SHAP explainer file
└── X_train.csv            # Training dataset

deployment/
├── fastapi.socket         # Systemd socket file for FastAPI
├── fastapi.service        # Systemd service file for FastAPI
├── fastapi.nginx          # Nginx configuration file for deployment
└── github_deploy_fastapi.sh  # Deployment script to assist with automated deployments

venv/
└── (virtual environment including necessary Python packages)
```

## Local Development

1. Ensure Python 3.11+ is installed.

2. Clone the repository (if not already done) and navigate to the project directory:

    ```bash
    git clone git@github.com:shaunchuah/fatigue_ml_prod.git
    cd fatigue_ml_prod
    ```

3. Create a virtual environment and activate it:
    - On macOS/Linux:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - On Windows:

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the FastAPI server in development mode:

    ```bash
    uvicorn main:app --reload
    ```

6. Open your browser and go to:
    - API docs: <http://127.0.0.1:8000/docs>
    - Alternative API docs: <http://127.0.0.1:8000/redoc>

## Production Server Setup

Follow these steps to configure the production server:

1. **Create and prepare a new user**
    - Create a new user and add to the sudo group:

      ```sh
      sudo adduser fastapi
      sudo usermod -aG sudo fastapi
      ```

    - Switch to the new user:

      ```sh
      su fastapi
      ```

2. **Generate and configure SSH keys**
    - Generate an RSA SSH key:

      ```sh
      ssh-keygen -t rsa
      ```

    - Display your public key and add it as a deploy key on GitHub:

      ```sh
      cat ~/.ssh/id_rsa.pub
      ```

3. **Clone the repository and set up the environment**
    - Clone your GitHub repository:

      ```sh
      git clone git@github.com:shaunchuah/fatigue_ml_prod.git
      cd fatigue_ml_prod
      ```

    - Create a virtual environment and install dependencies:

      ```sh
      python3 -m venv venv
      pip install -r requirements.txt
      ```

4. **Configure services and deployment files**
    - Copy systemd socket and service configuration files:

      ```sh
      sudo cp deployment/fastapi.socket /etc/systemd/system/fastapi.socket
      sudo cp deployment/fastapi.service /etc/systemd/system/fastapi.service
      sudo systemctl daemon-reload
      sudo systemctl enable fastapi
      ```

    - Set up Nginx:

      ```sh
      sudo cp deployment/fastapi.nginx /etc/nginx/sites-available/fastapi
      sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
      sudo nginx -t
      sudo systemctl restart fastapi
      sudo systemctl restart nginx
      sudo certbot --nginx
      ```

5. **Deploy additional resources**
    - Copy the SHAP explainer file to the project directory:

      Copy `source_model/shap_explainer.pkl` into the project directory using SFTP.

## Docker Production Deployment

1. **Build the Docker image**

    ```bash
    docker build -t shaunchuah/fatigue_ml_prod .
  
    ```

2. **Run the Docker container**

    ```bash
    docker run -d -p 8080:8080 --name fatigue_ml_container --restart always fatigue_ml_prod
    ```

3. **Updating the Docker container**

    ```bash
    docker stop fatigue_ml_container
    docker rm fatigue_ml_container
    docker run -d -p 8080:8080 shaunchuah/fatigue_ml_prod --name fatigue_ml_container --restart always
    ```

## Author

Developed by Shaun Chuah. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

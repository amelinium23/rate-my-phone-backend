### Rate my phone - backend
![img](https://github.com/amelinium23/rate-my-phone-backend/actions/workflows/main.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
---
### Setup
Prerequisites:
- min. Python 3.9
- installed virtual environment, if you don't have this package install it by:
  ```bash
  pip install virtualenv
  ```

1. Make virtual environment by command:
    ```bash
    python -m venv venv
    ```
2. Activate virtual environment:
    ```bash
    source venv/bin/activate
    ```
3. Install all packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Setup .env (for all secret contact developer):
    ```bash
    touch .env
    ```
    Edit file to contain this variables:
    ```sh
    GOOGLE_CREDENTIALS = ''
    GOOGLE_APPLICATION_CREDENTIALS = "google-credentials.json"
    GSM_ARENA_API_URL = 'https://script.google.com/macros/s/AKfycbwZVHW_-CozBkuiQwX-YEBA5L6PVhMV3YDu-1KZXHThiqdQxzyRfx89uf1Lm-8dDV5J/exec'
    ```

#### VS Code setup
1. Create .vscode folder
2. Inside .vscode create `launch.json` file, and copy the configuration:
    ```json
    {
      "configurations":
      [
          {
              "name": "Python: Flask",
              "type": "python",
              "request": "launch",
              "module": "flask",
              "env": {
                  "FLASK_APP": "${workspaceRoot}/wsgi.py",
                  "FLASK_ENV": "development",
                  "FLASK_DEBUG": "1"
              },
              "args": [
                  "run",
              ],
              "jinja": true,
          }
      ]
    }
    ```
3. Launch project from Run and Debug tab.

---

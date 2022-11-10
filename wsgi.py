from main.app import rate_my_phone_app
import os

if __name__ == "__main__":
    print(os.environ.get("PYTHON_VERSION", None))
    rate_my_phone_app.run()

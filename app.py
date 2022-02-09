from flask import Response
from .Brands.brand_routes import brands
from . import app

app.register_blueprint(brands)

@app.route('/')
def hello_page() -> Response:
    return Response('Welcome to rate my phone api!', status=200)

if __name__ == '__main__':
    app.run()
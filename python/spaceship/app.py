import numpy as np 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from spaceship.config import Settings
from spaceship.routers import api, health


def make_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.state.settings = settings

    if settings.debug:
        app.mount('/static', StaticFiles(directory='build'), name='static')

    app.include_router(api.router, prefix='/api', tags=['api'])
    app.include_router(health.router, prefix='/health', tags=['health'])

    @app.get('/', include_in_schema=False, response_class=FileResponse)
    async def root() -> str:
        return 'build/index.html'

    @app.get('/matrix')
    def matrix() -> dict:
        matrix_a = np.random.randint(1,9,(10,10))
        matrix_b = np.random.randint(1,9,(10,10))
        product = np.dot(matrix_a,matrix_b)
        res = {
            "matrix_a":matrix_a.tolist(),
            "matrix_b":matrix_b.tolist(),
            "product":product.tolist()
        }
        return res

    return app
#Alex Shopiak was here
#Alex Shopiak was here twice
from typing import Union
from fastapi import FastAPI, Request, Response, Body
from scraper.product import Product
from shopee_scraper import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{username}")
async def read_items(username: str, q: Union[str, None] = None):
    shopee_scrapper = ShopeeScrapper(username)
    products, error_msg = shopee_scrapper.scrape_list_items()
    data = {}
    if not error_msg: data['data'] = shopee_scrapper.generate_items_json(products)
    data['message'] = error_msg
    return data

@app.get("/products/")
async def get_product(request: Request, response: Response, payload: dict = Body(default={})):
    url = payload['url'] if 'url' in payload else request.query_params.get('url')
    product = Product(url)
    data = product.info().serialize()

    if data:
        response.status_code = 200
        response.body = data
    else:
        response.status_code = 500
        response.body = {'error': 'Something went wrong'}
    
    return response.body
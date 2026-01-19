from fastapi import FastAPI,Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/book/{id}")
async def get_book(id: int = Path(..., gt=0 , le=100 ,description="书籍id,取值范围1-100")):

    return {
        "id": id
    }


@app.get("/author/{name}")
async def get_author(name: str = Path(..., min_length=2, max_length=10)):
    return {
        "name": f"这是{name}的信息"
    }

@app.get("/news/{id}")
async def get_news(id:int = Path(...,gt=0,lt=100)):
    return {
        "id":id
    }

@app.get("/news/category")
async def get_news_category(category:str = Path(...,min_length=2,max_length=10)):
    return {
        "category":category
    }
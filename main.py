from optparse import Option
from typing import Optional

from fastapi import FastAPI,Path,Query
from pydantic import BaseModel,Field

from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/book/id/{id}")
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
#需求 查询新闻 -> 分页 ,skip:跳过的记录数,limit:返回的记录数
@app.get("/news/news_list")
async def get_news_page(
        skip:int = Query(0,ge=0,le=100,description="跳过的记录数"),
        limit:int = Query(10,ge=0,le=100,description="返回的记录数")
):
    return {
        "skip":skip,
        "limit":limit
    }


@app.get("/book/info")
async def get_book_info(
        category:str = Query("Python开发",min_length=5,max_length=255),
        price:int = Query(...,gt=50,le=100)
):
    return {
        "category":category,
        "price":price
    }

class User(BaseModel):
    username: str = Field("张三",min_length=2,max_length=255,description="用户名")
    password: str = Field(...,min_length=5,max_length=255,description="密码")


@app.post("/user/register")
async def register(user:User):
    return {
        "username":user.username,
        "password":user.password
    }

class Book(BaseModel):
    name:str = Field(...,min_length=2,max_length=20)
    author:Optional[str] = Field(None,min_length=2,max_length=20)
    publisher:str = Field("黑马出版社")
    price:float = Field(...,gt=0)

@app.post("/book/add")
async def add_book(book:Book):
    return {
        "name":book.name,
        "author":book.author,
        "publisher":book.publisher,
        "price":book.price
    }


@app.get("/html",response_class=HTMLResponse)
async def get_html():
    html = """
    <html>
        <body>
            <h1>这是HTML页面</h1>
        </body>
    </html>
    """
    return html

@app.get("/file")
async def get_file():
    file_name = "C:/Users/hanbing/Pictures/Screenshots/屏幕截图222.png"

    return FileResponse(file_name)
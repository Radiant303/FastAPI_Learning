from optparse import Option
from typing import Optional

from datetime import datetime
from fastapi import FastAPI,Path,Query,HTTPException,Depends
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse
from sqlalchemy import DateTime, func, String
from starlette.responses import FileResponse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
app = FastAPI()

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_test?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,          # 是否打印SQL
    pool_size=10,       # 连接池大小
    max_overflow=10     # 最大溢出连接数
)

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        comment="创建时间"
    )

    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )


class Book(Base):
    __tablename__ = "book"

    id:Mapped[int] = mapped_column(primary_key=True,comment="书籍ID")
    bookname:Mapped[str] = mapped_column(String(255),comment="书籍名称")
    author:Mapped[str] = mapped_column(String(255),comment="书籍作者")
    publisher:Mapped[str] = mapped_column(String(255),comment="书籍出版社")
class User(Base):
    __tablename__ = "user"

    id:Mapped[int] = mapped_column(primary_key=True,comment="用户ID")
    username:Mapped[str] = mapped_column(String(255),comment="用户名称")
    password:Mapped[str] = mapped_column(String(255),comment="用户密码")

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()



# @app.middleware("http")
# async def middleware1(request,call_next):
#     print("中间件1开始执行")
#     response = await call_next(request)
#     print("中间件1结束执行")
#     return response
#
# @app.middleware("http")
# async def middleware2(request,call_next):
#     print("中间件2开始执行")
#     response = await call_next(request)
#     print("中间件2结束执行")
#     return response
@app.get("/")
async def root():
    return {"message": "Hello World"}






#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.get("/book/id/{id}")
# async def get_book(id: int = Path(..., gt=0 , le=100 ,description="书籍id,取值范围1-100")):
#
#     return {
#         "id": id
#     }
#
#
# @app.get("/author/{name}")
# async def get_author(name: str = Path(..., min_length=2, max_length=10)):
#     return {
#         "name": f"这是{name}的信息"
#     }
#
# @app.get("/news/{id}")
# async def get_news(id:int = Path(...,gt=0,lt=100)):
#     return {
#         "id":id
#     }
#
# @app.get("/news/category")
# async def get_news_category(category:str = Path(...,min_length=2,max_length=10)):
#     return {
#         "category":category
#     }
# #需求 查询新闻 -> 分页 ,skip:跳过的记录数,limit:返回的记录数
# @app.get("/news/news_list")
# async def get_news_page(
#         skip:int = Query(0,ge=0,le=100,description="跳过的记录数"),
#         limit:int = Query(10,ge=0,le=100,description="返回的记录数")
# ):
#     return {
#         "skip":skip,
#         "limit":limit
#     }
#
#
# @app.get("/book/info")
# async def get_book_info(
#         category:str = Query("Python开发",min_length=5,max_length=255),
#         price:int = Query(...,gt=50,le=100)
# ):
#     return {
#         "category":category,
#         "price":price
#     }
#
# class User(BaseModel):
#     username: str = Field("张三",min_length=2,max_length=255,description="用户名")
#     password: str = Field(...,min_length=5,max_length=255,description="密码")
#
#
# @app.post("/user/register")
# async def register(user:User):
#     return {
#         "username":user.username,
#         "password":user.password
#     }
#
# class Book(BaseModel):
#     name:str = Field(...,min_length=2,max_length=20)
#     author:Optional[str] = Field(None,min_length=2,max_length=20)
#     publisher:str = Field("黑马出版社")
#     price:float = Field(...,gt=0)
#
# @app.post("/book/add")
# async def add_book(book:Book):
#     return {
#         "name":book.name,
#         "author":book.author,
#         "publisher":book.publisher,
#         "price":book.price
#     }
#
#
# @app.get("/html",response_class=HTMLResponse)
# async def get_html():
#     html = """
#     <html>
#         <body>
#             <h1>这是HTML页面</h1>
#         </body>
#     </html>
#     """
#     return html
#
# @app.get("/file")
# async def get_file():
#     file_name = "C:/Users/hanbing/Pictures/Screenshots/屏幕截图222.png"
#
#     return FileResponse(file_name)
#
# class News(BaseModel):
#     id:int
#     title:str
#     content:str
#
# @app.get("/news/{id}",response_model=News)
# async def get_news(id:int):
#     return {
#         "id":id,
#         "title":"新闻标题",
#         "content":"新闻内容"
#     }
#
# @app.get("/newsex/{id}")
# async def get_news(id:int):
#     if id == 1:
#         return {
#             "id":id,
#             "title":"新闻标题",
#             "content":"新闻内容"
#         }
#     else:
#         raise HTTPException(status_code=404,detail="新闻不存在")


# async def common_parameters(
#         skip:int = Query(0,ge=0,le=100),
#         limit:int = Query(10,ge=0,le=100)
# ):
#     return {"skip":skip,"limit":limit}
#
# @app.get("/news/news_list")
# async def get_news_list(commons = Depends(common_parameters)):
#     return commons
#
#
# @app.get("/user/user_list")
# async def get_user_list():
#     return {
#         "message":"hello"
#     }
#



import time
import traceback
from fastapi import Depends,status, FastAPI, HTTPException,Form,Request, File, UploadFile
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse,JSONResponse
from fastapi.exceptions import HTTPException, RequestErrorModel,RequestValidationError,WebSocketRequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from loguru import logger


def register_exception(app: FastAPI):
    """
    全局异常捕获
    :param app:
    :return:
    """
    #@app.exception_handler(HTTPException)
    #async def custom_http_exception_handler(request: Request, exc: RequestValidationError):
    #    print(f"OMG! An HTTP error!: {repr(exc)}")
        #触发 HTTPException 时，可以用参数 detail 传递任何能转换为 JSON 的值，不仅限于 str。
        #还支持传递 dict、list 等数据结构。
        #FastAPI 能自动处理这些数据，并将之转换为 JSON。

    # 捕获参数 验证错误
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """ 
        捕获请求参数 验证错误
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"参数错误\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"code": 10002, "data": {"tip": exc.errors()}, #"body": exc.body,
                                      "message": "参数不全或参数错误"}),
        )

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        logger.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "data": {"tip": "服务器错误"}, "message": "fail"},
        )

    # 捕获断言错误，用于返回错误状态
    @app.exception_handler(AssertionError)
    async def asser_exception_handler(request: Request, exc: AssertionError):
        logger.error(f"断言错误，URL：{request.url}, 此处条件不符合")
        logger.info(f"------------------------{exc.args}")
        state = exc.args[0] if exc.args else 0
        return JSONResponse(res(state=state))

# 声明一个 源 列表；重点：要包含跨域的客户端 源
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    # 客户端的源
    "http://127.0.0.1:8081"
]

def register_cors(app: FastAPI):
    """
    支持跨域  https://developer.aliyun.com/article/921791
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='https?://.*',  # 改成用正则就行了 # 允许访问的源 =origins
        allow_credentials=True,# 支持 cookie
        allow_methods=["*"],   # 允许使用的请求方法
        allow_headers=["*"],   # 允许携带的 Headers
    )


def register_middleware(app: FastAPI):
    """
    请求响应拦截
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 5))
        logger.info(f"访问记录:{request.method} url:{request.url}  耗时:{str(round(process_time, 5))}")
        return response

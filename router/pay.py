# 导入必要的库
from fastapi import Request,Depends
from models.db import User
from router.auth import check_token
from fastapi import APIRouter
from fastapi.responses import HTMLResponse ,JSONResponse,PlainTextResponse
from pydantic import BaseModel
from models.db import HistoryMoney

# 参考资料
# https://github.com/fzlee/alipay/blob/master/docs/apis.zh-hans.md

from alipay import AliPay
# 实例化FastAPI
router = APIRouter()

# 定义请求体模型
class Order(BaseModel):
    subject: str
    out_trade_no: str
    total_amount: float
        
        

 

# 定义支付接口
@router.post("/alipay", response_class=JSONResponse)
async def pay(payment: dict,current_user:User=Depends(check_token)):
    print(payment)

    order = Order(
        subject="test",
        out_trade_no="t0001",
        total_amount=0.01
    )


    #业务处理:使用python skd 调用支付宝的支付接口
    app_private_key_string = open('./static/key/app_private_key.pem').read()
    alipay_public_key_string = open('./static/key/alipayPublicKey_RSA2.pem').read()
    

    # 实例化AliPay
    alipay = AliPay(
        appid="2021003196616041",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True  # 默认False
    )


    # 构造订单参数
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order.out_trade_no,
        total_amount=order.total_amount,
        subject=order.subject,
        return_url="http://localhost:8000/alipay/success",
        notify_url="http://localhost:8000/alipay/notify"
    )
    # 构造支付页面url  正式环境位子https://openapi.alipay.com/gateway.do
    pay_url = f"https://openapi.alipay.com/gateway.do?{order_string}"
    # 返回支付页面
    #return f"<h1>请前往支付页面完成支付：</h1><a href='{pay_url}'>去支付</a>"
    return JSONResponse({'statu': "ok",'errmsg':'ok','alipay_url': pay_url})
    return f"<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script><script>$(document).ready(function(){{window.open('{pay_url}')}});</script>"


# 定义支付宝回调接口
@router.post("/alipay/notify", response_class=PlainTextResponse)
async def notify(request: Request):
    # 获取POST请求中的参数
    params = await request.form()
    # 将参数转换为字典类型
    post_dict = {}
    for key, value in params.items():
        post_dict[key] = value
    # 调用SDK中的verify方法进行验签
    result = alipay.verify(post_dict, post_dict.pop("sign"))
    if result:
        # 验签通过，处理业务逻辑
        # TODO: 处理业务逻辑
        return "success"
    else:
        # 验签失败，记录日志并返回错误信息
        # TODO: 记录日志
        return "fail"

# 定义成功回调接口
@router.post("/alipay/success", response_class=PlainTextResponse)
async def success(request: Request):
    # TODO: 处理成功回调逻辑
    return "success"
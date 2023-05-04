from easy_i18n.t import Ai18n
from conf.config import configs
import os
# BASE_DIR
"""
使用的地方： 比如统一的 response.py 可以通过 imort导入

from api.utils.i18nHelper import t

message=t("{param} format error").format(param="密码")


**Ai18n 说明**
Ai18n 类接收两个参数：
1.参数 locales 是list形式，指定了语言都使用哪几种。举例：["en", "zh"] 那么对应的会在config指定的目录下找 en.json 和 zh.json加载过来
默认的 east_i18n 有目录 i18n 可供参考
2.参数 config 是dict形式，你可以指定后覆盖默认的 config值：

    :load_path - where to find translate files（default is : i18n）
    :default_locale - default locale（default is : en）
    :default_module - default module（default is : g）
    :default_encoding - default encoding（default is : UTF-8）

    
**config 说明**
config使用举例：

    config = {
        "load_path": "/locales", # 指定在 /locales 下找对应的翻译 json文件
        "default_module": "global", # 指定默认的全局模块，你可以为比如用户模块，订单模块单独设置翻译，如果不指定 module 则会去全局模块查找。
    }
    a_i18n = Ai18n(locales=["en", "zh"], config=config)

**NOTE:** 
for example your locale is en , define load_path as a absolutely path is recommended,
create an en.json in this path. the content for example is: (default_module should equal g)
    {
      "g": {
        "hi": "hello world",
        "test": "test 1"
      },
      "user": {
        "hi": "user:hello world",
        "user {id} is deleted": "user {id} is deleted"
      }
    }

比如上述例子指定 load_path 为 /locales 且 Ai18n(locales=["en", "zh"], config=config)  
那么要提前在 /locales 下 创建 en.json 和 zh.json  
json内容参考上述例子即可  

"""
config = {
    "load_path": os.path.join(configs.BASE_DIR, 'conf'),
    "default_locale": "zh", 
}
a_i18n = Ai18n(locales=["zh"], config=config)
t = a_i18n.translate

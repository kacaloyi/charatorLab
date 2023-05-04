代码规范: https://blog.csdn.net/axiaowua/article/details/119038533

main (存放启动项目入口文件)
- control(存放和数据库交互的控制器文件)
- item / model (存放数据结构文件)
- router
    |-internal (存放内部api处理文件)
        |--routers.py (路由模块)
        |--dependencies.py (依赖项模块)
    |- external (存放外部api处理文件)
        |--routers.py (路由模块)
        |--dependencies.py (依赖项模块)
    |..(其他分类api)

- docs (存放相关文档)
- conf (存放配置文件)
- static (存放静态资源文件)
- views (存放模板文件)
- utils (存放三方、工具、常量、异常等公用模块)
- log (存放临时日志文件)
- task (存放异步任务文件 Celery 等)
- database (存放数据库文件)
- test (测试代码)
gunicorn.conf.py
README.md
requirements.txt
xx.sh   启停脚本
# https://pypi.org/project/fastapi-mail/ 
# pip install fastapi-mail
# https://sabuhish.github.io/fastapi-mail/example/



# FastAPI 上传文件
# https://www.jb51.net/article/252704.htm 

# 使用File需要提前安装 python-multipart
# https://blog.csdn.net/xys430381_1/article/details/123890134 上传并保存，返回服务器端的文件url。
# 客户端bootstrap的写法
# https://blog.csdn.net/qq_38688799/article/details/89326159
# https://www.zhiu.cn/68859.html 


@app.post("/upload/)
async def upload(file: UploadFile = File(...)):
    imgbytes = file.read() # imgbytes includes all the file format informatiorimgname = file.filename
    # imgbase64 = base64.b64decode(imgbytes)# don't do this
    pathname = "/img/"+file.filename
    with open(pathname, 'wb') as  f
        f.write(imgbytes)# imgbytes includes the file format information, so fout.mrite(ingbytes) will save the bytes as image,video or others# fout.write(imgbase64) # if fout.write(imgbase64), the saved file is messy codefout.close()
        f.close()
    file.close()
    return {"pathname":pathname}
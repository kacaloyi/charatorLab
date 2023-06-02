>openssl
OpenSSL> genrsa -out app_private_key.pem  2048
OpenSSL> rsa -in app_private_key.pem -pubout -out app_public_key.pem
必须用OpenSSL生成app公钥私钥。把公钥上传给阿里。
下载的阿里公钥，注意需要在文本的首尾添加标记位(-----BEGIN PUBLIC KEY-----和-----END PUBLIC KEY-----) 
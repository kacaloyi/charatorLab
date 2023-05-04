#!/usr/bin/env python
# -*- coding:utf-8 -*-
#import jwt
from jose import JWTError, jwt 

from datetime import datetime, timedelta
from typing import List,Optional
from conf.config import *
#from jose.jwt import  exceptions

JWT_SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_token(payload: dict, key = JWT_SALT ,timeout=20):
    """
    :param payload: 例如：{'user_id':1,'username':'wupeiqi'}用户信息
    :param timeout: token的过期时间，默认20分钟
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }

    payload['exp'] = datetime.utcnow() + timedelta(minutes=timeout)

    result = jwt.encode(payload=payload, key=key,
                        algorithm="HS256", headers=headers).decode('utf-8')
    return result


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, True)
        result['status'] = True
        result['data'] = verified_payload
    except jwt.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.JWTError:
        result['error'] = 'token认证失败'
    except jwt.JWTClaimsError:
        result['error'] = '非法的token'

        #JWTError: If the signature is invalid in any way.
        #ExpiredSignatureError: If the signature has expired.
        #JWTClaimsError: If any claim is invalid in any way.

    
    return result

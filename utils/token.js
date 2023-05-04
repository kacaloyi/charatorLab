
/*
 *创建一个cookie方法
 *终端cookie缓存，键值对key=value；如果key的名称相同则会覆盖上一个值
 *新增：cookieHandler.set("key1",value);
 *获取：cookieHandler.get("key1",defaultValue);
 *删除：cookieHandler.del("key1");
 */
 var cookieHandler = {
	path: "/",
	get: function(cookie_name, default_value) {
		var reg = '(/(^|;| )' + cookie_name + '=([^;]*)(;|$)/g)';
		var temp = eval(reg).exec(document.cookie);
		if (temp != null) {
			var value = temp[2];
			return escape(value);
		}
		return default_value;
	},
	set: function(name, value, day) {
		day = day == undefined ? 30 : day;
		var str = name + '=' + value + '; ';
		if (day) {
			var date = new Date();
			date.setTime(date.getTime() + day * 24 * 3600 * 1000);
			str += 'expires=' + date.toGMTString() + '; ';
		}
		str += "path=" + this.path;
		document.cookie = str;
	},
	del: function(name) {
		this.set(name, null, -1);
	}
};

// 获取token
//cookieHandler.get("normal_login_token")
// 删除token
//cookieHandler.del("normal_login_token")


//在登录中使用cookie方法保存token
let data = {
    loginName: $("#phone").val(),
    loginType: $('#checkbox1').is(':checked') ? "1" : "0",
    password: $.md5($("#pwd").val()),
}
$.ajax({
    type: "post", // 请求方式
    contentType: "application/json",
    url: login + "v1/userLogin?loginName=" + data.loginName + "&loginType=" + data.loginType + "&password=" + data.password,
    dataType: "json", // 数据类型可以为 text xml json  script  jsonp
    success: function(res) { // 返回的参数就是 action里面所有的有get和set方法的参数
        if (res.resultCode === "00000000") {
            showMessage("登录成功", 1);
            // 使用cookie保存token
            cookieHandler.set("normal_login_token", res.data.token)
            cookieHandler.set("accountId", res.data.user.accountId)
            cookieHandler.set("cellPhone", res.data.user.cellPhone)
            $(location).prop('href', './Account.html')
        } else {
            showMessage(res.resultMsg, 0);
        }
    }
});





/*
handleSubmit(who)
{
      if (who == 1) {
        instance.post('/login/studentLogin',{
            username: this.ruleForm2.username,
            password: this.ruleForm2.password
          }).then(res => {
          console.log(res.data);
          if (res.data.code == 200) {
            alert("登陆成功,返回token是" + res.data.data.token);
            //把token字符串放在cookie里面(第一个参数cookie名称，第二个名称参数值，第三个参数作用范围)
            cookie.set('token', res.data.data.token,{domain:'localhost'});
            this.$router.push({name:'Student'})//跳转到学生路由
          } else {
            alert(res.data.message)
          }
        }
};
*/
/*
function Cookie(key, value) {
    this.key = key;
    if (value != null) {
        this.value = escape(value);
    }
    this.expiresTime = null;
    this.domain = null;
    this.path = "/";
    this.secure = null;
}
Cookie.prototype.setValue = function (value) {
    this.value = escape(value);
}
Cookie.prototype.getValue = function () {
    return unescape(this.value);
}

Cookie.prototype.setExpiresTime = function (time) {
    this.expiresTime = time;
}

Cookie.prototype.getExpiresTime = function () {
    return this.expiresTime;
}

Cookie.prototype.setDomain = function (domain) {
    this.domain = domain;
}

Cookie.prototype.getDomain = function () {
    return this.domain;
}
Cookie.prototype.setPath = function (path) {
    this.path = path;
}

Cookie.prototype.getPath = function () {
    return this.path;
}

Cookie.prototype.Write = function (v) {
    if (v != null) {
        this.setValue(v);
    }
    var ck = this.key + "=" + this.value;
    if (this.expiresTime != null) {
        try {
            ck += ";expires=" + this.expiresTime.toUTCString();;
        }
        catch (err) {
            alert("expiresTime参数错误");
        }
    }
    if (this.domain != null) {
        ck += ";domain=" + this.domain;
    }
    if (this.path != null) {
        ck += ";path=" + this.path;
    }
    if (this.secure != null) {
        ck += ";secure";
    }
    document.cookie = ck;
}
Cookie.prototype.Read = function () {
    try {
        var cks = document.cookie.split("; ");
        var i = 0;
        for (i = 0; i
            window.onload = function () {
                var ck = new Cookie("HasLoaded");
                if (ck.Read() == null) {
                    //未加载过，Cookie内容为空 

                    window.location.assign("http://localhost/1/2.html");

                    ck.Write("true");
                    //设置Cookie。只要IE不关闭，Cookie就一直存在               
                }
                else {
                    //Cookie存在，表示页面是被刷新的            

                    alert("页面刷新,不在显示该效果");
                }
            }

            //这个页面用来判断是否是第一次打开,是的话则跳转到新页面
*/
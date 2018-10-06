var username_re = /^[A-Za-z0-9\_]{8,16}$/;
var mobile_re = /^(\+?(?:0086|086|86))?((?:13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])(?:\d{8}))$/;

new Vue({
    el: '#register',
    data: {
        username: '',
        nickname: '',
        password: '',
        password2: '',
        mobile: '',
        email: ''
    },
    methods: {
        login: function() {
            if(!username_re.exec(this.username)){
                alert('帐号非法')
                return ;
            };
            if(this.password != this.password2){
                alert('两次密码不同')
                return ;
            };
            if(this.password.length<8 || this.password.length>32){
                alert('密码非法')
                return ;
            };
            if(!mobile_re.exec(this.mobile)){
                alert('手机号非法')
                return ;
            };
            var form = {
                username: this.username,
                password: this.password,
                mobile: this.mobile,
                email: this.email,
                nickname: this.nickname
            }
            this.$http.post(api.Register,
                form, {emulateJSON:true}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        window.location.href = '/'
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        }
    }
})

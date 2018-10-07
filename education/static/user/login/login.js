var username_re = /^[A-Za-z0-9\_]{8,16}$/;
var mobile_re = /^(\+?(?:0086|086|86))?((?:13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])(?:\d{8}))$/;

new Vue({
    el: '#login',
    data: {
        username: '',
        password: '',
    },
    methods: {
        login: function() {
            if(!username_re.exec(this.username)){
                alert('帐号错误')
                return ;
            };
            if(this.password.length<8 || this.password.length>32){
                alert('密码错误')
                return ;
            };
            var form = {
                username: this.username,
                password: this.password,
            }
            this.$http.post(api.Login,
                form, {emulateJSON:true}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        console.log(result.data);
                        var user_json = JSON.stringify(result.data)
                        localStorage.setItem("user", user_json);
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

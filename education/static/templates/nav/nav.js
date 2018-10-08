Vue.component('edunav', {
    props: ['index', 'user'],
    template:   '<div class="navInner"> \
                    <span class="navLogo"><a href=""><img src="/static/images/catalogue/kedaya.jpg"/></a></span> \
                    <a v-if="user"><span class="user logout" v-on:click="logout">退出</span><span class="user">{{user.nickname || user.username}}</span></a>\
                    <a href="/static/user/login/login.html" v-else="user"> \
                        <span class="BusinessLogin">登录</span>\
                    </a> \
                    <ul class="navMenu"> \
                        <a href="/static/catalogue/index.html"> \
                            <li :class="{menuAction: index==0}" >首页</li> \
                        </a> \
                        <a href="/static/catalogue/example/query/query.html"> \
                            <li :class="{menuAction: index==1}">查题</li> \
                        </a> \
                        <a href="/static/catalogue/category/create/create.html" v-if="user && user.permissions.modify_category"> \
                            <li :class="{menuAction: index==2}">创建分类</li> \
                        </a> \
                        <a href="/static/catalogue/example/create/create.html"> \
                            <li :class="{menuAction: index==3}">创建题目</li> \
                        </a> \
                        <a> \
                            <li :class="{menuAction: index==4}">test</li> \
                        </a> \
                        <a> \
                            <li :class="{menuAction: index==5}">test</li> \
                        </a> \
                    </ul> \
                    <link rel="stylesheet" href="/static/templates/nav/nav.css"></link> \
                </div>',
    methods:{
        logout: function(){
            this.$http.get(api.Logout).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        localStorage.removeItem('user');
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

// html
// <div id="nav">
//     <nav v-bind:index="index">
//     </nav>
// </div>
var Nav = new Vue({
    el: '#nav',
    data: {
        index: null,
        user: null
    },
    created: function(){
        if(localStorage.user){
            this.user = JSON.parse(localStorage.getItem('user'));
            console.log(this.user);
        }
    }
})

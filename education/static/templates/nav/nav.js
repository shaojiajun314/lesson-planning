Vue.component('edunav', {
    props: ['index', 'user'],
    template:   '<div class="navInner"> \
                    <span class="navLogo"><a href="/"><img src="/static/images/catalogue/kedaya.jpg"/></a></span> \
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
                        <a href="/static/dashboard/permissions/permissions.html" v-if="user && user.permissions.is_staff"> \
                            <li :class="{menuAction: index==4}">权限管理</li> \
                        </a> \
                        <a　href="/static/catalogue/files/query/query.html?type=courseware"> \
                            <li :class="{menuAction: index==5}">查课件</li> \
                        </a> \
                        <a　href="/static/catalogue/files/query/query.html?type=examination_outline"> \
                            <li :class="{menuAction: index==5}">查提纲</li> \
                        </a> \
                        <a　href="/static/catalogue/files/create/create.html?type=courseware"> \
                            <li :class="{menuAction: index==5}">上传新课件</li> \
                        </a> \
                        <a　href="/static/catalogue/files/create/create.html?type=examination_outline"> \
                            <li :class="{menuAction: index==5}">上传新提纲</li> \
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
                        sessionStorage.removeItem('user');
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
        if(sessionStorage.user){
            this.user = JSON.parse(sessionStorage.getItem('user'));
        }
    },
    methods: {
        get_user_info: function(){
            if(this.user){
                return ;
            }
            this.$http.post(api.Login,
                {}, {emulateJSON:true}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.user = result.data
                        var user_json = JSON.stringify(result.data)
                        sessionStorage.setItem("user", user_json);
                    }else {
                    }
                },function(){
                });
        }
    }
})

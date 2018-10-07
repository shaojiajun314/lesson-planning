Vue.component('edunav', {
    props: ['index'],
    template:   '<div class="navInner"> \
                    <span class="navLogo"><a href=""><img src="/static/images/catalogue/kedaya.jpg"/></a></span> \
                    <a href="business-login.html"><span class="BusinessLogin">登录</span></a> \
                    <ul class="navMenu"> \
                        <a href="/static/catalogue/index.html"> \
                            <li :class="{menuAction: index==0}" >首页</li> \
                        </a> \
                        <a href="/static/catalogue/example/query/query.html"> \
                            <li :class="{menuAction: index==1}">查题</li> \
                        </a> \
                        <a href="/static/catalogue/category/create/create.html"> \
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
                </div>'
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
    }
})

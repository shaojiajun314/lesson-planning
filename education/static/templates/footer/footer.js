// html
// <div id="nav">
//     <nav v-bind:index="index">
//     </nav>
// </div>


// ' \
// <div class="copyright"> \
//     <p>Copyright © 2018 sxc.com Inc. All Rights Reserved.</p> \
//     <div class="img"> \
//         <i class="icon2"></i> \
//         <span>联系微信：shaojiajun314</span> \
//     </div> \
//     <div class="img"> \
//         <i class="icon1"></i> \
//         <span>联系地址：浙江省湖州市</span> \
//     </div> \
//     <div class="img"> \
//         <i class="icon"></i> \
//         <span>联系邮箱：63770117@qq.com</span> \
//     </div> \
// </div> \
// <link rel="stylesheet" href="/static/templates/footer/footer.css"></link>'
var Footer = new Vue({
    el: '#footer',
    data: {
        html: ' \
        <div class="copyright"> \
            <p>欢迎投递意见或者建议，可通过如下联系方式</p> \
            <div class="img"> \
                <span>联系微信：shaojiajun314</span> \
            </div> \
            <div class="img"> \
                <span>联系地址：浙江省湖州市</span> \
            </div> \
            <div class="img"> \
                <span>联系邮箱：63770117@qq.com</span> \
            </div> \
        </div> \
        <link rel="stylesheet" href="/static/templates/footer/footer.css"></link>'
    }
})

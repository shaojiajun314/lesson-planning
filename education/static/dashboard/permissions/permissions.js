Nav.index = 8

new Vue({
    el: '#permissions',
    data: {
        category_modify: [],
        example_modify: [],
        examinationoutline_modify:[],
        courseware_modify:[],

        category_username: null,
        example_username: null,
        examinationoutline_username: null,
        courseware_username: null
    },
    created: function () {
        this.get_category_modify()
        this.get_example_modify()
        this.get_examinationoutline_modify()
        this.get_courseware_modify()
    },
    methods: {
        get_category_modify: function(){
            this.$http.get(api.DashboardUsersPermissions, {params: {type: 'modify_category'}})
                .then(function(res){
                    var result = res.body
                    console.log(result);
                    if(result.code === 0){
                        this.category_modify = this.category_modify.concat(res.body.data);
                        console.log(this.category_modify);
                    }else {
                        alert(result.desc)
                    }
                },function(e){
                    if(e.status === 403){
                        alert('请先登入');
                        window.location.href = '/static/user/login/login.html'
                    }else {
                        alert('请求错误');
                    }
                });
        },
        get_example_modify: function(){
            this.$http.get(api.DashboardUsersPermissions, {params: {type: 'modify_example'}})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.example_modify = this.example_modify.concat(res.body.data);
                    }else {
                        alert(result.desc)
                    }
                },function(e){
                    if(e.status === 403){
                        alert('请先登入');
                        window.location.href = '/static/user/login/login.html'
                    }else {
                        alert('请求错误');
                    }
                });
        },
        get_examinationoutline_modify: function(){
            this.$http.get(api.DashboardUsersPermissions, {params: {type: 'modify_examinationoutline'}})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.examinationoutline_modify = this.examinationoutline_modify.concat(res.body.data);
                    }else {
                        alert(result.desc)
                    }
                },function(e){
                    if(e.status === 403){
                        alert('请先登入');
                        window.location.href = '/static/user/login/login.html'
                    }else {
                        alert('请求错误');
                    }
                });
        },
        get_courseware_modify: function(){
            this.$http.get(api.DashboardUsersPermissions, {params: {type: 'modify_courseware'}})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.courseware_modify = this.courseware_modify.concat(res.body.data);
                    }else {
                        alert(result.desc)
                    }
                },function(e){
                    if(e.status === 403){
                        alert('请先登入');
                        window.location.href = '/static/user/login/login.html'
                    }else {
                        alert('请求错误');
                    }
                });
        },
        submit_category: function(codename){
            var user_name = {
                'modify_category': this.category_username,
                'modify_example': this.example_username,
                'modify_courseware': this.courseware_username,
                'modify_examinationoutline': this.examinationoutline_username
            }[codename]
            if(!user_name){
                alert('请输入帐号')
                return ;
            }
            this.$http.post(api.DashboardUsersPermissionsCreate,
                {codename: codename, 'username':user_name})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        alert(result.desc)
                        window.location.reload()
                    }else {
                        alert(result.desc)
                    }
                },function(e){
                    if(e.status === 403){
                        alert('请先登入');
                        window.location.href = '/static/user/login/login.html'
                    }else {
                        alert('请求错误');
                    }
                });
        },
        clear_permisson: function(codename, username){
            this.$http.post(api.DashboardUsersPermissionsDelete.replace(/{username}/, username),
                {codename: codename})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        alert(result.desc)
                        window.location.reload()
                    }else {
                        alert(result.desc)
                    }
                },function(e){
                    if(e.status === 403){
                        alert('请先登入');
                        window.location.href = '/static/user/login/login.html'
                    }else {
                        alert('请求错误');
                    }
                });
        }
    }
})

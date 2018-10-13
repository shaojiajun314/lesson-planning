Nav.index = 8

new Vue({
    el: '#permissions',
    data: {
        category_modify: [],
        example_modify: [],
        files_modify:[],

        category_username: null,
        example_username: null,
        files_username: null,

        user_like_list: [],
        selected_username: null,

        dropdown_key: null,
        next_url: null
    },
    created: function () {
        this.get_category_modify()
        this.get_example_modify()
        this.get_file_modify()
    },
    methods: {
        get_category_modify: function(){
            this.$http.get(api.DashboardUsersPermissions, {params: {type: 'modify_category'}})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.category_modify = this.category_modify.concat(res.body.data);
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
        get_file_modify: function(){
            this.$http.get(api.DashboardUsersPermissions, {params: {type: 'modify_edufile'}})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.files_modify = this.files_modify.concat(res.body.data);
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
                'modify_edufile': this.files_username,
            }[codename]
            if(user_name!=this.selected_username){
                alert('出错了,!!!, 请保存这段文字联系开发人员,' + user_name + ',' + this.selected_username)
                return ;
            }
            if(!this.selected_username){
                alert('请选择帐号')
                return ;
            }
            this.$http.post(api.DashboardUsersPermissionsCreate,
                {codename: codename, 'username':this.selected_username})
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
        },
        user_like_search: function(codename){
            var like_user_name = {
                'modify_category': this.category_username,
                'modify_example': this.example_username,
                'modify_edufile': this.files_username,
            }[codename];
            this.$http.get(api.UserLikeSearch,
                {params:{like_username: like_user_name}})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        console.log(result.data.users_list.length);
                        // if(result.data.users_list.length == 0){
                        //     this.user_like_list = [{
                        //         username: '没有对应用户'
                        //     }]
                        //     this.next_url = result.data.next_link
                        //     return
                        // }
                        this.user_like_list = result.data.users_list;
                        this.next_url = result.data.next_link
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
        user_like_dropdown: function(codename){
            this.user_like_search(codename)
            this.dropdown_key = {
                'modify_category': 'category',
                'modify_example': 'example',
                'modify_edufile': 'files',
            }[codename]
        },
        user_like_dropup: function(type) {
            // this.dropdown_key = null
            // if(this.selected_username){
            //     return
            // }
            // this.selected_username = null
            // // var tmp = {'modify_category': this.category_username,
            // //     'modify_example': this.example_username,
            // //     'modify_edufile': this.files_username,
            // // }[type]
            // // tmp = null
            // this.modify_type_username(type, null)
            var that = this
            setTimeout(function(){
                that.do_user_like_dropup(type)
            }, 200)

        },
        do_user_like_dropup(type){
            this.dropdown_key = null
            console.log(this.selected_username, 123131313);
            if(this.selected_username){
                return
            }
            this.selected_username = null
            this.modify_type_username(type, null)
        },
        select_user: function(username, type){
            this.selected_username = username;
            // var tmp = {'modify_category': this.category_username,
            //     'modify_example': this.example_username,
            //     'modify_edufile': this.files_username,
            // }[type]
            // tmp = username
            this.modify_type_username(type, username)
        },
        modify_type_username: function(key, value){
            console.log(key, value);
            if(key == 'modify_category'){
                this.category_username = value
            }else if (key == 'modify_example') {
                this.example_username = value
            }else if (key == 'modify_edufile') {
                this.files_username = value
            }
        }
    }
})


var type = GetRequest().type;
var ApiUrl = {
    'courseware': api.CreateFile.replace(/{type}/, 'courseware'),
    'examination_outline': api.CreateFile.replace(/{type}/, 'examination_outline'),
}[type]
Nav.index = index = {
    courseware: 6,
    examination_outline: 7
}[type]
new Vue({
    el: '#example-create',
    data: {
        title: null,
        description: null,

        category: [],
        current_category: {name:'', id: null},
    },
    methods: {
        get_category_root: function(){
            if(this.category.length != 0){
                return ;
            }
            this.$http.get(api.CategoryRoot).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.category.push(res.body.data);
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        get_category: function(parent_id, category_index){
            var current_length = category_index + 1
            if(this.category.length > current_length){
                this.category = this.category.slice(0, current_length)
            }
            this.$http.get(api.Category.replace(/{parent_pk}/, parent_id)).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.category.push(res.body.data);
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });

        },
        clean_category: function() {
            this.category = []
        },
        input_category: function(id, root_index, index){
            var parent = this.category[root_index][index]
            var path = parent.path
            var current_category_lead = []
            var tmp_category
            while(root_index>=0){
                tmp_category = this.category[root_index]
                for(var i=0; i<tmp_category.length; i++){
                    if(tmp_category[i].path == path){
                        current_category_lead.push(tmp_category[i].name)
                        path = tmp_category[i].path.slice(0, -4)
                    }
                }
                root_index--
            }
            current_category_lead.reverse()
            this.current_category = {name:current_category_lead.join(' -> '), id:id}

            this.clean_category()
        },
        cancel_input_category: function(){
            this.clean_category();
            this.current_category = {name:'', id: null};
        },


        submit_input: function(){
            var content_file = this.$refs.contentFile
            if(!content_file.files.length){
                alert('请选择上传文件')
                return
            }
            if(!this.title){
                alert('请输入标题')
                return
            }
            if(!this.description){
                alert('请输入描述')
                return
            };
            if(!this.current_category.id){
                alert('请输入分类')
                return
            }

            var form = new FormData()
            form.append('title', this.title)
            form.append('description', this.description)
            form.append('file', content_file.files[0])
            form.append('category_id', this.current_category.id)

            this.$http.post(ApiUrl,
                form, {"Content-Type": "multipart/form-data"})
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        Modal.is_hidden = false
                        Modal.title = '上传成功'
                        Modal.body = '跳转详情页面'
                        Modal.cancel = '取消'
                        Modal.cancel_func = function(){
                            Modal.is_hidden = true
                        }
                        Modal.sure = '确定'
                        Modal.sure_func = function(){
                            window.location.href =
                                '/static/catalogue/files/update/update.html?file_id='
                                +result.data.id

                        }

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

    }
})

new Vue({
    el: '#category-create',
    data: {
        name:'',

        category: [],
        current_category: {name:'', id: null},
        current_category_lead: [],
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
            if(!this.name){
                alert('请输入新分类名称')
                return
            };
            if(this.current_category.id){
                parent_id = this.current_category.id + '/' //url拼接需要
            }else {
                parent_id = ''
            }

            var form = new FormData()
            if(this.$refs.imgInput.files.length !== 0) {
                form.append('img', this.$refs.imgInput.files[0])
            }
            form.append('name', this.name)

            this.$http.post(api.CreateCategory.replace(/{parent_id}/, parent_id),
                form, {"Content-Type": "multipart/form-data"}).then(function(res){
                    var result = res.body
                    if(result.code === 0){

                        Modal.is_hidden = false
                        Modal.title = '创建成功'
                        Modal.body = '请选择跳转页面'
                        Modal.cancel = '留在本页'
                        Modal.cancel_func = function(){
                            Modal.is_hidden = true
                        }
                        Modal.sure = '创建新题'
                        Modal.sure_func = function(){
                            window.location.href =
                                '/static/catalogue/example/create/create.html'
                        }

                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });

        },

    }
})

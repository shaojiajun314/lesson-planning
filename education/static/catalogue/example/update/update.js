var example_id = GetRequest().example_id;

new Vue({
    el: '#example-update',
    data: {
        content: '',　//题目

        content_imgs: [],
        content_img_ctr: [true,], //题目图片数量控制

        answer: [],　//答案
        add_answer: '',
        answer_img_ctr: [true,], //答案图片数量控制

        category: [],
        current_category: {name:'', id: null},
        is_edit: false, // 模式 是否为编辑模式

        edit_content: '',
        delete_example_imgs: [], //删除图片id
        delete_answer: [], //删除答案id
        edit_current_category: {name:'', id: null},


    },
    created: function () {
      this.get_example_detail(example_id);
    },
    methods: {
        // 查询模式 start
        get_example_detail: function(pk){
            this.$http.get(api.ExampleDetail.replace(/{pk}/, pk)).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        var data = result.data
                        this.content = data.content
                        this.edit_content = data.content
                        this.handle_categories(data.categories)
                        this.content_imgs = data.images
                        this.answer = data.answers
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        handle_categories: function(categories){
            var current_category_lead = []
            for(var i=0; i<categories.length; i++){
                current_category_lead.push(categories[i].name)
            };
            this.current_category = {name:current_category_lead.join(' -> '),
                id:categories[i-1].id}
            this.edit_current_category = {name:current_category_lead.join(' -> '),
                id:categories[i-1].id}
        },
        // 查询模式 end

        change_mode: function() {
            this.is_edit = !this.is_edit
        },

        // 编辑模式 start
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
            this.edit_current_category = {name:current_category_lead.join(' -> '), id:id}

            this.clean_category()
        },
        cancel_input_category: function(){
            this.clean_category();
            this.edit_current_category = {name:'', id: null};
        },

        input_img: function(index, type) {
            var maps = {
                'answer': this.answer_img_ctr,
                'content': this.content_img_ctr
            }
            if(maps[type].length == index + 1){
                maps[type].push(true)
            }
        },
        add_delete_img: function(example_img_id){
            var i = this.delete_example_imgs.indexOf(example_img_id)
            if( i< 0){
                this.delete_example_imgs.push(example_img_id)
            }else {
                this.delete_example_imgs.splice(i, 1)
            }
        },
        add_delete_answers: function(answer_id){
            var i = this.delete_answer.indexOf(answer_id)
            if( i< 0){
                this.delete_answer.push(answer_id)
            }else {
                this.delete_answer.splice(i, 1)
            }
        },
        submit_input: function(){
            if(!this.edit_content){
                alert('请输入提干')
                return
            };
            // if(!this.add_answer){
            //     alert('请输入答案')
            //     return
            // };
            if(!this.edit_current_category.id){
                alert('请输入分类')
                return
            }
            var form = new FormData()
            form.append('category_id', this.edit_current_category.id)
            form.append('content', this.edit_content)
            form.append('answer', this.add_answer)

            form.append('example_imgs_delete', JSON.stringify(this.delete_example_imgs))
            form.append('answer_delete', JSON.stringify(this.delete_answer))

            // 图片添加
            var content_img = this.$refs.contentImg
            for(var i=0; i<content_img.length; i++){
                if(content_img[i].files.length == 1){
                    form.append(('content_img' + i), content_img[i].files[0])
                }
            }

            var answer_img = this.$refs.answerImg
            for(var i=0; i<answer_img.length; i++){
                if(answer_img[i].files.length == 1){
                    form.append(('answer_img' + i), answer_img[i].files[0])
                }
            }
            this.$http.post(api.UpdateExample.replace(/{pk}/, example_id),
                form, {"Content-Type": "multipart/form-data"}).then(function(res){
                    var result = res.body
                    if(result.code === 0){

                        Modal.is_hidden = false
                        Modal.title = '修改成功'
                        Modal.body = '请选择跳转页面'
                        Modal.cancel = '留在详情页面'
                        Modal.cancel_func = function(){
                            window.location.reload()
                        }
                        Modal.sure = '跳转首页'
                        Modal.sure_func = function(){
                            window.location.href =
                                '/'
                        }

                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        // 编辑模式 end
    }

})

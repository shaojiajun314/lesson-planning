new Vue({
    el: '#example-create',
    data: {
        content: '',　//题目
        content_img_ctr: [true,], //题目图片数量控制

        answer: '',　//答案
        answer_img_ctr: [true,], //答案图片数量控制

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

        input_img: function(index, type) {
            var maps = {
                'answer': this.answer_img_ctr,
                'content': this.content_img_ctr
            }
            if(maps[type].length == index + 1){
                maps[type].push(true)
            }
        },

        submit_input: function(){
            if(!this.content){
                alert('请输入提干')
                return
            };
            if(!this.answer){
                alert('请输入答案')
                return
            };
            if(!this.current_category.id){
                alert('请输入分类')
                return
            }
            var form = new FormData()
            form.append('category_id', this.current_category.id)
            form.append('content', this.content)
            form.append('answer', this.answer)

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
            this.$http.post(api.CreateExample,
                form, {"Content-Type": "multipart/form-data"}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        // 模态框
                        Modal.is_hidden = false
                        Modal.title = '创建成功'
                        Modal.body = '跳转详情页面'
                        Modal.cancel = '取消'
                        Modal.cancel_func = function(){
                            Modal.is_hidden = true
                        }
                        Modal.sure = '确定'
                        Modal.sure_func = function(){
                            window.location.href =
                                '/static/catalogue/example/update/update.html?example_id='+result.data.id
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

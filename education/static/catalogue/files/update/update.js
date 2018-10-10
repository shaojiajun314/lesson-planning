var args = GetRequest();
var file_id = args.file_id
var type = args.type
var FileDetailUrl = api.FileDetail.replace(/{type}/, type).replace(/{pk}/, file_id)
var FileDeleteUrl = api.DeleteFile.replace(/{type}/, type).replace(/{pk}/, file_id)

new Vue({
    el: '#file-update',
    data: {
        file_data: {},
        // content: '',　//题目
        // difficulty: 0,
        //
        // content_imgs: [],
        // content_img_ctr: [true,], //题目图片数量控制
        //
        // answer: [],　//答案
        // add_answer: '',
        // answer_img_ctr: [true,], //答案图片数量控制
        //
        // category: [],
        current_category: {name:'', id: null},
        // is_edit: false, // 模式 是否为编辑模式
        //
        // edit_content: '',
        // delete_example_imgs: [], //删除图片id
        // delete_answer: [], //删除答案id
        // edit_current_category: {name:'', id: null},
        // edit_difficulty: null,

        // permissions_modify: false
    },
    created: function () {
      this.get_file_detail(file_id);
      // this.permissions_modify = Nav.user.permissions.modify_example
    },
    methods: {
        // 查询模式 start
        get_file_detail: function(pk){
            this.$http.get(FileDetailUrl).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        var data = result.data
                        this.file_data = data
                        // this.content = data.content
                        // this.edit_content = data.content
                        console.log(data);
                        this.handle_categories(data.categories)
                        // this.content_imgs = data.images
                        // this.answer = data.answers
                        // this.difficulty = data.difficulty
                        // this.edit_difficulty = data.difficulty
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
        handle_categories: function(categories){
            var current_category_lead = []
            for(var i=0; i<categories.length; i++){
                current_category_lead.push(categories[i].name)
            };
            this.current_category = {name:current_category_lead.join(' -> '),
                id:categories[i-1].id}
        },
        // 查询模式 end

        download: function() {
            console.log();
            window.open(this.file_data.file, '_blank'); // 新开窗口下载
            alert('下载完成')
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
        delete_file: function(){
            this.$http.post(FileDeleteUrl, {},
                {"Content-Type": "multipart/form-data"}).then(function(res){
                var result = res.body
                if(result.code === 0){
                    console.log(result);
                    // this.content_imgs = data.images
                    // this.answer = data.answers
                    // this.difficulty = data.difficulty
                    // this.edit_difficulty = data.difficulty
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
        // 编辑模式 end
    }

})

var GetRequest = function() {
   var url = location.search; //获取url中"?"符后的字串
   var theRequest = {}
   if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}
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
        delete_example_imgs: [], //删除图片id
        delete_answer: [], //删除答案id
        is_edit: false, // 模式 是否为编辑模式

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
                        console.log(data);
                        this.content = data.content
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
                id:current_category_lead[i-1].id}
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
        add_delete_img: function(example_img_id){
            var i = this.delete_example_imgs.indexOf(example_img_id)
            if( i< 0){
                this.delete_example_imgs.push(example_index)
            }else {
                this.delete_example_imgs.splice(i, 1)
            }
        },
        add_delete_answers: function(answer_id){

        },
        submit_input: function(){
            if(!this.content){
                alert('请输入提干')
                return
            };
            if(!this.add_answer){
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
            form.append('add_answer', this.add_answer)

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
                        alert(result.desc)
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

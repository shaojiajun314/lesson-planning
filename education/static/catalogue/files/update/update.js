var args = GetRequest();
var file_id = args.file_id
var type = args.type
var FileDetailUrl = api.FileDetail.replace(/{type}/, type).replace(/{pk}/, file_id)
var FileDeleteUrl = api.DeleteFile.replace(/{type}/, type).replace(/{pk}/, file_id)

new Vue({
    el: '#file-update',
    data: {
        file_data: {},
        current_category: {name:'', id: null},
        permissions_modify: false
    },
    created: function () {
      this.get_file_detail(file_id);
      this.permissions_modify = Nav.user && Nav.user.permissions[{
          'courseware': 'modify_courseware',
          'examination_outline': 'modify_examinationoutline'
      }[type]]
    },
    methods: {
        // 查询模式 start
        get_file_detail: function(pk){
            this.$http.get(FileDetailUrl).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        var data = result.data
                        this.file_data = data
                        this.handle_categories(data.categories)
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

        delete_file: function(){
            this.$http.post(FileDeleteUrl, {},
                {"Content-Type": "multipart/form-data"}).then(function(res){
                var result = res.body
                if(result.code === 0){
                    Modal.is_hidden = false
                    Modal.title = '删除成功'
                    Modal.body = '请选择跳转页面'
                    Modal.cancel = '首页'
                    Modal.cancel_func = function(){
                        window.location.href =　'/'
                    }
                    Modal.sure = '文件查询'
                    Modal.sure_func = function(){
                        window.location.href =
                            '/static/catalogue/files/query/query.html?type=' + type
                    }
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

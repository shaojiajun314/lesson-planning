var category_id = GetRequest().category_id;

new Vue({
    el: '#category-update',
    data: {
        current_category_path:[],

        name:'',
        img_url: ''
    },
    created: function () {

        this.init_data(category_id)
    },
    methods: {
        init_data: function(category_id){
            if(category_id){
                category_pk = category_id + '/' // url 请求拼接
            }else {
                category_pk = '';
            }
            if(!category_id){
                this.current_category_path = [];
                return ;
            }
            this.$http.get(api.AncestorsCategory.replace(/{category_pk}/, category_id))
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.current_category_path = result.data
                        var this_category = result.data[result.data.length-1]
                        this.name = this_category.name
                        this.img_url = this_category.image
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        change_category: function(categoryid){
            window.location.href =
                '/static/catalogue/category/update/update.html?category_id=' + categoryid
        },

        submit_input: function(){
            if(!this.name){
                alert('请输入新分类名称')
                return
            };

            var form = new FormData()
            if(this.$refs.imgInput.files.length !== 0) {
                form.append('img', this.$refs.imgInput.files[0])
            }
            form.append('name', this.name)

            this.$http.post(api.UpdateCategory.replace(/{pk}/, category_id),
                form, {"Content-Type": "multipart/form-data"}).then(function(res){
                    var result = res.body
                    if(result.code === 0){

                        Modal.is_hidden = false
                        Modal.title = '修改成功'
                        Modal.body = '请选择跳转页面'
                        Modal.cancel = '留在本页'
                        Modal.cancel_func = function(){
                            window.location.reload()
                        }
                        Modal.sure = '返回首页'
                        Modal.sure_func = function(){
                            window.location.href =　'/'
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

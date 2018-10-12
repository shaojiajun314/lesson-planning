var args = GetRequest()
var category_id = args.category_id;
var type = args.type;
var Files_url = api.Files.replace(/{type}/, type)
Nav.index = index = {
    courseware: 4,
    examination_outline: 5
}[type]

var category = new Vue({
    el: '#category',
    data: {
        category: [],
        clean_key: true
    },
    created: function () {
      this.get_category_root();
    },
    methods: {
        get_category_root: function(){
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
            this.clean_key = false
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
        query_file: function(category_id){
            files_list.files = []
            files_list.next_link = api.Files.replace(/{category_pk}/, (category_id + '/')).replace(/{type}/, type)
            files_list.get_files()
            files_list.get_ancestors_category(category_id)
        },
        clean_category: function(){
            this.clean_key = true
            var that = this
            setTimeout(function() {
                if(that.clean_key){
                    that.category = that.category.slice(0, 1)
                }
            }, 300)
        }
    }
})

var files_list = new Vue({
    el: '#file-list',
    data: {
        files: [],
        next_link: null,
        // answer_key_list: [],
        is_assembly: false,
        current_category_path: [],
        category_id: '',

        order_by: '',
        order: '',
    },
    created: function () {
        if(category_id){
            category_pk = category_id + '/' // url 请求拼接
        }else {
            category_pk = '';
        }
        this.next_link = Files_url.replace(/{category_pk}/, category_pk)
        this.get_files()
        this.get_ancestors_category(category_id)
    },
    methods: {
        get_ancestors_category: function(category_id){
            if(!category_id){
                this.current_category_path = [];
                return ;
            }
            this.category_id = category_id
            this.$http.get(api.AncestorsCategory.replace(/{category_pk}/, category_id))
                .then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.current_category_path = result.data
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        change_category: function(category_id) {
            if(category_id){
                category_pk = category_id + '/' // url 请求拼接
            }else {
                category_pk = '';
            }
            this.category_id = category_id ? category_id : '';
            this.files = []
            this.next_link = Files_url.replace(/{category_pk}/, category_pk)
            this.get_files()
            this.get_ancestors_category(category_id)
        },
        get_files: function(){
            if(! this.next_link){
                alert('没有更多了')
                return;
            }
            this.$http.get(this.next_link, {params: {}}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.next_link = result.data.next_link;
                        this.files = this.files.concat(result.data.files)
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        get_file_detail: function(file_id) {
            window.location.href = '/static/catalogue/files/update/update.html?file_id=' + file_id
        },
    },
})

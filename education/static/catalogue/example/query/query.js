Nav.index = 1

var category_id = GetRequest().category_id;

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
        query_example: function(category_id){
            examples_list.examples = []
            // examples_list.answer_key_list = []
            examples_list.next_link = api.Examples.replace(/{category_pk}/, (category_id + '/'))
            examples_list.get_examples()
            examples_list.get_ancestors_category(category_id)
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

var example_assemble_limit = 60;// 每次选题
var examples_list = new Vue({
    el: '#example-list',
    data: {
        examples: [],
        next_link: null,
        // answer_key_list: [],
        is_assembly: false,
        assembled_example: [],
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
        this.next_link = api.Examples.replace(/{category_pk}/, category_pk)
        this.get_examples()
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
            this.examples = []
            // this.answer_key_list = []
            this.next_link = api.Examples.replace(/{category_pk}/, category_pk)
            this.get_examples()
            this.get_ancestors_category(category_id)
        },
        get_examples: function(){
            if(! this.next_link){
                alert('没有更多了')
                return;
            }
            console.log(this.order + this.order_by,1231313);
            this.$http.get(this.next_link, {params: { 'order_by': (this.order + this.order_by)}}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        this.next_link = result.data.next_link;
                        this.examples = this.examples.concat(result.data.examples)
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });
        },
        get_example_detail: function(example_id) {
            window.location.href = '/static/catalogue/example/update/update.html?example_id=' + example_id
            // var i = this.answer_key_list.indexOf(example_index)
            // if( i< 0){
            //     this.answer_key_list.push(example_index)
            // }else {
            //     this.answer_key_list.splice(i, 1)
            // }
        },

        change_assembly: function(){
            this.is_assembly = !this.is_assembly
            this.assembled_example = []
        },
        change_assembly_checked: function(example_id){
            var i = this.assembled_example.indexOf(example_id)
            if( i< 0){
                if(this.assembled_example.length >= example_assemble_limit){
                    alert('限选'+example_assemble_limit+'题')
                    return ;
                }
                this.assembled_example.push(example_id)
            }else {
                this.assembled_example.splice(i, 1)
            }
        },
        download_docx: function(){
            if(this.assembled_example.length == 0){
                alert('请先选题')
                return ;
            }
            var args = this.assembled_example.join('-')
            var url = api.DownloadAssembledExamples + '?example_ids=' + args + '&v=' + Math.random().toString(36).substring(2)
            window.open(url, '_blank'); // 新开窗口下载
            alert('下载完成')
            this.change_assembly()
        },
        change_order: function(field){
            if(this.order_by == field){
                this.order = this.order ? '' : '-';
                console.log(this.order);
            }else {
                this.order_by = field;
                this.order = '';
            };
            if(this.category_id){
                category_pk = this.category_id + '/' // url 请求拼接
            }else {
                category_pk = '';
            }
            this.examples = []
            this.next_link = api.Examples.replace(/{category_pk}/, category_pk)
            // examples_list.answer_key_list = []
            this.get_examples()
        }
    },
})

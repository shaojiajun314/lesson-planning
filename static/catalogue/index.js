new Vue({
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
        query_example: function(example_id){
            console.log(example_id);
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

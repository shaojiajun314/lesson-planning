new Vue({
    el: '#category-create',
    data: {
        category: [],
        name:'',
        parent_category: {name:'', id: null}
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
            console.log(123);
            this.category = []
        },
        input_parent: function(id, name){
            console.log(id, name);
            this.parent_category = {name:name, id:id}
        },
        submit_input: function(){
            console.log(123132123);
            if(!this.name){
                alert('请输入新分类名称')
                return
            };
            if(this.parent_category.id){
                parent_id = this.parent_category.id + '/' //url拼接需要
            }else {
                parent_id = ''
            }
            this.$http.post(api.CreateCategory.replace(/{parent_id}/, parent_id),
                {name:this.name}, {emulateJSON:true}).then(function(res){
                    var result = res.body
                    if(result.code === 0){
                        alert(result.desc)
                    }else {
                        alert(result.desc)
                    }
                },function(){
                    alert('请求错误');
                });

        }
    }
})
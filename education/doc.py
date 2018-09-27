文档
################################################################################
#                              分类                                            #
################################################################################

分类创建：
    url: api/catalogue/category/(?:(?P<parent_pk>\d+)/)?create/
    kw: parent_pk(父节点id，不填创建根目录)
    arg: {name: '分类名称'}

分类更新：
    url: api/catalogue/category/(?P<pk>\d+)/update/
    kw: pk(节点id)
    arg: {name: '分类名称'}

分类列表：
    url: api/catalogue/category/(?:(?P<parent_pk>\d+)/)?list/
    kw: parent_pk(父节点id，不填获取根目录列表)

################################################################################
#                              题目                                            #
################################################################################

创建题目:
    url: api/catalogue/example/create/
    arg: {category_id: '分类id',
         content: '题目内容',
         answer: '初始化答案1内容'}

更新题目:
    url: api/catalogue/example/(?P<pk>\d+)/update/
    kw: pk(题目id)
    arg: {content: '题目内容'}

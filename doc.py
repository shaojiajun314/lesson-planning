文档

<注:>
    返回值:
        {'msg': 'success', #英文描述
        'desc': 'success',　#中文描述
        'code': 0, # 0请求成功　其他均失败具体原因查看desc及msg
        'data': {} # 返回数据
        }

################################################################################
#                              用户                                            #
################################################################################

注册：
    url: api/user/register/
    arg: {username: '帐号', password: '密码'}
    data: {'username': '帐号',
        'nickname': '昵称',
        'mobile': '手机号'}
    }

登入：
    url: api/user/login/
    arg: {username: '帐号', password: '密码'}
    data: {'username': '帐号',
        'nickname': '昵称',
        'mobile': '手机号'}
    }
################################################################################
#                              分类                                            #
################################################################################

分类创建：
    url: api/catalogue/category/(?:(?P<parent_pk>\d+)/)?create/
    kw: parent_pk(父节点id，不填创建根目录)
    arg: {name: '分类名称', 'img': '图片'}

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
         answer: '初始化答案1内容',
         'content_img*': '题干图片', #　可多张　例如：content_img0, content_img1
         'answer_img*': '答案图片', #　同上
         }

更新题目:
    url: api/catalogue/example/(?P<pk>\d+)/update/
    kw: pk(题目id)
    arg: {content: '题目内容'}

// const HTTPRootUrl = 'http://127.0.0.1:8000'
// const HTTPSRootUrl = 'http://127.0.0.1:8000'
const HTTPRootUrl = ''
const HTTPSRootUrl = ''

const ApiRootUrl = HTTPSRootUrl + '/api/';

const api = {
    CategoryRoot: ApiRootUrl + 'catalogue/category/query/',
    Category: ApiRootUrl + 'catalogue/category/{parent_pk}/query/',
    CreateCategory: ApiRootUrl + 'catalogue/category/{parent_id}create/',
    UpdateCategory: ApiRootUrl + 'catalogue/category/{pk}/update/',
    AncestorsCategory: ApiRootUrl + 'catalogue/category/{category_pk}/ancestors/query/',

    CreateExample: ApiRootUrl + 'catalogue/example/create/',
    UpdateExample: ApiRootUrl + 'catalogue/example/{pk}/update/',
    Examples: ApiRootUrl + 'catalogue/category/{category_pk}examples/query/',
    ExampleDetail: ApiRootUrl + 'catalogue/example/{pk}/query/',
    DownloadAssembledExamples: ApiRootUrl + 'catalogue/examples/docx/create/',

    Register: ApiRootUrl + 'user/register/',
    Login: ApiRootUrl + 'user/login/',
    Logout: ApiRootUrl + 'user/logout/',

    DashboardUsersPermissions: ApiRootUrl + 'dashboard/permission/users/query/',
    DashboardUsersPermissionsCreate: ApiRootUrl + 'dashboard/permission/users/create/',
    DashboardUsersPermissionsDelete: ApiRootUrl + 'dashboard/permission/users/{username}/delete/'
}

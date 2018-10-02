// const HTTPRootUrl = 'http://127.0.0.1:8000'
// const HTTPSRootUrl = 'http://127.0.0.1:8000'
const HTTPRootUrl = ''
const HTTPSRootUrl = ''

const ApiRootUrl = HTTPSRootUrl + '/api/';

const api = {
    CategoryRoot: ApiRootUrl + 'catalogue/category/list/',
    Category: ApiRootUrl + 'catalogue/category/{parent_pk}/list/',
    CreateCategory: ApiRootUrl + 'catalogue/category/{parent_id}create/',

    CreateExample: ApiRootUrl + 'catalogue/example/create/',
    Examples: ApiRootUrl + 'catalogue/category/{category_pk}examples/list/',
}

const HTTPRootUrl = 'http://127.0.0.1:8000'
const HTTPSRootUrl = 'http://127.0.0.1:8000'

const ApiRootUrl = HTTPSRootUrl + '/api/';

const api = {
    CategoryRoot: ApiRootUrl + 'catalogue/category/list/',
    Category: ApiRootUrl + 'catalogue/category/{parent_pk}/list/'
}

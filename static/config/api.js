// const HTTPRootUrl = 'http://127.0.0.1:8000'
// const HTTPSRootUrl = 'http://127.0.0.1:8000'
const HTTPRootUrl = ''
const HTTPSRootUrl = ''

const ApiRootUrl = HTTPSRootUrl + '/api/';

const api = {
    CategoryRoot: ApiRootUrl + 'catalogue/category/query/',
    Category: ApiRootUrl + 'catalogue/category/{parent_pk}/query/',
    CreateCategory: ApiRootUrl + 'catalogue/category/{parent_id}create/',
    AncestorsCategory: ApiRootUrl + 'catalogue/category/{category_pk}/ancestors/query/',

    CreateExample: ApiRootUrl + 'catalogue/example/create/',
    Examples: ApiRootUrl + 'catalogue/category/{category_pk}examples/query/',
    DownloadAssembledExamples: ApiRootUrl + 'catalogue/examples/docx/create/',
}

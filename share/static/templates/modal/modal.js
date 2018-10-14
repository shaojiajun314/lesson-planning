Vue.component('modal', {
    props: ['title', 'body', 'cancel', 'sure', 'cancel_func', 'sure_func'],
    template: '<div class="modal-content"> \
             <header class="modal-header"> \
                  <h4>{{title}}</h4> \
             </header> \
             <div class="modal-body"> \
                  <p>{{body}}</p> \
             </div> \
             <footer class="modal-footer"> \
                  <button id="cancel" @click="cancel_func()">{{cancel}}</button> \
                   <button id="sure" @click="sure_func">{{sure}}</button> \
             </footer> \
        </div>',
})

// html
// <div id="modal"  class="modal"  v-bind:class="{'hidden': is_hidden}">
//     <modal v-bind:title="title" v-bind:body="body"
//         v-bind:cancel="cancel" v-bind:sure="sure"
//         v-bind:cancel_func="cancel_func"
//         v-bind:sure_func="sure_func">
//     </modal>
// </div>

// data = {
//     is_hidden:false,
//     title:'body',
//     body: 'body',
//     cancel: 'test_cancel',
//     sure: 'sure',
//     cancel_func: function(){
//         console.log('can');
//     },
//     sure_func: function(){
//         console.log('sur');
//     }
// }
var Modal = new Vue({
    el: '#modal',
    data: {
        is_hidden:true,
        title:'',
        body: '',
        cancel: '',
        sure: '',
        cancel_func: function(){},
        sure_func: function(){}
      },
})

import DataExample from '../views/DataExample.vue'
import DrivingParam from '../views/DrivingParam.vue'
import SurroundingRock from '../views/SurroundingRock.vue'
import VueRouter from "vue-router"; 
import Vue from 'vue'

Vue.use(VueRouter);
const routes = [
    {
        path: '/data-example',
        component: DataExample,
    },
    {
        path: '/driving-param',
        component: DrivingParam,
    },
    {
        path: '/surrounding-rock',
        component: SurroundingRock,
    },
];

var router = new VueRouter({
    routes: routes,
    mode: "history",
  });
export default router;
import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./assets/main.css"
import App from "./App.vue";
import router from "./router";
import axios from 'axios'
import VueAxios from "vue-axios"

const app = createApp(App);

app.use(VueAxios, axios)
app.use(router);
app.use(ElementPlus);
// app.use(axios)
app.mount("#app");

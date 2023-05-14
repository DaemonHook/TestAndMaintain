import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./assets/main.css"
import App from "./App.vue";
import router from "./router";
import service from "./service";
const app = createApp(App);

app.use(router);
app.use(ElementPlus);
app.config.globalProperties.api = service
// app.use(axios)
app.mount("#app");

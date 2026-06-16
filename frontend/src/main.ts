import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// Import styles
import './assets/styles/main.css';

// Import fonts
import './assets/styles/fonts.css';

// Import print styles (only for print)
import './assets/styles/print.css';

const app = createApp(App);

// Plugins
app.use(createPinia());
app.use(router);

// Mount
app.mount('#app');
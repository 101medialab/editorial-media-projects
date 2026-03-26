import { createApp } from 'vue'
import './style.css'
import Main from './Main.vue'
import { register } from 'swiper/element/bundle'

register()
createApp(Main).mount('#app')

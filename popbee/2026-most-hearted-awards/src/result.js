import { createApp } from 'vue'
import './style.css'
import Result from './Result.vue'
import { register } from 'swiper/element/bundle'

register()
createApp(Result).mount('#app')

<template>
  <section class="section-result pt-[58px] pb-[80px]" :style="config.background ? { backgroundColor: config.background } : {}">
    <div class="logo-wrapper flex align-center justify-center mb-[60px]">
      <img
          :src="`${PUBLIC_URL}result/${config.logo ?? 'logo-white.svg'}`"
          alt="Most Hearted Awards 2026"
          class="w-[130px]"
      />
    </div>
    <swiper-container ref="swiperEl" init="false">
      <swiper-slide v-for="item in config.items" :key="item.id">
        <SectionItem :item="item" :box="config.box" />
      </swiper-slide>
    </swiper-container>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {PUBLIC_URL} from "~/constants.js";
import SectionItem from '~/components/Result/SectionItem.vue'

const props = defineProps({
  config: {
    type: Object,
    required: true,
  },
})

const swiperEl = ref()

const swiperParams = {
  slidesPerView: 'auto',
  spaceBetween: 15,
  centerInsufficientSlides: true,
  slidesOffsetBefore: 15,
  slidesOffsetAfter: 15,
  mousewheel: {
    forceToAxis: true,
  },
  breakpoints: {
    1024: {
      spaceBetween: 105,
      slidesOffsetBefore: 30,
      slidesOffsetAfter: 30,
    },
  },
}

onMounted(() => {
  Object.assign(swiperEl.value, swiperParams)
  swiperEl.value.initialize()
})
</script>

<style scoped lang="scss">
.section-result {
  width: 100%;

  :deep(swiper-slide) {
    width: fit-content;
  }
}
</style>

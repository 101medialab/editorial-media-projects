<template>
  <section class="section-result pt-[58px] pb-[80px]" :style="config.background ? { backgroundColor: config.background } : {}">
    <div class="logo-wrapper flex align-center justify-center mb-[60px]">
      <img
          :src="`${PUBLIC_URL}result/${config.logo ?? 'logo-white.svg'}`"
          alt="Most Hearted Awards 2026"
          class="w-[130px]"
      />
    </div>
    <div class="slider-wrapper relative">
      <swiper-container ref="swiperEl" init="false">
        <swiper-slide v-for="item in config.items" :key="item.id">
          <SectionItem :item="item" :box="config.box" :section="config.id" />
        </swiper-slide>
      </swiper-container>
      <div
        class="shelf-wrapper absolute bottom-[10px] left-0 w-full h-[93px] pointer-events-none"
        :class="isPartTwo ? 'bottom-[15px]' : 'bottom-[20px]'"
        :style="{ backgroundImage: `url(${PUBLIC_URL}result/shelf_v2.png)`, backgroundRepeat: 'repeat-x', backgroundSize: 'auto 93px' }"
      />
    </div>
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

const isPartTwo = props.config.id === 'part-two'

const swiperParams = {
  slidesPerView: 'auto',
  spaceBetween: 30,
  centeredSlides: true,
  centerInsufficientSlides: true,
  slidesOffsetBefore: 15,
  slidesOffsetAfter: 15,
  mousewheel: {
    forceToAxis: true,
  },
  breakpoints: {
    768: {
      centeredSlides: false,
    },
    1200: {
      centeredSlides: false,
      // slidesPerView: props.config.items.length,
      spaceBetween: isPartTwo ? 90 : 105,
      slidesOffsetBefore: 0,
      slidesOffsetAfter: 0,
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

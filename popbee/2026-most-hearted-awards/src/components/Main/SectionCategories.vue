<template>
  <section class="section-categories pt-[61px] pb-[60px]">
    <div class="container mb-[30px]">
      <h2
        class="font-bodndi mb-[20px] text-center text-[60px] tracking-normal normal-case italic md:text-[60px]"
      >
        Voting Categories
      </h2>
      <p class="text-center text-base leading-6">
        我們從 10 個類別中精選出最受關注的選項，請於每個類別中選出 3
        個最喜愛的選項，為它們加油打氣。
      </p>
    </div>

    <swiper-container ref="swiperEl" init="false">
      <swiper-slide
        v-for="{ id, 'short-name': shortName, image } in config.slice(0, -3)"
        :key="`category-${id}`"
        class="w-[160px] md:max-w-[167px]"
      >
        <div class="relative aspect-[3/4] overflow-hidden rounded-[20px]">
          <a
            class="absolute inset-0 z-20"
            :href="`#category-${id}`"
            @click="scrollParentToChildEl"
          ></a>
          <img
            :src="`${PUBLIC_URL}${image}`"
            :alt="shortName"
            class="h-full w-full object-cover"
          />
          <p
            class="font-bodndi absolute inset-0 z-10 flex items-center justify-center text-center text-[18px] leading-[1.2] text-white italic md:text-[22px]"
          >
            {{ shortName }}
          </p>
        </div>
      </swiper-slide>
    </swiper-container>
  </section>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { PUBLIC_URL } from '~/constants'

defineProps({
  config: {
    type: Array,
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
    768: {
      spaceBetween: 20,
      slidesOffsetBefore: 30,
      slidesOffsetAfter: 30,
    },
  },
}

const pymChild = inject('pymChild')
const scrollOffset = inject('scrollOffset')

const scrollParentToChildEl = (e) => {
  e.preventDefault()
  const id = e.target.hash

  const topPos =
    document.querySelector(id).getBoundingClientRect().top +
    window.scrollY -
    scrollOffset.value
  pymChild.value.scrollParentToChildPos(topPos)
}

onMounted(() => {
  Object.assign(swiperEl.value, swiperParams)
  swiperEl.value.initialize()
})
</script>

<style scoped>
.section-categories {
  background-image: url('/categories-bg.jpg');
  background-size: cover;
  background-position: center top;
}
</style>

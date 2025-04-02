<template>
  <section class="bg-categories pt-[61px] pb-[60px]">
    <div class="container max-w-[800px] text-center">
      <div class="mb-[30px]">
        <h2
          class="mb-[10px] text-[46px] tracking-[-1.8px] uppercase md:text-[60px]"
        >
          Most Hearted
        </h2>
        <p class="mb-[20px]">By POPBEE Audiences</p>
        <p>
          POPBEE 誠意呈獻&mdash;Most-Hearted
          Awards！這是一場由你決定的時尚與潮流大賞，我們精選了過去一年內在
          POPBEE 網站上最受關注的關鍵字，並將它們分為 7
          個不同類別，讓你來為最愛的選項送上「愛心」支持。我們還加入了編輯評分環節，讓專業觀點為這場投票增添更多參考依據。無論是影響力非凡的明星、引領潮流的時尚單品、不可或缺的美妝單品，還是備受矚目的運動單品、閃耀動人的珠寶及令人期待的新興品牌&mdash;這一次，你的選擇將決定誰是最受歡迎的
          Most-Hearted 之選！
        </p>
      </div>

      <div class="mb-[30px]">
        <h3
          class="mb-[20px] text-[28px] tracking-[-1.44px] italic md:text-[36px]"
        >
          How to Vote
        </h3>
        <p>
          我們從 7 個類別中精選出最受關注的選項，請於每個類別中選出 3
          個最喜愛的選項，為它們加油打氣。
        </p>
      </div>
    </div>

    <swiper-container ref="swiperEl" init="false">
      <swiper-slide
        v-for="{ id, 'short-name': shortName, image } in config"
        :key="`category-${id}`"
        class="@container w-[100px] md:w-[176px]"
      >
        <div
          class="relative overflow-hidden rounded-[14px] after:absolute after:inset-0 after:bg-black/60 after:transition-opacity after:duration-300 after:content-[''] hover:after:opacity-0"
        >
          <a
            class="absolute inset-0 z-20"
            :href="`#category-${id}`"
            @click="scrollParentToChildEl"
          ></a>
          <img :src="`${PUBLIC_URL}${image}`" :alt="shortName" />
          <div
            class="absolute top-1/2 left-1/2 z-10 -translate-x-1/2 -translate-y-1/2 transform"
          >
            <img
              class="w-[85.3cqw] max-w-none"
              :src="`${PUBLIC_URL}oval-sm.svg`"
              alt="oval"
            />
            <p
              class="font-bodndi absolute top-1/2 left-1/2 mt-[2px] -translate-x-1/2 -translate-y-1/2 transform text-center text-[14px] leading-[14px] uppercase md:text-[24px] md:leading-[21.6px]"
            >
              {{ shortName }}
            </p>
          </div>
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
    window.pageYOffset -
    scrollOffset.value
  pymChild.value.scrollParentToChildPos(topPos)
}

onMounted(() => {
  Object.assign(swiperEl.value, swiperParams)
  swiperEl.value.initialize()
})
</script>

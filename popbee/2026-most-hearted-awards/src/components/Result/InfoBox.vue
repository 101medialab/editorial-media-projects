<template>
  <div class="result-announcement-info-box relative overflow-hidden lg:min-h-[614px]">

    <div class="ra-inner-wrapper">
      <h1 class="text-[46px] md:text-[60px]">Result Announcement</h1>

      <div class="ra-board">
        <p>感謝所有參與 POPBEE Most-Hearted Award 的讀者，這場由大家決定的潮流盛事終於揭曉！我們根據各位 POPBEE
          編輯及讀者的投票結果，整理出 10 大類別中最受歡迎的 Most-Hearted 之選。</p>

        <p>無論是時尚迷熱愛的單品、話題度最高的明星，還是美妝界的經典之選，每一個入選者都代表了過去一年來最受關注的潮流趨勢。快來看看你的
          Most-Hearted 之選是否成功上榜，一起回顧這些最受讀者喜愛的時尚、單品與品牌吧！</p>
        <!-- Corner screws (plaque aesthetic) -->
        <img :src="`${PUBLIC_URL}result/screw.png`" alt="" aria-hidden="true" class="screw screw-tl" />
        <img :src="`${PUBLIC_URL}result/screw.png`" alt="" aria-hidden="true" class="screw screw-tr" />
        <img :src="`${PUBLIC_URL}result/screw.png`" alt="" aria-hidden="true" class="screw screw-bl" />
        <img :src="`${PUBLIC_URL}result/screw.png`" alt="" aria-hidden="true" class="screw screw-br" />
      </div>
    </div>
    <img
        v-for="img in decorativeImages"
        :key="img.src"
        :src="`${PUBLIC_URL}${img.src}`"
        alt=""
        aria-hidden="true"
        class="absolute pointer-events-none"
        :style="isMobile ? img.mobile : isTablet ? img.tablet : img.desktop"
    />
  </div>
</template>
<style scoped lang="scss">
$navy: #1E3160;
$screw-inset: 14px;

.result-announcement-info-box {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #F2F2F0;
}

.ra-inner-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  padding: 60px 10%;
  text-align: center;
  width: 100%;

  h1 {
    font-family: var(--font-bodndi);
    font-style: italic;
    font-weight: 400;
    color: $navy;
    line-height: 1;
    letter-spacing: -0.02em;
  }

  @media (min-width: 100rem) {
    padding: 60px 22%;
  }

  @media (min-width: 48.0625rem) and (max-width: 64rem) {
    padding: 60px 40px;
  }

  @media (max-width: 48rem) {
    padding: 120px 15px;
    gap: 50px;
  }
}

.ra-board {
  position: relative;
  background: #ffffff;
  border: 1.5px solid #333;
  padding: 52px 56px;
  width: 100%;
  max-width: 760px;
  box-shadow: 6px 8px 7.5px 0 #00000040;

  p {
    font-family: var(--font-notos-tc), sans-serif;
    color: $navy;
    font-size: 16px;
    line-height: 150%;
    text-align: center;

    & + p {
      margin-top: 20px;
    }
  }

  .screw {
    position: absolute;
    width: 22px;
    height: 22px;
    pointer-events: none;

    &-tl { top: $screw-inset;    left: $screw-inset;  }
    &-tr { top: $screw-inset;    right: $screw-inset; }
    &-bl { bottom: $screw-inset; left: $screw-inset;  }
    &-br { bottom: $screw-inset; right: $screw-inset; }
  }

  @media (max-width: 64rem) {
    padding: 40px 28px;
    max-width: 600px;
  }
}
</style>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { PUBLIC_URL } from '~/constants.js'

const decorativeImages = [
  {
    src: 'result/1.png',
    desktop: { left: '-20px', top: '20px', width: '230px', objectFit: 'contain' },
    tablet:  { left: '-20px', top: '20px', width: '230px', objectFit: 'contain' },
    mobile:  { left: '-20px', top: '-20px', width: '140px', objectFit: 'contain' },
  },
  {
    src: 'result/2.png',
    desktop: { right: '55px', top: '20px', width: '260px', objectFit: 'contain' },
    tablet:  { right: '0', top: '25px', width: '200px', objectFit: 'contain' },
    mobile:  { right: '-30px', top: '2.9%', width: '140px', objectFit: 'contain' },
  },
  {
    src: 'result/3.png',
    desktop: { left: '100px', bottom: '-20px', width: '100px', objectFit: 'contain' },
    tablet:  { left: '60px', bottom: '-15px', width: '100px', objectFit: 'contain' },
    mobile:  { left: '30px', bottom: '-40px', width: '70px', objectFit: 'contain' },
  },
  {
    src: 'result/4.png',
    desktop: { right: '-65px', bottom: '-55px', width: '260px', transformOrigin: 'center', objectFit: 'contain' },
    tablet:  { right: '-65px', bottom: '-55px', width: '260px', transformOrigin: 'center', objectFit: 'contain' },
    mobile:  { right: '-100px', bottom: '-100px', width: '200px', transformOrigin: 'center', objectFit: 'contain' },
  },
]

const isMobile = ref(false)
const isTablet = ref(false)
let mqMobile, mqTablet
const onMobileChange = (e) => { isMobile.value = e.matches }
const onTabletChange = (e) => { isTablet.value = e.matches }

onMounted(() => {
  mqMobile = window.matchMedia('(max-width: 48rem)')
  mqTablet = window.matchMedia('(min-width: 48.0625rem) and (max-width: 64rem)')
  isMobile.value = mqMobile.matches
  isTablet.value = mqTablet.matches
  mqMobile.addEventListener('change', onMobileChange)
  mqTablet.addEventListener('change', onTabletChange)
})

onUnmounted(() => {
  mqMobile?.removeEventListener('change', onMobileChange)
  mqTablet?.removeEventListener('change', onTabletChange)
})
</script>

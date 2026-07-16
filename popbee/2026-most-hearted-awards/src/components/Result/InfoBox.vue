<template>
  <div class="result-announcement-info-box relative overflow-hidden lg:min-h-[614px]">

    <div class="ra-inner-wrapper">
      <h1>Result Announcement</h1>

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
    <!-- Top-left product (1.png — tall portrait) -->
    <img
        :src="`${PUBLIC_URL}result/1.png`"
        alt=""
        aria-hidden="true"
        class="absolute pointer-events-none"
        style="left: -3.6%; top: 5.6%; width: 16.1%; object-fit: contain;"
    />

    <!-- Top-right product (2.png — wide landscape) -->
    <img
        :src="`${PUBLIC_URL}result/2.png`"
        alt=""
        aria-hidden="true"
        class="absolute pointer-events-none"
        style="left: 80.5%; top: 2.9%; width: 15.4%; object-fit: contain;"
    />

    <!-- Bottom-left product (3.png — tall portrait) -->
    <img
        :src="`${PUBLIC_URL}result/3.png`"
        alt=""
        aria-hidden="true"
        class="absolute pointer-events-none"
        style="left: 5%; top: 61.4%; width: 7.5%; object-fit: contain;"
    />

    <!-- Bottom-right product (4.png — rotated) -->
    <img
        :src="`${PUBLIC_URL}result/4.png`"
        alt=""
        aria-hidden="true"
        class="absolute pointer-events-none"
        style="left: 85.6%; top: 56.1%; width: 20%; transform-origin: center; object-fit: contain;"
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
  padding: 60px 22%;
  text-align: center;
  width: 100%;

  h1 {
    font-family: var(--font-bodndi);
    font-style: italic;
    font-size: 60px;
    font-weight: 400;
    color: $navy;
    line-height: 1;
    letter-spacing: -0.02em;
  }

  @media (max-width: 48rem) {
    padding: 50px 8%;
    gap: 50px;
  }
}

.ra-board {
  position: relative;
  background: #ffffff;
  border: 1.5px solid $navy;
  padding: 52px 56px;
  width: 100%;
  max-width: 760px;
  box-shadow: 6px 8px 7.5px 0 #00000040;

  p {
    font-family: var(--font-notos-tc), sans-serif;
    color: $navy;
    font-size: 15px;
    line-height: 1.9;
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

  @media (max-width: 48rem) {
    padding: 40px 28px;

    p {
      font-size: 13px;
      line-height: 1.8;
    }
  }
}
</style>
<script setup>
import {PUBLIC_URL} from "~/constants.js";
</script>

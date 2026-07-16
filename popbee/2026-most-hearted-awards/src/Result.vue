<template>
  <div ref="root">
    <section class="main-banner">
      <img
          :src="`${PUBLIC_URL}result/m-hero-banner.jpg`"
          alt="Most Hearted Awards 2026"
          class="w-full sm:hidden"
      />
      <img
          :src="`${PUBLIC_URL}result/hero-banner.jpg`"
          alt="Most Hearted Awards 2026"
          class="hidden w-full sm:block"
      />
    </section>

    <InfoBox />

    <SectionResult
      v-for="part in resultConfig"
      :key="part.id"
      :config="part"
    />
  </div>
</template>

<script setup>
import {ref, onMounted, provide} from 'vue'
import pym from 'pym.js'
import {PUBLIC_URL} from "~/constants.js";
import InfoBox from '~/components/Result/InfoBox.vue'
import SectionResult from '~/components/Result/SectionResult.vue'
import resultConfig from '~/result-config.json'

const pymChild = ref()
const scrollOffset = ref(0)
const viewportInfo = ref({
  width: 0,
  height: 0,
})

provide('pymChild', pymChild)
provide('scrollOffset', scrollOffset)
provide('viewportInfo', viewportInfo)

onMounted(() => {
  pymChild.value = new pym.Child({polling: 500})
  pymChild.value.onMessage('positionOffset', (offset) => {
    scrollOffset.value = +offset
  })
  pymChild.value.onMessage('viewport-iframe-position', (payload) => {
    const [width, height] = payload.split(' ')
    viewportInfo.value = {width: +width, height: +height}
  })
})
</script>

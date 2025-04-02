<template>
  <div ref="root">
    <section>
      <picture>
        <source media="(min-width: 768px)" :srcset="`${mainBannerLg}`" />
        <img
          class="w-full"
          :src="`${mainBannerSm}`"
          alt="Most Hearted Awards 2025"
        />
      </picture>
    </section>

    <SectionCategories />

    <div>
      <SectionCategory
        v-for="item in config"
        :id="`category-${item.id}`"
        :key="`section.category.${item.id}`"
        :config="item"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import pym from 'pym.js'
import mainBannerLg from '~/assets/most-hearted-award-result-banner-lg.jpg?w=2700'
import mainBannerSm from '~/assets/most-hearted-award-result-banner-sm.jpg'
import SectionCategories from '~/components/Result/SectionCategories.vue'
import SectionCategory from '~/components/Result/SectionCategory.vue'
import config from '~/config.json'

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
  pymChild.value = new pym.Child({ polling: 500 })
  pymChild.value.onMessage('positionOffset', (offset) => {
    scrollOffset.value = +offset
  })
  pymChild.value.onMessage('viewport-iframe-position', (payload) => {
    const [width, height] = payload.split(' ')
    viewportInfo.value = { width: +width, height: +height }
  })
})
</script>

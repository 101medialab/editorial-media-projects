<template>
  <div ref="root">
    <section class="main-banner">
      <img
          :src="`${PUBLIC_URL}mob-hero-banner.jpg`"
          alt="Most Hearted Awards 2026"
          class="w-full sm:hidden"
      />
      <img
          :src="`${PUBLIC_URL}hero-banner.jpg`"
          alt="Most Hearted Awards 2026"
          class="hidden w-full sm:block"
      />
    </section>

    <SectionCategories />

    <div>
      <SectionCategory
        v-for="(item, index) in config"
        :id="`category-${item.id}`"
        :key="`section.category.${item.id}`"
        :config="item"
      >
        <template #footer>
          <footer
            v-if="index === config.length - 1"
            class="mt-[60px] text-center"
          >
            <small class="text-[11px]"
              >* Design elements and background colors</small
            >
          </footer>
        </template>
      </SectionCategory>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import pym from 'pym.js'
import SectionCategories from '~/components/Result/SectionCategories.vue'
import SectionCategory from '~/components/Result/SectionCategory.vue'
import config from '~/config.json'
import {PUBLIC_URL} from "~/constants.js";

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

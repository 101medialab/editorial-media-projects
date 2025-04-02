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
        v-for="(item, index) in config"
        :id="`category-${item.id}`"
        :key="`section.category.${item.id}`"
        :config="item"
      >
        <template #footer>
          <footer v-if="index === config.length - 1" class="mt-[60px]">
            <div class="mb-[30px]">
              <button
                class="pointer-events-none min-w-[191px] rounded-full bg-[#AAA] px-[40px] py-[11px] text-base font-medium text-white"
              >
                投票已完結
              </button>
            </div>

            <p>
              <small class="text-[11px]"
                >* Images from Getty Images & Brands</small
              >
            </p>
          </footer>
        </template>
      </SectionCategory>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import pym from 'pym.js'
import mainBannerLg from '~/assets/most-hearted-award-banner-lg.jpg?w=2700'
import mainBannerSm from '~/assets/most-hearted-award-banner-sm.jpg'
import SectionCategories from '~/components/Preview/SectionCategories.vue'
import SectionCategory from '~/components/Preview/SectionCategory.vue'
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

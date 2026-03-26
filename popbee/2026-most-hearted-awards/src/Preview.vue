<template>
  <div ref="root">
    <section>
      <div
        class="w-full h-64 md:h-96 bg-gradient-to-r from-green-500 to-blue-500 flex items-center justify-center"
      >
        <h1 class="text-white text-4xl md:text-6xl font-bold text-center">
          Preview 2026
        </h1>
      </div>
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
                >* Design elements and background colors</small
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

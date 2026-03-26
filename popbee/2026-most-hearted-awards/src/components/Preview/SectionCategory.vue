<template>
  <section ref="el" :class="[bgColor]" class="py-[60px] text-center">
    <div class="mx-auto max-w-[1600px] px-[15px] md:px-[30px]">
      <header class="mb-[60px]">
        <p
          class="font-bodndi mb-[20px] text-[28px] leading-none tracking-[-1.44px] italic md:text-[36px]"
        >
          Most Hearted Awards
        </p>
        <h4 class="text-[46px] tracking-[-1.8px] uppercase md:text-[60px]">
          {{ name }}
        </h4>
      </header>

      <div class="group/category">
        <div
          class="grid grid-cols-2 justify-center gap-x-[15px] gap-y-[60px] sm:grid-cols-3 md:grid-cols-4 md:gap-x-[30px] xl:grid-cols-6"
        >
          <SectionItem
            v-for="item in items"
            :key="`section.${id}.${item.id}`"
            :item="item"
          />
        </div>
      </div>
      <slot name="footer" />
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import SectionItem from '~/components/Preview/SectionItem.vue'

const { config } = defineProps({
  config: {
    type: Object,
    required: true,
  },
})

const id = computed(() => config.id)
const bgColor = computed(() => config['bg-color'])
const name = computed(() => config.name)
const items = computed(() => config.items)
</script>

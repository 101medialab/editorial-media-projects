<template>
  <section ref="el" class="py-[60px] md:py-[80px]">
    <div
      class="mx-auto flex max-w-[1600px] flex-col px-[15px] md:px-[30px]"
      :class="isEven ? 'md:flex-row-reverse' : 'md:flex-row'"
    >
      <div
        class="title-wrapper mb-[40px] text-center md:mb-0 md:flex md:w-[195px] md:shrink-0 md:items-start md:justify-center"
      >
        <h4
          class="font-bodndi text-[46px] tracking-[-1.8px] text-white italic md:text-[60px] md:leading-none md:tracking-[-2.4px]"
          :class="isEven ? 'md:vertical-rl' : 'md:vertical-lr'"
        >
          {{ name }}
        </h4>
      </div>

      <div
        class="group/category flex-1"
        :class="{ selected: selectedItems.length }"
      >
        <div
          class="grid grid-cols-2 gap-x-[15px] gap-y-[60px] sm:grid-cols-3 md:gap-x-[60px]"
        >
          <SectionItem
            v-for="item in items"
            :key="`section.${id}.${item.id}`"
            class=""
            :item="item"
            :disabled="selectedItems.length >= VOTES_EACH_CATEGORY"
            ref="sectionItems"
            @selected="onSelected"
          />
        </div>
      </div>
      <div class="cate-spacing hidden md:block md:w-[120px] md:shrink-0"></div>
    </div>
    <slot name="footer" />
  </section>
</template>

<script setup>
import { computed, ref, useTemplateRef, inject } from 'vue'
import SectionItem from '~/components/Main/SectionItem.vue'
import { VOTES_EACH_CATEGORY } from '~/constants'

const { config, index } = defineProps({
  config: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['selected-items', 'auto-next-section'])

const isEven = computed(() => index % 2 !== 0)

const selectedItems = ref([])
const el = useTemplateRef('el')
const sectionItems = useTemplateRef('sectionItems')

const id = computed(() => config.id)
const name = computed(() => config.name)
const items = computed(() => config.items)

const autoNextSection = computed(
  () => selectedItems.value.length >= VOTES_EACH_CATEGORY,
)

defineExpose({
  el,
  id,
  autoNextSection,
})

const viewportInfo = inject('viewportInfo')

const onSelected = () => {
  selectedItems.value = sectionItems.value
    .filter((item) => item.selected)
    .map((item) => item.item)

  emit('selected-items', {
    id: id.value,
    items: selectedItems.value,
  })

  if (autoNextSection.value) {
    emit('auto-next-section')
  }
}
</script>

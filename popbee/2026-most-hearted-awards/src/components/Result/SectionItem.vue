<template>
  <div class="section-item">
    <div class="item-visual">
      <img
        :src="`${PUBLIC_URL}result/items/${item.image}`"
        :alt="item.title"
        class="product-img h-auto"
        :class="section === 'part-two' ? 'w-[225px]' : 'w-[271px]'"
      />
    </div>
  </div>
</template>

<script setup>
import { PUBLIC_URL } from '~/constants'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  box: {
    type: String,
    required: true,
  },
  section: {
    type: String,
    default: '',
  },
})
</script>

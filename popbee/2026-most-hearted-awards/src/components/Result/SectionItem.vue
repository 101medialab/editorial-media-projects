<template>
  <div class="section-item">
    <div class="item-visual flex justify-center items-center flex-col">
      <img
        :src="`${PUBLIC_URL}result/items/${item.image}`"
        :alt="item.title"
        class="product-img h-auto w-[271px]"
        :class="section === 'part-two' ? 'w-[225px]' : 'w-[271px]'"
      />
      <div class="name-tag relative w-[225px] mt-[11px]">
        <img
            :src="`${PUBLIC_URL}result/name-tag@2x.png`"
            :alt="item.title"
            class="w-full"
        />
        <div class="name-tag-inner absolute left-0 top-0 w-full h-full flex justify-center items-center px-[38px]">
          <div class="name-tag-text text-[#522A25] text-[16px]/[120%] text-center">{{ item.title }}</div>
        </div>
      </div>
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

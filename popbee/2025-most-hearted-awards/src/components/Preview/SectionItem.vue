<template>
  <div class="group/item flex flex-col">
    <div class="flex flex-1 flex-col">
      <div class="mb-[20px]">
        <div class="relative">
          <div class="absolute inset-0 pr-[6.2%] pl-[6.2%]">
            <div
              :style="{ '--mask-asset-url': `url(${PUBLIC_URL}item/mask.svg)` }"
              class="mask-image-frame img-container after:absolute after:inset-0 after:z-[1] after:bg-black/60 after:content-['']"
              :class="{
                'after:opacity-0': selected,
                'after:opacity-100': !selected,
              }"
            >
              <img
                class="w-full"
                :src="`${PUBLIC_URL}${image}`"
                :alt="name"
                draggable="false"
              />
            </div>
            <img
              class="absolute inset-0 w-full transition-opacity duration-300"
              :class="[selected ? 'opacity-100' : 'opacity-0']"
              :src="`${PUBLIC_URL}item/decor.svg`"
              alt="decor"
              draggable="false"
            />
          </div>
          <img
            class="relative z-10 w-full"
            :src="`${PUBLIC_URL}item/frame.svg`"
            alt="frame"
            draggable="false"
          />
        </div>
      </div>
      <div class="@container">
        <p
          class="mb-[10px] text-[17px] leading-[21.6px] font-medium whitespace-break-spaces"
        >
          {{ name }}
        </p>
      </div>
      <p class="text-justify text-[14px] leading-[18.2px]">
        {{ text }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { PUBLIC_URL } from '~/constants'

const { item, disabled } = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const image = computed(() => item.image)
const name = computed(() => item.name)
const text = computed(() => item.text)
const selected = computed(() => item.selected ?? false)
</script>

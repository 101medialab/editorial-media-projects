<template>
  <div class="group/item flex flex-col">
    <div class="flex flex-1 flex-col">
      <div class="mb-[15px] max-sm:px-[26px]">
        <div class="group relative">
          <div class="absolute inset-0">
            <div
              :style="{
                '--mask-asset-url': `url(${PUBLIC_URL}item/result-mask.svg)`,
              }"
              class="mask-image-frame img-container after:absolute after:inset-0 after:z-[1] after:bg-black/60 after:content-['']"
              :class="{
                'after:opacity-0': selected,
                'after:opacity-100': !selected,
              }"
              style="mask-position: initial"
            >
              <img
                class="w-full transition-transform duration-300 group-hover:scale-105"
                :src="`${PUBLIC_URL}${image}`"
                :alt="name"
                draggable="false"
              />
            </div>
          </div>
          <img
            class="relative z-10 w-full"
            :src="`${PUBLIC_URL}item/result-frame.svg`"
            alt="frame"
            draggable="false"
          />
          <slot name="badge" />
          <a
            class="absolute inset-0 z-20 block"
            :href="url"
            target="_blank"
          ></a>
        </div>
      </div>
      <div class="@container">
        <p
          class="mb-[20px] text-[24px] leading-[28.8px] font-medium whitespace-break-spaces"
        >
          {{ name }}
        </p>
      </div>
      <p class="text-center text-base leading-[24px]">
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
const text = computed(() => item.long_text ?? item.text)
const selected = computed(() => item.selected ?? false)
const url = computed(() => item.url)
</script>

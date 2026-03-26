<template>
  <div class="group/item flex flex-col">
    <div class="flex flex-1 flex-col">
      <div class="mb-[20px]">
        <div class="relative">
          <div class="absolute inset-0 pr-[6.2%] pl-[6.2%]">
            <div
              class="aspect-square rounded-lg overflow-hidden after:absolute after:inset-0 after:z-[1] after:bg-black/60 after:content-['']"
              :class="{
                'after:opacity-0': selected,
                'after:opacity-100': !selected,
              }"
            >
              <div
                class="w-full h-full flex items-center justify-center text-white font-bold text-xl"
                :style="{ backgroundColor: item['background-color'] || '#6b7280' }"
              >
                {{ name }}
              </div>
            </div>
            <div
              class="absolute inset-0 border-4 border-white rounded-lg transition-opacity duration-300"
              :class="[selected ? 'opacity-100' : 'opacity-0']"
            ></div>
          </div>
          <div
            class="relative z-10 w-full aspect-square border-2 border-gray-300 rounded-lg"
          ></div>
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

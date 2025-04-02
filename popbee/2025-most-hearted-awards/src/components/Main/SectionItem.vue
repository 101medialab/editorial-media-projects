<template>
  <div
    class="group/item flex cursor-pointer flex-col"
    :class="{ selected: selected }"
    @click="onSelected"
  >
    <div class="flex flex-1 flex-col">
      <div class="mb-[20px]">
        <div class="relative">
          <div class="absolute inset-0 pr-[6.2%] pl-[6.2%]">
            <div
              :style="{ '--mask-asset-url': `url(${PUBLIC_URL}item/mask.svg)` }"
              class="mask-image-frame img-container after:absolute after:inset-0 after:z-[1] after:bg-black/60 after:opacity-0 after:transition-opacity after:duration-300 after:content-['']"
              :class="[
                {
                  'group-hover/category:group-[&:not(:hover)]/item:after:opacity-100 group-[&.selected]/category:group-[&:not(:hover)]/item:after:opacity-100':
                    !selected,
                },
              ]"
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
    <button
      class="mt-[20px] flex cursor-pointer items-center justify-center gap-[5px] rounded-full border border-white px-[20px] py-[10px] font-medium"
      :class="{ 'bg-white text-black': selected }"
    >
      <span v-show="selected"
        ><img :src="`${PUBLIC_URL}heart.svg`" alt="heart"
      /></span>
      <span>{{ buttonText }}</span>
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { PUBLIC_URL } from '~/constants'

const { item, disabled } = defineProps({
  item: {
    type: Object,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['selected'])

const selected = ref(false)
const image = computed(() => item.image)
const name = computed(() => item.name)
const text = computed(() => item.text)

const buttonText = computed(() => (selected.value ? '已選' : '選擇'))

const onSelected = () => {
  if (!disabled || selected.value) {
    selected.value = !selected.value
    emit('selected')
  }
}

defineExpose({
  selected,
  item,
})
</script>

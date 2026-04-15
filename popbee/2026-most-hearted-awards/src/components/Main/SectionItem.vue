<template>
  <div
    class="group/item flex cursor-pointer flex-col"
    :class="{ selected: selected }"
    @click="onSelected"
  >
    <div class="flex flex-1 flex-col">
      <div class="mb-[20px]">
        <div class="relative aspect-[226/293] w-full">
          <div
            class="absolute inset-0 overflow-hidden after:absolute after:inset-0 after:z-[1] after:bg-black/60 after:opacity-0 after:transition-opacity after:duration-300 after:content-['']"
            style="clip-path: ellipse(50% 50% at 50% 50%)"
            :class="[
              {
                'group-hover/category:group-[&:not(:hover)]/item:after:opacity-100 group-[&.selected]/category:group-[&:not(:hover)]/item:after:opacity-100':
                  !selected,
              },
            ]"
          >
            <img
              class="h-full w-full object-cover"
              :src="`${PUBLIC_URL}${image}`"
              :alt="name"
              draggable="false"
            />
          </div>
        </div>
      </div>
      <div class="@container">
        <p
          class="mb-[10px] text-center text-[20px] leading-[1.2] font-medium whitespace-break-spaces lg:text-[24px]"
        >
          {{ name }}
        </p>
      </div>
    </div>
    <button
      class="mt-[20px] flex cursor-pointer items-center justify-center gap-[5px] rounded-full border border-white px-[20px] py-[10px] font-medium"
      :class="{ 'bg-white text-black': selected }"
    >
      <span v-if="selected"
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

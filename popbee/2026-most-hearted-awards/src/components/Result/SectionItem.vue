<template>
  <div class="section-item">
    <div class="item-visual">
      <div class="category-badge">{{ item.category }}</div>
      <img
        :src="`${PUBLIC_URL}result/product/${item.image}`"
        :alt="item.title"
        class="product-img w-[271px] h-[319px]"
      />
      <div class="box-frame" aria-hidden="true" v-html="boxSvgHtml" />
    </div>

<!--    <div class="item-name">-->
<!--      <img :src="`${PUBLIC_URL}result/name-tag.svg`" alt="" aria-hidden="true" class="name-tag-bg" />-->
<!--      <p>{{ item.title }}</p>-->
<!--    </div>-->
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
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
})

const boxSvgHtml = ref('')

watchEffect(async () => {
  const res = await fetch(`${PUBLIC_URL}result/${props.box}`)
  boxSvgHtml.value = await res.text()
})
</script>

<style scoped lang="scss">
.section-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.item-visual {
  position: relative;
  width: 100%;

  .category-badge {
    position: absolute;
    top: 14px;
    left: 14px;
    z-index: 20;
    background-color: #1a2c4e;
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 4px 10px;
    text-transform: uppercase;
    pointer-events: none;
  }

  .product-img {
    position: absolute;
    inset: 0;
    margin: auto;
    max-width: 60%;
    max-height: 70%;
    object-fit: contain;
    z-index: 0;
  }

  .box-frame {
    position: relative;
    z-index: 10;
    width: 100%;
    display: block;

    :deep(svg) {
      width: 100%;
      height: auto;
      display: block;
    }
  }
}

.item-name {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin-top: 0;

  .name-tag-bg {
    width: 100%;
    display: block;
  }

  p {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #1a2c4e;
    white-space: pre-line;
    padding: 0 12px;
  }
}
</style>

<template>
  <div ref="root">
    <section>
      <picture>
        <source media="(min-width: 768px)" :srcset="`${mainBannerLg}`" />
        <img
          class="w-full"
          :src="`${mainBannerSm}`"
          alt="Most Hearted Awards 2025"
        />
      </picture>
    </section>

    <SectionCategories :config="config" />
    <div :class="{ 'pointer-events-none': completed || submitting }">
      <SectionCategory
        v-for="(item, index) in config"
        :id="`category-${item.id}`"
        :key="`section.category.${item.id}`"
        :config="item"
        ref="sectionCategoriesEl"
        @selected-items="onSelected"
        @auto-next-section="onAutoNextSection"
      >
        <template #footer>
          <footer v-if="index === config.length - 1" class="mt-[60px]">
            <div class="mb-[30px]">
              <button
                v-if="!completed"
                @click="submitVote"
                :disabled="!isVotingFulfilled"
                class="min-w-[191px] rounded-full bg-white px-[40px] py-[13.5px] text-base text-black not-disabled:cursor-pointer disabled:bg-[#AAA] disabled:text-white"
                :class="{ 'opacity-65': submitting }"
              >
                {{ submitButtonText }}
                <span v-if="submitting"
                  >&nbsp;<span class="loader"></span
                ></span>
              </button>
              <button
                v-else
                class="pointer-events-none min-w-[191px] rounded-full bg-[#333] px-[40px] py-[13.5px] text-base text-white"
              >
                您已成功投票
              </button>
            </div>

            <p>
              <small class="text-[11px]"
                >* Images from Getty Images & Brands</small
              >
            </p>
          </footer>
        </template>
      </SectionCategory>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, provide, useTemplateRef } from 'vue'
import { ofetch } from 'ofetch'
import pym from 'pym.js'
import mainBannerLg from '~/assets/most-hearted-award-banner-lg.jpg?w=2700'
import mainBannerSm from '~/assets/most-hearted-award-banner-sm.jpg'
import SectionCategories from '~/components/Main/SectionCategories.vue'
import SectionCategory from '~/components/Main/SectionCategory.vue'
import config from '~/config.json'
import { VOTES_EACH_CATEGORY, API_URL } from '~/constants'

const votes = ref(new Map())
const completed = ref(false)
const submitting = ref(false)
const pymChild = ref()
const scrollOffset = ref(0)
const currentSection = ref('')
const viewportInfo = ref({
  width: 0,
  height: 0,
})

const root = useTemplateRef('root')
const sectionCategoriesEl = useTemplateRef('sectionCategoriesEl')

provide('pymChild', pymChild)
provide('scrollOffset', scrollOffset)
provide('viewportInfo', viewportInfo)

const onSelected = (selectedItems) => {
  currentSection.value = selectedItems.id
  votes.value.set(selectedItems.id, selectedItems.items)

  sendIncompleteSectionMessage()
}

const onAutoNextSection = () => {
  // go to the submit button
  if (isVotingFulfilled.value) {
    const scrollPosition =
      root.value.getBoundingClientRect().bottom -
      viewportInfo.value.height +
      window.pageYOffset +
      scrollOffset.value

    pymChild.value.scrollParentToChildPos(scrollPosition)
  } else {
    // go to next incomplete section
    const sectionIndex = sectionCategoriesEl.value.findIndex(
      (section) => section.id === currentSection.value,
    )

    const lastIndex = sectionCategoriesEl.value.findLastIndex(
      (section) =>
        !section.autoNextSection || section.id === currentSection.value,
    )

    const nextIndex = sectionCategoriesEl.value
      .map((el) => el.autoNextSection)
      .indexOf(false, sectionIndex !== lastIndex ? sectionIndex : 0)

    if (nextIndex !== -1) {
      const nextEl = sectionCategoriesEl.value[nextIndex].el

      const scrollPosition =
        nextEl.getBoundingClientRect().top +
        window.pageYOffset -
        scrollOffset.value

      pymChild.value.scrollParentToChildPos(scrollPosition)
    }
  }

  sectionCategoriesEl.value.filter((section) => !section.autoNextSection)
}

const isVotingFulfilled = computed(
  () =>
    votes.value.size === config.length &&
    [...votes.value.values()].every(
      (items) => items.length >= VOTES_EACH_CATEGORY,
    ),
)

const checkForIncompleteSection = () => {
  const section = [...votes.value.keys()].find(
    (key) => votes.value.get(key).length < VOTES_EACH_CATEGORY,
  )

  if (
    !section ||
    section === currentSection.value ||
    votes.value.get(section).length === 0
  ) {
    pymChild.value.sendMessage('reminder', null)

    return false
  }

  return section
}

const sendIncompleteSectionMessage = () => {
  const section = checkForIncompleteSection()
  let message = null

  if (section) {
    const name = findSectionNameById(section)
    message = `每個類別中必須選擇三個項目，${name} 只選了 ${votes.value.get(section).length}/${VOTES_EACH_CATEGORY}`
  }

  pymChild.value.sendMessage('reminder', message)
}

const submitButtonText = computed(() => {
  if (submitting.value) return '提交中...'

  return !isVotingFulfilled.value ? '請選擇所有類別' : '提交'
})

const findSectionNameById = (id) => {
  return config.find((item) => item.id === id).name
}

const formData = computed(() => {
  return [...votes.value.values()].reduce((acc, items) => {
    items.forEach((item) => {
      acc[item.id] = 1
    })

    return acc
  }, {})
})

const submitVote = async () => {
  if (!isVotingFulfilled.value) return

  const body = {
    googleSheetName: 'pb-awards',
    data: {
      timestamp: new Date().toString(),
      ...formData.value,
    },
  }

  submitting.value = true

  await ofetch(API_URL, {
    method: 'POST',
    mode: 'no-cors',
    body,
  })
    .then(() => {
      completed.value = true
    })
    .catch(() => {
      submitting.value = false
    })
}

onMounted(() => {
  pymChild.value = new pym.Child({ polling: 500 })
  pymChild.value.onMessage('positionOffset', (offset) => {
    scrollOffset.value = +offset
  })
  pymChild.value.onMessage('viewport-iframe-position', (payload) => {
    const [width, height] = payload.split(' ')
    viewportInfo.value = { width: +width, height: +height }
  })
})
</script>

<style scoped>
.loader {
  width: 20px;
  display: inline-block;
  aspect-ratio: 8;
  background: radial-gradient(circle closest-side, #fff 90%, #fff0) 0 /
    calc(100% / 3) 100% space;
  clip-path: inset(0 100% 0 0);
  animation: l1 1.3s steps(4) infinite;
}

@keyframes l1 {
  to {
    clip-path: inset(0 -34% 0 0);
  }
}
</style>

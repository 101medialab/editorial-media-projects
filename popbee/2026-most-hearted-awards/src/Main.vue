<template>
  <div ref="root">
    <section class="main-banner">
      <img
        :src="`${PUBLIC_URL}mob-hero-banner.jpg`"
        alt="Most Hearted Awards 2026"
        class="w-full sm:hidden"
      />
      <img
        :src="`${PUBLIC_URL}hero-banner.jpg`"
        alt="Most Hearted Awards 2026"
        class="hidden w-full sm:block"
      />
    </section>

    <section
      class="intro flex flex-col items-center justify-center gap-y-[55px] pt-[60px] text-base leading-6 text-[#1E3160] [text-shadow:1px_1px_1px_rgba(0,0,0,0.004)]"
    >
      <div class="w-full items-center px-[15px] text-center md:max-w-[800px]">
        <p class="mb-[15px]">
          POPBEE 誠意呈獻—Most-Hearted
          Award！這是一場由你決定的時尚與潮流大賞，我們精選了過去一年內在 POPBEE
          網站上最受關注的關鍵字，並將它們分為 10
          個不同類別，讓你來為最愛的選項送上「愛心」支持。
        </p>
        <p>
          我們還加入了編輯評分環節，讓專業觀點為這場投票增添更多參考依據。無論是引領潮流的時尚單品、不可或缺的美妝單品，還是備受矚目的運動單品、閃耀動人的珠寶、令人期待的新興品牌，以及城中熱門科技新品，這一次，你的選擇將決定誰是最受歡迎的
          Most-Hearted 之選！
        </p>
      </div>

      <img :src="`${PUBLIC_URL}mob-intro-img.png`" alt="" class="sm:hidden" />
      <img :src="`${PUBLIC_URL}intro-img.png`" alt="" class="hidden sm:block w-full" />
    </section>

    <SectionCategories :config="config" />
    <div :class="{ 'pointer-events-none': completed || submitting }" class="pt-[60px] lg:pt-[80px]">
      <SectionCategory
        v-for="(item, index) in config"
        :id="`category-${item.id}`"
        :key="`section.category.${item.id}`"
        :config="item"
        :index="index"
        ref="sectionCategoriesEl"
        @selected-items="onSelected"
        @auto-next-section="onAutoNextSection"
      >
        <template #footer>
          <footer
            v-if="index === config.length - 1"
            class="mt-[60px] text-center"
            ref="footerEl"
          >
            <div class="mb-[30px]">
              <button
                v-if="!completed"
                @click="submitVote"
                :disabled="!isVotingFulfilled"
                class="min-w-[191px] rounded-full bg-white px-[40px] py-[13.5px] text-base text-black not-disabled:cursor-pointer disabled:bg-[#AAA] disabled:text-white not-disabled:hover:opacity-70"
                :class="{ 'opacity-65': submitting }"
              >
                {{ submitButtonText }}<span v-show="submitting"><span class="loader"></span></span>
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
      <div class="closing mx-auto max-w-[1123px] px-[15px] pb-[60px]">
        <img :src="`${PUBLIC_URL}luggage.png`" alt="" class="w-full" />
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  onUnmounted,
  provide,
  useTemplateRef,
} from 'vue'
import { ofetch } from 'ofetch'
import pym from 'pym.js'
import SectionCategories from '~/components/Main/SectionCategories.vue'
import SectionCategory from '~/components/Main/SectionCategory.vue'
import config from '~/config.json'
import { VOTES_EACH_CATEGORY, PUBLIC_URL, API_URL } from '~/constants'

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
const footerEl = useTemplateRef('footerEl')

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
      footerEl.value[0].getBoundingClientRect().top +
      window.pageYOffset -
      scrollOffset.value -
      (viewportInfo.value.height / 2) +
      footerEl.value[0].offsetHeight

      // window.scrollTo({
      //   top: scrollPosition,
      //   behavior: 'smooth',
      // })
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
        window.scrollY -
        scrollOffset.value

        // window.scrollTo({
        //   top: scrollPosition,
        //   behavior: 'smooth',
        // })
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
  if (submitting.value) return '提交中'

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
    googleSheetName: 'pb-26-awards',
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

const scrollToTop = () => {
  if (pymChild.value) {
    pymChild.value.scrollParentToChildPos(0)
  }
}

onMounted(() => {
  pymChild.value = new pym.Child({ polling: 500 })
  pymChild.value.onMessage('positionOffset', (offset) => {
    scrollOffset.value = +offset
  })
  pymChild.value.onMessage('viewport-iframe-position', (payload) => {
    const [vWidth, vHeight] = payload.split(' ').map(Number)
    viewportInfo.value = { width: vWidth, height: vHeight }
  })
  // Listen for back-to-top click from the parent page
  pymChild.value.onMessage('backToTop', () => scrollToTop())

  // Use IntersectionObserver on the banner to tell the parent when to show/hide the button
  const banner = root.value?.querySelector('.main-banner')
  if (banner) {
    const observer = new IntersectionObserver(
      ([entry]) => {
        pymChild.value.sendMessage(
          'backToTop',
          entry.isIntersecting ? 'hide' : 'show',
        )
      },
      { threshold: 0 },
    )
    observer.observe(banner)
  }
})

onUnmounted(() => {})
</script>

<style scoped>
.intro {
  background-image: url('/intro-grain-bg.jpg');
  background-repeat: repeat;
  background-size: auto;
}

.loader {
  width: 16px;
  display: inline-block;
  aspect-ratio: 8;
  background: radial-gradient(circle closest-side, #000 90%, #0000) 0 /
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

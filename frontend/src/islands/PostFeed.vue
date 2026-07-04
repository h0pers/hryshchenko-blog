<script setup>
// Infinite scroll for the server-rendered post list: when the sentinel below
// the list comes into view, fetch the next page of the same URL and append
// its post cards. The next page is advertised by the list's data-next-page
// attribute, rendered server-side by blog/includes/post_list.html.
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { LoaderCircle } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const loading = ref(false)
const error = ref(false)
const nextUrl = ref(null)
const sentinel = ref(null)

let list = null
let observer = null

function readNextUrl(root) {
  return root.querySelector('[data-post-list]')?.getAttribute('data-next-page') ?? null
}

async function loadMore() {
  if (loading.value || !nextUrl.value) return
  loading.value = true
  error.value = false
  try {
    const response = await fetch(nextUrl.value, { headers: { Accept: 'text/html' } })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const doc = new DOMParser().parseFromString(await response.text(), 'text/html')
    for (const card of doc.querySelectorAll('[data-post-card]')) {
      list.appendChild(card)
    }
    nextUrl.value = readNextUrl(doc)
    if (!nextUrl.value) observer?.disconnect()
  } catch {
    error.value = true
  } finally {
    loading.value = false
    // Re-observe so the callback fires again if the sentinel is still in
    // view after the new cards were appended (short pages, fast scrolling).
    if (nextUrl.value && !error.value && observer && sentinel.value) {
      observer.unobserve(sentinel.value)
      observer.observe(sentinel.value)
    }
  }
}

onMounted(() => {
  list = document.querySelector('[data-post-list]')
  nextUrl.value = readNextUrl(document)
  if (!list || !nextUrl.value) return

  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((entry) => entry.isIntersecting)) loadMore()
    },
    { rootMargin: '400px 0px' },
  )
  observer.observe(sentinel.value)
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <div ref="sentinel" class="flex justify-center py-6" aria-live="polite">
    <Button v-if="error" variant="outline" size="sm" @click="loadMore">Load more</Button>
    <p v-else-if="nextUrl" class="flex items-center gap-2 text-sm text-muted-foreground" role="status">
      <LoaderCircle class="size-4 animate-spin" aria-hidden="true" />
      Loading more posts…
    </p>
  </div>
</template>

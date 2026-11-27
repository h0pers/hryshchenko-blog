<script setup>
// Header RSS icon. Links to the /subscribe/ page rather than the raw feed,
// which browsers show as plain XML. Rendered to static HTML at build time
// (no client directive), so it ships no JavaScript.
import { Rss } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

defineProps({
  url: { type: String, required: true },
})
</script>

<template>
  <Button as="a" :href="url" variant="ghost" size="icon" aria-label="Subscribe via RSS">
    <Rss aria-hidden="true" />
  </Button>
</template>

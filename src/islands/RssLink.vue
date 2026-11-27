<script setup>
// Icon link to the RSS feed. Rendered to static HTML at build time (no
// client directive), so it ships no JavaScript.
import { Rss } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

defineProps({
  url: { type: String, required: true },
})
</script>

<template>
  <Button as="a" :href="url" variant="ghost" size="icon" aria-label="RSS feed">
    <Rss aria-hidden="true" />
  </Button>
</template>

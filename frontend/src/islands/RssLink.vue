<script setup>
// Icon link to the RSS feed. The feed URL comes from the mount element's
// data-feed-url attribute (see templates/base.html).
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

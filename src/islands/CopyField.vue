<script setup>
// Read-only text field with a copy-to-clipboard button. The value is
// rendered at build time; JavaScript only adds the copy action, and the
// field stays selectable for manual copying without it.
import { onBeforeUnmount, ref } from 'vue'
import { Check, Copy } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const props = defineProps({
  value: { type: String, required: true },
  label: { type: String, required: true },
})

const copied = ref(false)
const input = ref(null)
let timer = null

async function copy() {
  try {
    await navigator.clipboard.writeText(props.value)
  } catch {
    // Clipboard API unavailable (e.g. insecure context): select the text so
    // the visitor can copy it themselves.
    input.value?.select()
    return
  }
  copied.value = true
  clearTimeout(timer)
  timer = setTimeout(() => (copied.value = false), 2000)
}

onBeforeUnmount(() => clearTimeout(timer))
</script>

<template>
  <div class="flex items-center gap-2">
    <input
      ref="input"
      :value="value"
      :aria-label="label"
      readonly
      class="h-9 min-w-0 flex-1 rounded-md border border-input bg-background px-3 font-mono text-sm text-foreground"
      @focus="$event.target.select()"
    />
    <Button variant="outline" size="sm" class="h-9" @click="copy">
      <Check v-if="copied" aria-hidden="true" />
      <Copy v-else aria-hidden="true" />
      <span aria-live="polite">{{ copied ? 'Copied' : 'Copy' }}</span>
    </Button>
  </div>
</template>

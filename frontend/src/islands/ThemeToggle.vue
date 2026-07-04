<script setup>
// Toggles the .dark class on <html> and persists the choice. The initial
// class is applied before paint by an inline script in templates/base.html.
import { ref } from 'vue'
import { Moon, Sun } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const isDark = ref(document.documentElement.classList.contains('dark'))

function toggle() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}
</script>

<template>
  <Button
    variant="ghost"
    size="icon"
    :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'"
    @click="toggle"
  >
    <Sun v-if="isDark" aria-hidden="true" />
    <Moon v-else aria-hidden="true" />
  </Button>
</template>

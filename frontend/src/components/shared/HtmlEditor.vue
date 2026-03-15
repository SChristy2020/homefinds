<template>
  <div class="html-editor">
    <div class="editor-toolbar">
      <button type="button" class="tb-btn" :class="{ active: boldActive }" @mousedown.prevent="exec('bold')" title="粗體"><strong>B</strong></button>
      <button type="button" class="tb-btn" :class="{ active: italicActive }" @mousedown.prevent="exec('italic')" title="斜體"><em>I</em></button>
      <button type="button" class="tb-btn" :class="{ active: underlineActive }" @mousedown.prevent="exec('underline')" title="底線"><u>U</u></button>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('strikeThrough')" title="刪除線"><s>S</s></button>
      <div class="tb-sep"></div>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('insertUnorderedList')" title="無序清單">• 列表</button>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('insertOrderedList')" title="有序清單">1. 列表</button>
      <div class="tb-sep"></div>
      <button type="button" class="tb-btn" @mousedown.prevent="insertLink" title="插入連結">🔗</button>
      <button type="button" class="tb-btn" @mousedown.prevent="insertImageUrl" title="插入圖片網址">🖼</button>
      <label class="tb-btn tb-upload" title="上傳圖片">
        📤
        <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="onImageFile" />
      </label>
      <div class="tb-sep"></div>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('removeFormat')" title="清除格式" style="font-size:0.72rem">清格式</button>
    </div>
    <div
      ref="editorEl"
      class="editor-body"
      contenteditable="true"
      @input="onInput"
      @keyup="checkState"
      @mouseup="checkState"
      @focus="checkState"
    ></div>
    <div v-if="uploading" class="editor-uploading">上傳中...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '@/utils/api'

const props = defineProps({
  modelValue: { type: String, default: '' },
  roomId: { type: Number, default: null },
})
const emit = defineEmits(['update:modelValue'])

const editorEl = ref(null)
const fileInput = ref(null)
const boldActive = ref(false)
const italicActive = ref(false)
const underlineActive = ref(false)
const uploading = ref(false)

onMounted(() => {
  if (editorEl.value) editorEl.value.innerHTML = props.modelValue || ''
})

watch(() => props.modelValue, (val) => {
  if (editorEl.value && editorEl.value.innerHTML !== (val || '')) {
    editorEl.value.innerHTML = val || ''
  }
})

function onInput() {
  emit('update:modelValue', editorEl.value.innerHTML)
}

function exec(cmd, value = null) {
  document.execCommand(cmd, false, value)
  editorEl.value.focus()
  emit('update:modelValue', editorEl.value.innerHTML)
  checkState()
}

function checkState() {
  boldActive.value = document.queryCommandState('bold')
  italicActive.value = document.queryCommandState('italic')
  underlineActive.value = document.queryCommandState('underline')
}

function insertLink() {
  const url = prompt('請輸入連結網址:', 'https://')
  if (url) exec('createLink', url)
}

function insertImageUrl() {
  const url = prompt('請輸入圖片網址:')
  if (url) exec('insertImage', url)
}

async function onImageFile(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const form = new FormData()
    form.append('file', file)
    const endpoint = props.roomId ? `/api/room/${props.roomId}/images` : '/api/uploads'
    const res = await api.upload(endpoint, form)
    const url = res.url || res.image_url
    if (url) exec('insertImage', url)
  } catch {
    // fallback: insert as object URL
    const url = URL.createObjectURL(file)
    exec('insertImage', url)
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}
</script>

<style scoped>
.html-editor {
  border: 1.5px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
}
.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 5px 8px;
  background: var(--surface, #f8f8f6);
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
}
.tb-btn {
  background: none;
  border: 1px solid transparent;
  border-radius: 3px;
  cursor: pointer;
  padding: 3px 8px;
  font-size: 0.82rem;
  color: var(--charcoal, #333);
  transition: all 0.15s;
  min-width: 28px;
  line-height: 1.4;
}
.tb-btn:hover { background: var(--accent-light, #f0ede6); border-color: var(--border); }
.tb-btn.active { background: var(--charcoal, #333); color: #fff; }
.tb-upload { cursor: pointer; }
.tb-sep {
  width: 1px;
  height: 18px;
  background: var(--border);
  margin: 0 3px;
}
.editor-body {
  min-height: 120px;
  padding: 10px 12px;
  outline: none;
  font-size: 0.88rem;
  line-height: 1.7;
  color: var(--charcoal, #333);
}
.editor-body:focus { background: #fffffe; }
.editor-body :deep(img) { max-width: 100%; height: auto; border-radius: 4px; display: block; margin: 4px 0; }
.editor-body :deep(a) { color: var(--accent, #b5935a); text-decoration: underline; }
.editor-uploading {
  padding: 4px 12px;
  font-size: 0.78rem;
  color: var(--mid);
  background: var(--surface);
  border-top: 1px solid var(--border);
}
</style>

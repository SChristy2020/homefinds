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
      <button type="button" class="tb-btn" @mousedown.prevent="insertMailto" title="插入Email連結">✉️</button>
      <button type="button" class="tb-btn" @mousedown.prevent="insertImageUrl" title="插入圖片網址">🖼</button>
      <button type="button" class="tb-btn" @mousedown.prevent="insertGoogleMap" title="嵌入 Google 地圖">🗺</button>
      <label class="tb-btn tb-upload" title="上傳圖片">
        📤
        <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="onImageFile" />
      </label>
      <div class="tb-sep"></div>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('indent')" title="縮排">⇥</button>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('outdent')" title="取消縮排">⇤</button>
      <div class="tb-sep"></div>
      <button type="button" class="tb-btn" @mousedown.prevent="exec('removeFormat')" title="清除格式" style="font-size:0.72rem">清格式</button>
    </div>
    <div class="editor-body-wrap">
      <div
        ref="editorEl"
        class="editor-body"
        contenteditable="true"
        @input="onInput"
        @keydown="onKeydown"
        @paste="onPaste"
        @keyup="checkState"
        @mouseup="checkState"
        @click="onEditorClick"
        @focus="checkState"
      ></div>
      <!-- Image resize overlay -->
      <div v-if="selectedImg" class="img-resize-overlay" :style="overlayStyle">
        <div class="resize-handle nw" @mousedown.prevent="startResize($event, 'nw')"></div>
        <div class="resize-handle ne" @mousedown.prevent="startResize($event, 'ne')"></div>
        <div class="resize-handle sw" @mousedown.prevent="startResize($event, 'sw')"></div>
        <div class="resize-handle se" @mousedown.prevent="startResize($event, 'se')"></div>
        <div class="img-size-label">{{ imgSizeLabel }}</div>
        <div class="img-align-toolbar">
          <button class="align-btn" :class="{ active: imgAlign === 'left' }"   @mousedown.prevent="setImgAlign('left')"   title="靠左">⬛︎←</button>
          <button class="align-btn" :class="{ active: imgAlign === 'center' }" @mousedown.prevent="setImgAlign('center')" title="置中">↔</button>
          <button class="align-btn" :class="{ active: imgAlign === 'right' }"  @mousedown.prevent="setImgAlign('right')"  title="靠右">→⬛︎</button>
        </div>
      </div>
    </div>
    <div v-if="uploading" class="editor-uploading">上傳中...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
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

// ── Image resize ──────────────────────────────────────────────────────────────
const selectedImg = ref(null)
const overlayStyle = ref({})
const imgSizeLabel = ref('')

function updateOverlay() {
  if (!selectedImg.value || !editorEl.value) return
  const editorRect = editorEl.value.getBoundingClientRect()
  const imgRect = selectedImg.value.getBoundingClientRect()
  overlayStyle.value = {
    left:   (imgRect.left - editorRect.left + editorEl.value.scrollLeft) + 'px',
    top:    (imgRect.top  - editorRect.top  + editorEl.value.scrollTop)  + 'px',
    width:  imgRect.width  + 'px',
    height: imgRect.height + 'px',
  }
  imgSizeLabel.value = `${Math.round(imgRect.width)} × ${Math.round(imgRect.height)}`
}

function onEditorClick(e) {
  if (e.target.tagName === 'IMG') {
    selectedImg.value = e.target
    imgAlign.value = getImgAlign(e.target)
    updateOverlay()
  } else {
    selectedImg.value = null
  }
}

function onDocumentClick(e) {
  if (!editorEl.value?.contains(e.target)) {
    selectedImg.value = null
  }
}

const imgAlign = ref('left')

function getImgAlign(img) {
  if (!img) return 'left'
  const ml = img.style.marginLeft
  const mr = img.style.marginRight
  if (ml === 'auto' && mr === 'auto') return 'center'
  if (ml === 'auto') return 'right'
  return 'left'
}

function setImgAlign(align) {
  if (!selectedImg.value) return
  const img = selectedImg.value
  if (align === 'center') { img.style.marginLeft = 'auto'; img.style.marginRight = 'auto' }
  else if (align === 'right') { img.style.marginLeft = 'auto'; img.style.marginRight = '0' }
  else { img.style.marginLeft = '0'; img.style.marginRight = 'auto' }
  imgAlign.value = align
  emit('update:modelValue', editorEl.value.innerHTML)
}

function startResize(e, corner) {
  if (!selectedImg.value) return
  const img = selectedImg.value
  const startX = e.clientX
  const startW = img.getBoundingClientRect().width

  function onMouseMove(e) {
    const dx = e.clientX - startX
    const newW = Math.max(40, corner === 'nw' || corner === 'sw' ? startW - dx : startW + dx)
    img.style.width  = newW + 'px'
    img.style.height = 'auto'
    updateOverlay()
  }

  function onMouseUp() {
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
    emit('update:modelValue', editorEl.value.innerHTML)
  }

  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(() => {
  if (editorEl.value) editorEl.value.innerHTML = props.modelValue || ''
  document.addEventListener('click', onDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
})

watch(() => props.modelValue, (val) => {
  if (editorEl.value && editorEl.value.innerHTML !== (val || '')) {
    editorEl.value.innerHTML = val || ''
    selectedImg.value = null
  }
})

// ── Editor commands ───────────────────────────────────────────────────────────
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

function insertMailto() {
  const email = prompt('請輸入 Email 地址:')
  if (!email) return
  const sel = window.getSelection()
  const text = sel && sel.toString() ? sel.toString() : email
  const html = `<a href="mailto:${email}">${text}</a>`
  document.execCommand('insertHTML', false, html)
  editorEl.value.focus()
  emit('update:modelValue', editorEl.value.innerHTML)
}

function insertImageUrl() {
  const url = prompt('請輸入圖片網址:')
  if (url) exec('insertImage', url)
}

function insertGoogleMap() {
  const input = prompt('請貼上 Google 地圖的 <iframe> 嵌入碼，或 embed 網址（maps/embed?pb=...）:')
  if (!input) return

  let iframeHtml = input.trim()

  // 若使用者只貼 URL，自動包成 iframe
  if (!iframeHtml.startsWith('<')) {
    if (!iframeHtml.includes('google.com/maps')) {
      alert('請貼入有效的 Google 地圖網址或 iframe 嵌入碼。')
      return
    }
    iframeHtml = `<iframe src="${iframeHtml}" width="100%" height="400" style="border:0;border-radius:6px;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>`
  }

  // 在 iframe 外包一層 div 方便排版
  const html = `<div class="map-embed" style="margin:12px 0;">${iframeHtml}</div><p><br></p>`
  document.execCommand('insertHTML', false, html)
  editorEl.value.focus()
  emit('update:modelValue', editorEl.value.innerHTML)
}

async function onPaste(e) {
  const items = Array.from(e.clipboardData?.items || [])
  const imageItem = items.find(item => item.type.startsWith('image/'))
  if (!imageItem) return
  e.preventDefault()
  const file = imageItem.getAsFile()
  if (!file) return
  uploading.value = true
  try {
    const { url } = await api.upload(file)
    if (url) exec('insertImage', url)
  } catch {
    const url = URL.createObjectURL(file)
    exec('insertImage', url)
  } finally {
    uploading.value = false
  }
}

function onKeydown(e) {
  if (e.key === 'Tab') {
    e.preventDefault()
    exec(e.shiftKey ? 'outdent' : 'indent')
  }
  if (e.key === 'Escape') selectedImg.value = null
}

async function onImageFile(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const { url } = await api.upload(file)
    if (url) exec('insertImage', url)
  } catch {
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
  background: #fff;
}
.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 5px 8px;
  background: var(--surface, #f8f8f6);
  border-bottom: 1px solid var(--border);
  border-radius: 6px 6px 0 0;
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
.editor-body-wrap {
  position: relative;
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
.editor-body :deep(img) { max-width: 100%; height: auto; border-radius: 4px; display: block; margin: 4px 0; cursor: pointer; }
.editor-body :deep(a) { color: var(--accent, #b5935a); text-decoration: underline; }
.editor-body :deep(ul), .editor-body :deep(ol) { padding-left: 1.5em; }
.editor-body :deep(ul) { list-style-type: disc; }
.editor-body :deep(ol) { list-style-type: decimal; }
.editor-body :deep(ul ul) { list-style-type: circle; }
.editor-body :deep(ul ul ul) { list-style-type: square; }
.editor-body :deep(blockquote) { margin-left: 1.5em; padding-left: 0.75em; border-left: 3px solid var(--border); }
.editor-body :deep(iframe) { max-width: 100%; width: 100% !important; height: 360px; border: none; border-radius: 6px; display: block; margin: 8px 0; }
.editor-body :deep(.map-embed) { width: 100%; }

/* Image resize overlay */
.img-resize-overlay {
  position: absolute;
  border: 2px solid #4a90e2;
  pointer-events: none;
  box-sizing: border-box;
  border-radius: 3px;
}
.resize-handle {
  position: absolute;
  width: 10px;
  height: 10px;
  background: #fff;
  border: 2px solid #4a90e2;
  border-radius: 2px;
  pointer-events: all;
  box-sizing: border-box;
}
.resize-handle.nw { top: -5px;    left: -5px;   cursor: nw-resize; }
.resize-handle.ne { top: -5px;    right: -5px;  cursor: ne-resize; }
.resize-handle.sw { bottom: -5px; left: -5px;   cursor: sw-resize; }
.resize-handle.se { bottom: -5px; right: -5px;  cursor: se-resize; }
.img-size-label {
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.65);
  color: #fff;
  font-size: 0.7rem;
  padding: 2px 7px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
}
.img-align-toolbar {
  position: absolute;
  top: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 2px;
  background: rgba(0,0,0,0.65);
  border-radius: 4px;
  padding: 3px 4px;
  pointer-events: all;
  white-space: nowrap;
}
.align-btn {
  background: none;
  border: 1px solid transparent;
  border-radius: 3px;
  color: #fff;
  font-size: 0.72rem;
  padding: 2px 7px;
  cursor: pointer;
  transition: background 0.12s;
}
.align-btn:hover { background: rgba(255,255,255,0.2); }
.align-btn.active { background: rgba(255,255,255,0.35); border-color: rgba(255,255,255,0.5); }

.editor-uploading {
  padding: 4px 12px;
  font-size: 0.78rem;
  color: var(--mid);
  background: var(--surface);
  border-top: 1px solid var(--border);
}
</style>

<script setup lang="ts">
import { ref, Text } from 'vue'

defineProps<{ msg: string }>()
const userInput = ref("")
const output = ref("")

const emoji = ref("NO EMOJIS")
const style = ref("Auto")
const textSize = ref("")

const styles = ["Auto", "Official", "Casual", "Creative", "Professional", "Friendly", "Urgent"];
const sizes = ["Large", "Middle", "Minimum"];

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(output.value)
    alert("Text copied")
  }catch (err) {
    alert("Error")
  }
}

const generatePost = async () => {
  output.value = `Please wait. Generate has started`

  try {
    const res = await fetch("http://localhost:5000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        url: userInput.value,
        emoji: emoji.value,
        style: style.value,
        text_size: textSize.value
      })
    })
    const data = await res.json()
    output.value = data.post
  } catch (err)
  {
    output.value = "Error generate"
    console.error(err)
  }
}
</script>

<template>
  <div class="page">
    <nav class="topnav">
      <a class="logo" href="#">Post Crafter</a>
    </nav>

    <div class="content">
      <div class="col">
        <h2>Generate Perfect Social Posts</h2>
        <p class="subtitle">Enter your URL and customize the content style</p>

        <div class="input-group">
          <input
            class="input"
            type="search"
            v-model="userInput"
            placeholder="https://example.com"
          />
        </div>

        <section>
          <h3>Text style</h3>
          <div class="radio-input">
            <label v-for="s in styles" :key="s" class="radiolabel">
              <input class="radio-input" type="radio" v-model="style" :value="s" />
              <span>{{ s }}</span>
            </label>
          </div>
          <p>Selected style: {{ style }}</p>
        </section>

        <section>
          <h3>Use emoji?</h3>
          <div class="radio-input">
            <label class="radiolabel">
              <input type="radio" v-model="emoji" value="NO EMOJIS" />
              <span>No</span>
            </label>
            <label class="radio">
              <input type="radio" v-model="emoji" value="Yes" />
              <span>Yes</span>
            </label>
          </div>
          <p>Choosed: {{ emoji }}</p>
        </section>

        <section>
          <h3>Text size</h3>
          <div class="radio-input">
            <label v-for="s in sizes" :key="s" class="radiolabel">
              <input type="radio" v-model="textSize" :value="s" />
              <span>{{ s }}</span>
            </label>
          </div>
          <p>Text size: {{ textSize }}</p>
        </section>

        <button @click="generatePost" class="generate-btn">Generate post</button>
      </div>

      <div class="col">
        <div class="output-box">
          <p>{{ output }}</p>
        </div>
        <button @click="copyToClipboard" class="copy-btn">Copy text</button>
      </div>
    </div>
    <footer class="bottomInfo">
      <h3>Post Crafter</h3>
      <p>AI-Powered Social Media Content Generator</p>
      <p>© 2025 Copiright</p>
    </footer>
  </div>
</template>

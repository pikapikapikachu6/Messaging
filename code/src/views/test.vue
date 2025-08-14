<script setup>
import {sha256, short, salt, RSA_encryption, RSA_decryption} from '../utils/crypto.js'

let input = $ref('')
let random = $ref('')

let username = $ref('')
let pwd = $ref('')
let mes = $ref('')


let checkResult = $ref('')

let key = $ref('')
async function generateRSAKeys () {
  function RSA2text (buffer) {
    const bytes = new Uint8Array(buffer), L = bytes.byteLength
    let bin = ''
    for (let i = 0; i < L; i++) bin += String.fromCharCode(bytes[i])
    return window.btoa(bin).replace(/[^\x00-\xff]/g, '$&\x01').replace(/.{64}\x01?/g, '$&\n')
  }
  try {
    const S = window.crypto.subtle
    const k = await S.generateKey({
      name: 'RSA-OAEP',
      modulusLength: 2048,
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
      hash: { name: 'SHA-256' }
    }, true, ['encrypt', 'decrypt'])
    const sk = RSA2text(await S.exportKey('pkcs8', k.privateKey))
    const pk = RSA2text(await S.exportKey('spki', k.publicKey))
    return [pk, sk]
  } catch (e) {
    console.error(e)
    return null
  }
}

async function getKeys() {
  let keys = await generateRSAKeys()
  let privateKey = keys[1]
  let publicKey = keys[0]
  console.log(privateKey)
  console.log(publicKey)
  const mess = "hello"
  console.log("encryp:" + RSA_encryption(publicKey, mess))
  let result = RSA_encryption(publicKey, mess)
  console.log("decryp:" + RSA_decryption(privateKey, result))
}

getKeys()



</script>

<template>

</template>


<style scoped>

</style>
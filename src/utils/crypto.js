import JSEncrypt from 'jsencrypt'

const enc = new TextEncoder('utf-8')
const base64 = buffer => btoa(String.fromCharCode(...new Uint8Array(buffer)))

export const salt = 'INFO2222-Project'

export const random = () => Math.random().toString(36).substr(2, 10)

export const short = str => str.substr(0, 10).replaceAll('+', '-').replaceAll('/', '_')

export const sha256 = str => window.crypto.subtle.digest('SHA-256', enc.encode(str)).then(base64)

export const RSA_encryption = (pk, msg) => {
  if (pk != undefined) {
    var encryptor = new JSEncrypt()
    encryptor.setPublicKey(pk)
    var cipher = encryptor.encrypt(msg)
    //console.log(cipher)
    return cipher
  }
  return "False"
}

export const RSA_decryption = (sk, cipher) => {
  if (sk != undefined) {
    var decryptor  = new JSEncrypt()
    decryptor.setPrivateKey(sk)
    var text = decryptor.decrypt(cipher)
    //console.log("The RSA msg: ", text)
    if (text == false) {
      //console.log("The RSA msg: ", text)
      return "False"
    }
    return text
  }
  return "False"
}
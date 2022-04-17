module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
  dev: {
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    proxyTable: {
      '/': {
        target: '127.0.0.1:80 ',
        changeOrigin: true,
      }
    }
  }
}

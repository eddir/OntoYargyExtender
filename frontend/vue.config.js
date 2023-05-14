module.exports = {
  lintOnSave: false,
  runtimeCompiler: true,
  configureWebpack: {
    //Necessary to run npm link https://webpack.js.org/configuration/resolve/#resolve-symlinks
    resolve: {
       symlinks: false
    }
  },
  transpileDependencies: [
    '@coreui/utils',
    '@coreui/vue'
  ],
  devServer: {
    disableHostCheck: true,
    host: 'localhost',
    port: 443,
    https: true,
    proxy: {
      '^/api': {
        target: 'https://ontology.rostkov.me',
        changeOrigin: true,
        ws: true,
      },
      '^/auth': {
        target: 'https://ontology.rostkov.me',
        changeOrigin: true,
        ws: true,
      },
      '^/admin': {
        target: 'https://ontology.rostkov.me',
        changeOrigin: true,
        ws: true,
      },
      '^/static': {
        target: 'https://ontology.rostkov.me',
        changeOrigin: true,
        ws: true,
      },
    }
  }
}

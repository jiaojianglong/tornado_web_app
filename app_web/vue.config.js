const isProduct = process.env.NODE_ENV === 'production';
const webpack = require('webpack')

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        $:"jquery",
        jQuery:"jquery",
        "windows.jQuery":"jquery"
      })
    ]},
  runtimeCompiler: true,
  css: {
    // Enable CSS source maps.
    sourceMap: true
  },
};

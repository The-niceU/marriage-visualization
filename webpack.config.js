<<<<<<< HEAD
const path = require('path');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
module.exports = {
   
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    plugins: [
    new BundleAnalyzerPlugin() // 添加插件
  ]
  },
  mode: 'production',
};
=======
const path = require('path');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
module.exports = {
   
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    plugins: [
    new BundleAnalyzerPlugin() // 添加插件
  ]
  },
  mode: 'production',
};
>>>>>>> cf9b8f26705edf91579650bea50a15c66659291f

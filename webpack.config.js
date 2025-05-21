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

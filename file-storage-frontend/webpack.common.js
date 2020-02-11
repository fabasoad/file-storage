const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = () => ({
    entry: [
        '@babel/polyfill',
        path.resolve(__dirname, 'src', 'app.js')
    ],
    module: {
        rules: [{
            test: /\.js$/,
            loader: 'babel-loader',
            exclude: /node_modules/
        }, {
            test: /\.s?css$/,
            use: [{
                loader: MiniCssExtractPlugin.loader
            }, {
                loader: 'css-loader',
                options: {
                    sourceMap: true
                }
            }, {
                loader: 'sass-loader',
                options: {
                    sourceMap: true
                }
            }]
        }]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'styles.css'
        })
    ],
    output: {
        path: path.join('/', 'app', 'public', 'dist'),
        filename: 'bundle.js'
    }
});
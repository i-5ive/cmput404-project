const HtmlWebPackPlugin = require("html-webpack-plugin"),
    webpack = require("webpack"),
    path = require("path"),
    PORT = process.env.PORT || 8081;

// Credit to user3923737 at https://stackoverflow.com/a/53726068 for the "output" property
module.exports = {
    resolve: {
        // removes the need to add file extensions to the end of imports
        extensions: ["\0", ".webpack.js", ".web.js", ".js", ".jsx", ".scss"]
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'index_bundle.js',
        publicPath: '/'
    },
    devServer: {
        // allows React-Router
        historyApiFallback: true,
        port: PORT,
        host: "127.0.0.1"
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.html$/,
                use: [
                    {
                        loader: "html-loader"
                    }
                ]
            },
            // src: https://getbootstrap.com/docs/4.0/getting-started/webpack/
            {
                test: /\.(scss)$/,
                use: [{
                    loader: "style-loader" // inject CSS to page
                }, {
                    loader: "css-loader" // translates CSS into CommonJS modules
                }, {
                    loader: "postcss-loader", // Run post css actions
                    options: {
                        plugins: function() { // post css plugins, can be exported to postcss.config.js
                            return [
                                require("precss"),
                                require("autoprefixer")
                            ];
                        }
                    }
                }, {
                    loader: "sass-loader" // compiles Sass to CSS
                }]
            }, {
                test: /\.css$/,
                use: [{
                    loader: "style-loader" // inject CSS to page
                }, {
                    loader: "css-loader" // translates CSS into CommonJS modules
                }]
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "[path][name].[ext]"
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: "./src/index.html",
            filename: "./index.html"
        }),
        new webpack.EnvironmentPlugin(["DJANGO_HOST"])
    ],
	node: {
		fs: "empty",
		net: "empty",
		tls: "empty"
	}
};

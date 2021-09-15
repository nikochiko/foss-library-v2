const path = require("path");
const webpack = require("webpack");

/*
 * Webpack plugins
 */
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const ProductionPlugins = [
  // production webpack plugins go here
  new webpack.DefinePlugin({
    "process.env": {
      NODE_ENV: JSON.stringify("production"),
    },
  }),
];

const debug = process.env.NODE_ENV !== "production";
const rootAssetPath = path.join(__dirname, "assets");

module.exports = {
  // configuration
  context: __dirname,
  entry: {
    main_js: "./assets/js/main",
    main_css: [
      path.join(
        __dirname,
        "node_modules",
        "@fortawesome",
        "fontawesome-free",
        "css",
        "all.css"
      ),
    ],
    main_scss: [path.join(__dirname, "assets", "scss", "custom.scss")],
  },
  mode: "production",
  output: {
    chunkFilename: "[id].js",
    filename: "[name].bundle.js",
    path: path.join(__dirname, "fosslib", "static", "build"),
    publicPath: "/static/build/",
  },
  resolve: {
    extensions: [".js", ".jsx", ".css", ".scss"],
  },
  devtool: debug ? "eval-source-map" : false,
  plugins: [
    new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
    new webpack.ProvidePlugin({ $: "jquery", jQuery: "jquery" }),
  ],
  module: {
    rules: [
      {
        test: /\.(css)$/,
        use: [
          "style-loader",
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: function () {
                  return [require("autoprefixer")];
                },
              },
            },
          },
        ],
      },
      {
        test: /\.(scss)$/,
        use: [
          "style-loader",
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: function () {
                  return [require("autoprefixer")];
                },
              },
            },
          },
          "sass-loader",
        ],
      },
      { test: /\.html$/, loader: "raw-loader" },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "url-loader",
        options: { limit: 10000, mimetype: "application/font-woff" },
      },
      {
        test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
        loader: "file-loader",
        options: { context: rootAssetPath, name: "[path][name].[ext]" },
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env"], cacheDirectory: true },
      },
    ],
  },
};

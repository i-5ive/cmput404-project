// Karma configuration
var path = require("path"),
    webpackConfig = require("./webpack.config.js");

webpackConfig.watch = true;
// Allows us to write shorter paths when importing files from src/js
// Also allows us to prevent network calls by stubbing axios
webpackConfig.resolve.modules = [path.resolve(__dirname, "src/js"), "node_modules"];
webpackConfig.mode = "development";
webpackConfig.module.rules.push({
    test: /\.jsx?$/,
    use: {
        loader: "istanbul-instrumenter-loader",
        options: { esModules: true }
    },
    include: [
        path.resolve("src/js/react")
    ]
});

module.exports = function(config) {
    config.set({
        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: "",

        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ["mocha"],

        // list of files / patterns to load in the browser
        files: [
            "tests.webpack.js"
        ],

        // list of files / patterns to exclude
        exclude: [
        ],

        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            "tests.webpack.js": ["webpack"]
        },

        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ["progress", "mocha", "coverage-istanbul"],
        coverageIstanbulReporter: {
            reports: [ "lcov", "text-summary" ],
            fixWebpackSourcePaths: true

            // enforces code coverage
            // thresholds: {
            //     each: {
            //         statements: 85,
            //         lines: 85,
            //         branches: 85,
            //         functions: 85,
            //         overrides: {
            //             "filename/example.jsx": {
            //                 statements: 0,
            //                 lines: 0,
            //                 branches: 0,
            //                 functions: 0
            //             }
            //         }
            //     }
            // }
        },

        // web server port
        port: 9876,

        // enable / disable colors in the output (reporters and logs)
        colors: true,

        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,

        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,

        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ["Chrome"],

        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: false,

        // Concurrency level
        // how many browser should be started simultaneous
        concurrency: Infinity,

        webpack: webpackConfig
    });
};

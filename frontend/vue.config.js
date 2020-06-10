module.exports = {
    devServer: {
        host: 'localhost'
    },
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = 'Loading'
                return args
            })
    }
};
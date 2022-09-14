module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'https://terminus-back.herokuapp.com/'
            }
        }
    }
}
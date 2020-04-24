module.exports = {
    extends: [
        'plugin:vue/vue3-recommended',
    ],
    rules: {
        "vue/component-tags-order": ["error", {
            "order": ["template", "script", "style"]
        }],
        "vue/html-indent": ["error", (4 | "tab"), {
            "attribute": 1,
            "baseIndent": 1,
            "closeBracket": 0,
            "alignAttributesVertically": true,
            "ignores": []
        }]
    }
};
module.exports = {

    extends: [
        "plugin:vue/recommended"
    ],

    rules: {
        "no-console": "off",
        "vue/no-use-v-if-with-v-for": "off",
        "vue/html-indent": [
            "error", 4, {"baseIndent": 1, "alignAttributesVertically": false}
        ],
        "vue/html-closing-bracket-newline": [
            "error",
            {
                "singleline": "never",
                "multiline": "never"
            }
        ]
    },

};

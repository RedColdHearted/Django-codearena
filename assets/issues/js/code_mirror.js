// This file needs to use CodeMirror and displays existing solution
const codeInputElement = document.getElementById("code-input")
const languageSelectElement = document.getElementById('language-select')

// Handle user's solution if it exist trough attributes
const solutionDataMapper = {
  language: codeInputElement.getAttribute("data-language"),
  content: codeInputElement.getAttribute("data-content")
}

// Performs attaching CodeMirror widget to form's textarea
const editor = CodeMirror.fromTextArea(codeInputElement, {
  lineNumbers: true,
  lineWrapping: true,
  mode: {
    name: solutionDataMapper.language ? solutionDataMapper.language.toLowerCase() : "python",
    singleLineStringErrors: false
  },
  theme: "default",
  indentUnit: 4,
  matchBrackets: true,
});

// Check if solution exists, displays it into CodeMirror widget
if (solutionDataMapper.content){
  editor.setValue(solutionDataMapper.content)
}

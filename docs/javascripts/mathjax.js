// Конфигурация MathJax 3 для нумерованных формул с \label / \eqref (P2).
// tags: 'ams' включает автонумерацию уравнений в окружениях \begin{equation}.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
    tags: "ams"            // нумерация уравнений + \eqref{...}
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// Пересборка формул после мгновенной навигации Material (navigation.instant)
document$.subscribe(() => {
  if (window.MathJax && window.MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
});

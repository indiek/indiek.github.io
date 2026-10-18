// "On this page" table of contents and copy buttons for code blocks.
document.addEventListener("DOMContentLoaded", () => {
  const toc = document.getElementById("toc");
  const content = document.getElementById("content");
  if (toc && content) {
    const headings = content.querySelectorAll("h2[id], h3[id]");
    if (headings.length === 0) {
      toc.parentElement.style.visibility = "hidden";
    } else {
      const list = document.createElement("ul");
      headings.forEach((heading) => {
        const item = document.createElement("li");
        item.className = heading.tagName === "H3" ? "level-3" : "level-2";
        const link = document.createElement("a");
        link.href = "#" + heading.id;
        link.textContent = heading.textContent;
        item.appendChild(link);
        list.appendChild(item);
      });
      toc.appendChild(list);
    }
  }

  document.querySelectorAll("div.highlighter-rouge").forEach((block) => {
    const code = block.querySelector("pre code");
    if (!code || !navigator.clipboard) return;
    const button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.textContent = "Copy";
    button.addEventListener("click", () => {
      navigator.clipboard.writeText(code.innerText).then(() => {
        button.textContent = "Copied";
        setTimeout(() => (button.textContent = "Copy"), 1500);
      });
    });
    block.appendChild(button);
  });
});

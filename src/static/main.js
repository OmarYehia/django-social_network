const toggleComment = node => {
    const commentList = node.nextSibling.nextSibling;
    commentList.classList.toggle("hide");
    node.innerText = (node.innerText == "Show Comments") ? "Hide Comments" : "Show Comments";
}
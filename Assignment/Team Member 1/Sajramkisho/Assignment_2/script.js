const btn = document.querySelector("button")
btn.addEventListener("click", () => {
  const input = document.getElementById("input-value").value
  const pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/
  if (input.match(pattern)) {
    error.classList.add("valid")
    error.classList.remove("invalid")
  } else {
    error.classList.add("invalid")
    error.classList.remove("valid")
  }
  if (input === "") {
    error.classList.remove("invalid")
    error.classList.remove("valid")
  }
})

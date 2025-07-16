const form = document.querySelector("form");
const loading = document.getElementById("loading");

form.addEventListener("submit", function() {
    loading.style.display = "block";
    form.querySelector("input[type=submit]").disabled = true;
});
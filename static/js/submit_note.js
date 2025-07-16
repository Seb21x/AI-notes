document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("noteForm");
    const loading = document.getElementById("loading")
    form.addEventListener("submit", function(submit) {
        submit.preventDefault();
        loading.style.display = "block";

        const note = document.getElementById("note").value;

        fetch("/add_note", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ note: note })
        })
        .then(res => res.json())
        .then(data => {
            window.location.reload();
        })
        .catch(err => {
            loading.innerHTML = "There was a problem with adding your note.";
            console.error(err);
        });
    });
});
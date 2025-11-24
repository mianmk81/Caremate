document.addEventListener("DOMContentLoaded", function () {
    let fileCount = 0;
    const fileUploadStatus = document.getElementById("fileUploadStatus");
    const medicationInputs = document.getElementById("medicationInputs");
    const uploadFileBtn = document.getElementById("uploadFileBtn");
    const uploadMoreFilesBtn = document.getElementById("uploadMoreFilesBtn");
    const addMedicationBtn = document.getElementById("addMedicationBtn");
    const analyzeBtn = document.getElementById("analyzeBtn");

    uploadFileBtn.addEventListener("click", () => {
        fileCount++;
        fileUploadStatus.textContent = `${fileCount} uploaded`;
    });

    uploadMoreFilesBtn.addEventListener("click", () => {
        fileCount++;
        fileUploadStatus.textContent = `${fileCount} uploaded`;
    });

    addMedicationBtn.addEventListener("click", () => {
        const newInput = document.createElement("div");
        newInput.innerHTML = `
            <label>Medication ${medicationInputs.children.length / 2 + 1}:</label>
            <input type="text" class="medication" placeholder="Enter medication">
        `;
        medicationInputs.appendChild(newInput);
    });

    analyzeBtn.addEventListener("click", () => {
        const medications = Array.from(document.querySelectorAll(".medication"))
            .map(input => input.value.trim())
            .filter(value => value);

        if (medications.length) {
            fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ medications })
            })
            .then(response => response.json())
            .then(data => {
                alert("Analysis Results: " + data.result);
            })
            .catch(error => {
                console.error("Error:", error);
            });
        } else {
            alert("Please add at least one medication.");
        }
    });
});
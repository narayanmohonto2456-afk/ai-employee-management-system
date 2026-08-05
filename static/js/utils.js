// ===============================
// EMS Utility Functions
// ===============================

/**
 * Get CSRF Token from Django form
 */
function getCSRFToken() {

    const csrfInput = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    );

    return csrfInput ? csrfInput.value : "";

}

/**
 * Show Bootstrap Alert
 */
function showMessage(type, message) {

    const messageBox = document.getElementById(
        "attendanceMessage"
    );

    if (!messageBox) return;

    messageBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">

            ${message}

            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert">
            </button>

        </div>
    `;

}
// ===============================
// Attendance Module
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Attendance Module Loaded");

    const checkInBtn = document.getElementById("checkInBtn");
    const checkOutBtn = document.getElementById("checkOutBtn");

    /**
     * Send Attendance Request
     */
    function sendAttendanceRequest(button) {

        if (!button) return;

        button.addEventListener("click", function (event) {

            event.preventDefault();

            fetch(button.dataset.url, {

                method: "POST",

                headers: {

                    "X-Requested-With": "XMLHttpRequest",

                    "X-CSRFToken": getCSRFToken(),

                },

            })

            .then(response => response.json())

            .then(data => {

                if (data.success) {

                    showMessage(
                        "success",
                        data.message
                    );

                    button.disabled = true;

                }

                else {

                    showMessage(
                        "warning",
                        data.message
                    );

                }

            })

            .catch(error => {

                console.error(error);

                showMessage(
                    "danger",
                    "Something went wrong."
                );

            });

        });

    }

    sendAttendanceRequest(checkInBtn);
    sendAttendanceRequest(checkOutBtn);

});
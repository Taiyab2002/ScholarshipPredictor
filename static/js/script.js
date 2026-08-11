/* =========================================
   SMARTSCHOLAR - QUESTIONNAIRE SCRIPT
========================================= */

let currentStep = 0;

const steps = document.querySelectorAll(".step");

const progress = document.getElementById("progress");

const stepText = document.getElementById("stepText");

const progressPercent =
    document.getElementById("progressPercent");

const indicators =
    document.querySelectorAll(".step-indicator");

const indicatorLines =
    document.querySelectorAll(".indicator-line");

const form =
    document.getElementById("scholarshipForm");

const submitButton =
    document.getElementById("submitButton");


/* =========================================
   SHOW STEP
========================================= */

function showStep(step) {

    steps.forEach((element, index) => {

        element.classList.toggle(
            "active",
            index === step
        );

    });


    const percentage =
        ((step + 1) / steps.length) * 100;


    progress.style.width =
        percentage + "%";


    stepText.textContent =
        `Step ${step + 1} of ${steps.length}`;


    progressPercent.textContent =
        `${percentage}%`;


    /* Step indicators */

    indicators.forEach((indicator, index) => {

        indicator.classList.remove(
            "active",
            "completed"
        );


        if (index < step) {

            indicator.classList.add(
                "completed"
            );

        }


        if (index === step) {

            indicator.classList.add(
                "active"
            );

        }

    });


    /* Progress connecting lines */

    indicatorLines.forEach((line, index) => {

        line.classList.toggle(
            "completed",
            index < step
        );

    });

}


/* =========================================
   VALIDATE CURRENT STEP
========================================= */

function validateCurrentStep() {

    const inputs =
        steps[currentStep].querySelectorAll(
            "input, select"
        );


    for (const input of inputs) {

        if (!input.checkValidity()) {

            input.reportValidity();

            input.focus();

            return false;

        }

    }


    return true;

}


/* =========================================
   NEXT STEP
========================================= */

function nextStep() {

    if (!validateCurrentStep()) {

        return;

    }


    if (currentStep < steps.length - 1) {

        currentStep++;

        showStep(currentStep);

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }

}


/* =========================================
   PREVIOUS STEP
========================================= */

function prevStep() {

    if (currentStep > 0) {

        currentStep--;

        showStep(currentStep);

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }

}


/* =========================================
   SUBMIT LOADING STATE
========================================= */

if (form) {

    form.addEventListener(
        "submit",
        function () {

            /*
             * Browser validation happens before
             * the submit event.
             */

            if (submitButton) {

                submitButton.classList.add(
                    "loading"
                );

                submitButton.innerHTML =
                    "Checking eligibility...";

            }

        }
    );

}


/* =========================================
   INITIALIZE
========================================= */

showStep(currentStep);
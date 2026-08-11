/* =========================================
   SMARTSCHOLAR - QUESTIONNAIRE SCRIPT
========================================= */

let currentStep = 0;

const steps =
    document.querySelectorAll(".step");

const progress =
    document.getElementById("progress");

const stepText =
    document.getElementById("stepText");

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


    indicatorLines.forEach((line, index) => {

        line.classList.toggle(
            "completed",
            index < step
        );

    });

}


/* =========================================
   ERROR HANDLING
========================================= */

function showError(input, message) {

    input.classList.add("invalid");

    input.classList.remove("valid");


    const errorElement =
        document.getElementById(
            input.id + "Error"
        );


    if (errorElement) {

        errorElement.textContent =
            "* " + message;

        errorElement.classList.add(
            "show"
        );

    }

}


function clearError(input) {

    input.classList.remove(
        "invalid"
    );


    const errorElement =
        document.getElementById(
            input.id + "Error"
        );


    if (errorElement) {

        errorElement.textContent = "";

        errorElement.classList.remove(
            "show"
        );

    }

}


function markValid(input) {

    clearError(input);

    input.classList.add("valid");

}


/* =========================================
   NAME VALIDATION
========================================= */

function validateName(input) {

    const value =
        input.value.trim();


    if (value === "") {

        showError(
            input,
            "Please enter your full name."
        );

        return false;

    }


    const namePattern =
        /^[\p{L}][\p{L}\s.'-]*$/u;


    if (!namePattern.test(value)) {

        showError(
            input,
            "Name should contain letters only. Numbers are not allowed."
        );

        return false;

    }


    if (value.length < 2) {

        showError(
            input,
            "Please enter a valid name."
        );

        return false;

    }


    markValid(input);

    return true;

}


/* =========================================
   AGE VALIDATION
========================================= */

function validateAge(input) {

    const value =
        input.value.trim();


    if (value === "") {

        showError(
            input,
            "Please enter your age."
        );

        return false;

    }


    if (!/^\d+$/.test(value)) {

        showError(
            input,
            "Age must be a whole number. Decimal values are not allowed."
        );

        return false;

    }


    const age =
        Number(value);


    if (
        !Number.isInteger(age) ||
        age < 15 ||
        age > 60
    ) {

        showError(
            input,
            "Age must be a whole number between 15 and 60."
        );

        return false;

    }


    markValid(input);

    return true;

}


/* =========================================
   CGPA VALIDATION
========================================= */

function validateCGPA(input) {

    const value =
        input.value.trim();


    if (value === "") {

        showError(
            input,
            "Please enter your current CGPA."
        );

        return false;

    }


    if (!/^\d+(\.\d{1,2})?$/.test(value)) {

        showError(
            input,
            "Please enter a valid CGPA, such as 3.75."
        );

        return false;

    }


    const cgpa =
        Number(value);


    if (
        !Number.isFinite(cgpa) ||
        cgpa < 0 ||
        cgpa > 4
    ) {

        showError(
            input,
            "CGPA must be between 0.00 and 4.00."
        );

        return false;

    }


    markValid(input);

    return true;

}


/* =========================================
   ACADEMIC PERCENTAGE VALIDATION
========================================= */

function validatePercentage(input) {

    const value =
        input.value.trim();


    if (value === "") {

        showError(
            input,
            "Please enter your academic percentage."
        );

        return false;

    }


    if (!/^\d+(\.\d{1,2})?$/.test(value)) {

        showError(
            input,
            "Please enter a valid percentage, such as 85 or 85.50."
        );

        return false;

    }


    const percentage =
        Number(value);


    if (
        !Number.isFinite(percentage) ||
        percentage < 0 ||
        percentage > 100
    ) {

        showError(
            input,
            "Academic percentage must be between 0 and 100."
        );

        return false;

    }


    markValid(input);

    return true;

}


/* =========================================
   IELTS VALIDATION
========================================= */

function validateIELTS(input) {

    const value =
        input.value.trim();


    if (value === "") {

        showError(
            input,
            "Please enter your IELTS score."
        );

        return false;

    }


    if (!/^\d+(\.5)?$/.test(value)) {

        showError(
            input,
            "IELTS score must use 0.5 increments, such as 6.5 or 7.0."
        );

        return false;

    }


    const score =
        Number(value);


    if (
        !Number.isFinite(score) ||
        score < 0 ||
        score > 9
    ) {

        showError(
            input,
            "IELTS score must be between 0 and 9."
        );

        return false;

    }


    markValid(input);

    return true;

}


/* =========================================
   SELECT VALIDATION
========================================= */

function validateSelect(input) {

    if (input.value === "") {

        showError(
            input,
            "Please select an option."
        );

        return false;

    }


    markValid(input);

    return true;

}


/* =========================================
   VALIDATE INDIVIDUAL INPUT
========================================= */

function validateInput(input) {

    switch (input.id) {

        case "name":

            return validateName(input);


        case "age":

            return validateAge(input);


        case "cgpa":

            return validateCGPA(input);


        case "academic_percentage":

            return validatePercentage(input);


        case "ielts_score":

            return validateIELTS(input);


        default:

            if (
                input.tagName === "SELECT"
            ) {

                return validateSelect(
                    input
                );

            }

            return true;

    }

}


/* =========================================
   VALIDATE CURRENT STEP
========================================= */

function validateCurrentStep() {

    const inputs =
        steps[currentStep].querySelectorAll(
            "input, select"
        );


    let allValid = true;

    let firstInvalid = null;


    inputs.forEach(input => {

        const valid =
            validateInput(input);


        if (!valid) {

            allValid = false;


            if (!firstInvalid) {

                firstInvalid = input;

            }

        }

    });


    if (firstInvalid) {

        firstInvalid.focus();

        firstInvalid.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }


    return allValid;

}


/* =========================================
   NEXT STEP
========================================= */

function nextStep() {

    if (!validateCurrentStep()) {

        return;

    }


    if (
        currentStep <
        steps.length - 1
    ) {

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
   REAL-TIME VALIDATION
========================================= */

const allInputs =
    document.querySelectorAll(
        "input, select"
    );


allInputs.forEach(input => {


    input.addEventListener(
        "blur",
        function () {

            validateInput(this);

        }
    );


    input.addEventListener(
        "input",
        function () {

            if (
                this.classList.contains(
                    "invalid"
                )
            ) {

                validateInput(this);

            }

        }
    );


    input.addEventListener(
        "change",
        function () {

            validateInput(this);

        }
    );

});


/* =========================================
   FINAL SUBMISSION VALIDATION
========================================= */

if (form) {

    form.addEventListener(
        "submit",
        function (event) {

            let valid = true;

            let firstInvalid = null;


            const inputs =
                this.querySelectorAll(
                    "input, select"
                );


            inputs.forEach(input => {

                const result =
                    validateInput(input);


                if (!result) {

                    valid = false;


                    if (!firstInvalid) {

                        firstInvalid = input;

                    }

                }

            });


            if (!valid) {

                event.preventDefault();


                if (firstInvalid) {

                    steps.forEach(
                        (step, index) => {

                            if (
                                step.contains(
                                    firstInvalid
                                )
                            ) {

                                currentStep =
                                    index;

                            }

                        }
                    );


                    showStep(
                        currentStep
                    );


                    firstInvalid.focus();


                    firstInvalid.scrollIntoView({

                        behavior: "smooth",

                        block: "center"

                    });

                }

                return;

            }


            /* Loading state */

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
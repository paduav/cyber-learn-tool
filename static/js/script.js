/* Recommended JSON response
{
    "lessonPlan": {
    "title": "Understanding Phishing",
    "summary": "A classroom-ready lesson...",
    "tags": [
      { "label": "Beginner", "type": "difficulty" },
      { "label": "Phishing", "type": "topic" },
      { "label": "45 min", "type": "duration" }
    ],
    "learningObjectives": [
      "Explain key concepts related to phishing.",
      "Analyze realistic scenarios and identify safe digital decision-making strategies."
    ],
    "standardsAlignment": [
      { "label": "Requested Alignment", "text": "CSTA 2-NI-05" }
    ],
    "materials": [
      "Slides",
      "Scenario cards"
    ],
    "introduction": {
      "time": "10 min",
      "text": "Introduce phishing with a short discussion prompt.",
      "bullets": [
        "Ask students what they know already.",
        "Set the lesson question."
      ]
    },
    "activities": [
      {
        "title": "Guided Scenario Review",
        "time": "15 min",
        "text": "Students review examples.",
        "bullets": [
          "Work in pairs",
          "Share reasoning"
        ]
      }
    ],
    "discussionReflection": {
      "time": "5 min",
      "bullets": [
        "What is one important idea to remember?"
      ]
    },
    "wrapUp": {
      "time": "5 min",
      "text": "Review the main takeaway.",
      "note": "Exit ticket..."
    }
  }
}
*/

// For storing data in the browser's sessionStorage, which remembers the user's form submission and generated lesson plan.
const LESSON_REQUEST_STORAGE_KEY = "lessonGenerator.latestRequest";
const LESSON_PLAN_STORAGE_KEY = "lessonGenerator.latestLessonPlan";
const SUGGESTED_TOPICS = [
    "Online Safety & Digital Citizenship",
    "Privacy & Personal Data Protection",
    "Passwords & Authentication",
    "Phishing & Social Engineering",
    "Cryptography",
    "Malware & Cyber Threats",
    "Operating Systems & Command line",
    "Network Security",
    "Artifical Intelligence",
];
const SUGGESTED_STANDARDS = [
    "K-12 Cybersecurity Standards",
    "ISTE Standards",
    "CSTA Computer Science Standards",
    "NICE Framework",
];

// Run two functions after the page's HTML has finished loading.
document.addEventListener("DOMContentLoaded", () => {
    initializeGeneratorForm();
    initializeLessonPlanPage();
});

function initializeGeneratorForm() {
    const form = document.querySelector("#lesson-generator-form");

    // Quits the function if the form is not on this page.
    if (!form) {
        return;
    }

    // Stores references to all the input elements.
    const fields = {
        topic: form.querySelector("#topic"),
        topicInput: form.querySelector("#topic-input"),
        difficulty: form.querySelector("#difficulty"),
        durationValue: form.querySelector("#duration-value"),
        durationUnit: form.querySelector("#duration-unit"),
        standards: form.querySelector("#standards"),
        standardsInput: form.querySelector("#standards-input"),
        customization: form.querySelector("#customization"),
    };
    const topicPicker = createTagPicker({
        root: fields.topic,
        input: fields.topicInput,
        tagList: form.querySelector("#topic-tags"),
        suggestionsContainer: form.querySelector("#topic-suggestions"),
        suggestions: SUGGESTED_TOPICS,
        onChange: () => {
            clearFieldError(fields.topic);
            hideMessage(statusMessage);
        },
    });
    const standardsPicker = createTagPicker({
        root: fields.standards,
        input: fields.standardsInput,
        tagList: form.querySelector("#standards-tags"),
        suggestionsContainer: form.querySelector("#standards-suggestions"),
        suggestions: SUGGESTED_STANDARDS,
        onChange: () => hideMessage(statusMessage),
    });

    const statusMessage = form.querySelector("#form-status");
    const submitButton = form.querySelector("#generate-button");
    const previewUrl = form.dataset.previewUrl || "lesson-plan";

    // When the form is submitted:
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Takes user's inputs and turns into a JavaScript object.
        const payload = buildLessonRequestPayload(fields, topicPicker, standardsPicker);
        // Checks for missing or invalid required values.
        const validationErrors = validateLessonRequest(payload);

        renderValidationErrors(validationErrors, fields);

        if (Object.keys(validationErrors).length > 0) {
            showMessage(statusMessage, "Please complete the required fields before generating the lesson plan.", "error");
            return;
        }

        // Visual feedback for the user by displaying a status message and disables the button.
        showMessage(statusMessage, "Preparing lesson plan preview...", "success");
        submitButton.disabled = true;
        submitButton.textContent = "Preparing...";

        // Saves the form data in browser storage.
        sessionStorage.setItem(LESSON_REQUEST_STORAGE_KEY, JSON.stringify(payload));

        /*
            BACKEND: send form data to Flask and wait for Flask to send back the lesson plan.
        */
        try {
            const lessonPlan = await requestLessonPlan(payload);
            // Saves the lesson plan in browser storage, then sends the browser to the preview page.
            sessionStorage.setItem(LESSON_PLAN_STORAGE_KEY, JSON.stringify(lessonPlan));
            window.location.href = previewUrl;
        } catch (error) { // Error handling
            console.error("Lesson preview preparation failed:", error);
            showMessage(
                statusMessage,
                error.message || "We could not prepare the lesson plan preview right now. Please try again.",
                "error"
            );
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Generate lesson plan";
        }
    });

    // Listens for "input" and "change" so it removes the error state.
    [fields.difficulty, fields.durationValue, fields.durationUnit, fields.customization].forEach((field) => {
        if (!field) {
            return;
        }

        field.addEventListener("input", () => {
            clearFieldError(field);
            hideMessage(statusMessage);
        });

        field.addEventListener("change", () => {
            clearFieldError(field);
            hideMessage(statusMessage);
        });
    });
}

// Preview page, where the generated lesson plan is displayed.
function initializeLessonPlanPage() {
    const titleElement = document.querySelector("#lesson-title");
    const pdfButton = document.querySelector("#save-pdf-button");

    // Opens the browser print dialog.
    if (pdfButton) {
        pdfButton.addEventListener("click", () => window.print());
    }

    // If this page is not the preview page, quit function.
    if (!titleElement) {
        return;
    }

    const pageMessage = document.querySelector("#lesson-page-message");
    // Reads the saved request and saved lesson plan from sessionStorage.
    const storedRequest = safelyParseStorage(LESSON_REQUEST_STORAGE_KEY);
    const storedLessonPlan = safelyParseStorage(LESSON_PLAN_STORAGE_KEY);

    // Warns the user no content has been generated yet.
    if (!storedRequest && !storedLessonPlan) {
        showMessage(
            pageMessage,
            "A lesson plan has not been generated. Complete the Lesson Details form to view your curated cybersecurity lesson plan.",
            "error"
        );
        return;
    }

    // Gets a lesson plan object, ensures correct structure, and displays it on the page.
    const renderedLessonPlan = normalizeLessonPlan(storedLessonPlan, storedRequest);
    renderLessonPlan(renderedLessonPlan);
}

// Reads the form values and builds a request object.
function buildLessonRequestPayload(fields, topicPicker, standardsPicker) {
    const durationValue = Number.parseInt(fields.durationValue.value, 10);
    const durationUnit = fields.durationUnit.value || "minutes";
    const topics = topicPicker.getValues();
    const standards = standardsPicker.getValues();

    return {
        topic: topics,
        difficultyLevel: fields.difficulty.value.trim().toLowerCase(),
        duration: {
            value: Number.isNaN(durationValue) ? null : durationValue,
            unit: durationUnit,
            display: Number.isNaN(durationValue) ? "" : formatDuration(durationValue, durationUnit),
            totalMinutes: Number.isNaN(durationValue) ? null : convertDurationToMinutes(durationValue, durationUnit),
        },
        standardsAlignment: standards,
        additionalCustomization: fields.customization.value.trim(),
    };
}

// Checks the request object and builds an errors object. Checks for missing inputs, adds an error message if something is wrong.
function validateLessonRequest(payload) {
    const errors = {};

    if (!Array.isArray(payload.topic) || payload.topic.length === 0) {
        errors.topic = "Please choose at least one learning topic or skill area.";
    }

    if (!payload.difficultyLevel) {
        errors.difficulty = "Please select a difficulty level.";
    }

    if (!payload.duration.value || payload.duration.value < 1) {
        errors.durationValue = "Please enter a valid time allotment.";
    }

    if (!payload.duration.unit) {
        errors.durationUnit = "Please choose minutes, hours, or days.";
    }

    return errors;
}

// Takes the lesson plan data and makes sure it has all the pieces the page expects.
function normalizeLessonPlan(lessonPlan, requestPayload = {}) {
    const requestTopics = normalizeRequestList(requestPayload?.topic);
    const requestTopic = requestTopics[0] || "Cybersecurity Awareness";
    const requestDifficulty = requestPayload?.difficultyLevel || "beginner";
    const requestDuration = requestPayload?.duration?.display || "45 min";

    const title = lessonPlan?.title || `Understanding ${requestTopic}`;
    const summary =
        lessonPlan?.summary ||
        `A classroom-ready lesson focused on ${requestTopic.toLowerCase()} with age-appropriate discussion, guided practice, and reflection.`;

    return {
        title,
        summary,
        tags: buildLessonTags(lessonPlan?.tags, requestDifficulty, requestTopic, requestDuration),
        learningObjectives: normalizeStringList(
            lessonPlan?.learningObjectives,
            [
                `Explain key concepts related to ${requestTopic.toLowerCase()}.`,
                "Analyze realistic scenarios and identify safe digital decision-making strategies.",
                "Apply clear steps students can use in everyday online interactions.",
            ]
        ),
        standardsAlignment: normalizeStandards(
            lessonPlan?.standardsAlignment,
            requestPayload?.standardsAlignment
        ),
        materials: normalizeStringList(lessonPlan?.materials, [
            "Teacher presentation slides or board space for guided discussion.",
            "Student handouts or devices for collaborative review.",
            "Example scenarios connected to the lesson topic.",
        ]),
        introduction: normalizeSection(
            lessonPlan?.introduction,
            "10 min",
            `Introduce ${requestTopic.toLowerCase()} with a short discussion prompt that connects the topic to students' real digital experiences.`,
            [
                "Invite students to share what they already know about the topic.",
                "Establish one key question the lesson will help answer.",
            ]
        ),
        activities: normalizeActivities(lessonPlan?.activities, requestTopic),
        discussionReflection: normalizeSection(
            lessonPlan?.discussionReflection,
            "5 min",
            "",
            [
                `What is one idea about ${requestTopic.toLowerCase()} that feels most important to remember?`,
                "Which part of the lesson felt most useful in a real-world setting?",
            ]
        ),
        wrapUp: normalizeWrapUp(lessonPlan?.wrapUp, requestTopic),
    };
}

function buildLessonTags(tags, difficultyLevel, topic, durationDisplay) {
    const normalized = Array.isArray(tags) ? tags.filter(Boolean) : [];

    if (normalized.length > 0) {
        return normalized.map((tag, index) => normalizeLessonTag(tag, index));
    }

    return [
        { label: toTitleCase(difficultyLevel), type: "difficulty" },
        { label: topic, type: "topic" },
        { label: durationDisplay, type: "duration" },
    ];
}

function normalizeLessonTag(tag, index) {
    if (typeof tag === "string") {
        return {
            label: tag,
            type: inferTagType(index)
        };
    }

    return {
        label: tag.label || "",
        type: tag.type || inferTagType(index)
    };
}

function getDifficultyModifier(label) {
    const value = String(label).toLowerCase();

    if (value.includes("beginner")) return "beginner";
    if (value.includes("intermediate")) return "intermediate";
    if (value.includes("advanced")) return "advanced";

    return "";
}

function normalizeStandards(standards, standardsFallback) {
    if (Array.isArray(standards) && standards.length > 0) {
        return standards.map((item) => {
            if (typeof item === "string") {
                return { label: "Standard", text: item };
            }

            return {
                label: item.label || item.framework || "Standard",
                text: item.text || item.description || "",
            };
        });
    }

    if (Array.isArray(standardsFallback) && standardsFallback.length > 0) {
        return standardsFallback.map((item) => ({ label: "Requested Alignment", text: item }));
    }

    if (typeof standardsFallback === "string" && standardsFallback.trim()) {
        return [{ label: "Requested Alignment", text: standardsFallback }];
    }

    return [
        {
            label: "Suggested Alignment",
            text: "Add a curriculum or framework alignment here when those details are ready.",
        },
    ];
}

function normalizeSection(section, fallbackTime, fallbackText, fallbackBullets) {
    if (typeof section === "string") {
        return {
            time: fallbackTime,
            text: section,
            bullets: fallbackBullets,
        };
    }

    return {
        time: section?.time || fallbackTime,
        text: section?.text || section?.summary || fallbackText,
        bullets: normalizeStringList(section?.bullets || section?.prompts, fallbackBullets),
    };
}

function normalizeActivities(activities, topic) {
    if (Array.isArray(activities) && activities.length > 0) {
        return activities.map((activity, index) => ({
            title: activity.title || `Activity ${index + 1}`,
            time: activity.time || "",
            text: activity.text || activity.description || "",
            bullets: normalizeStringList(activity.bullets || activity.steps, []),
        }));
    }

    return [
        {
            title: "Guided Scenario Review",
            time: "10 min",
            text: `Students examine realistic examples connected to ${topic.toLowerCase()} and identify what stands out.`,
            bullets: [
                "Work in pairs to identify patterns, red flags, or best-practice responses.",
                "Share findings with the class and compare reasoning.",
            ],
        },
        {
            title: "Collaborative Practice",
            time: "15 min",
            text: "Students apply the lesson concepts to short prompts or teacher-created mini cases.",
            bullets: [
                "Discuss possible decisions before choosing a final response.",
                "Explain why one action is safer or more effective than another.",
            ],
        },
    ];
}

function normalizeWrapUp(wrapUp, topic) {
    if (typeof wrapUp === "string") {
        return {
            time: "5 min",
            text: wrapUp,
            note: "",
        };
    }

    return {
        time: wrapUp?.time || "5 min",
        text:
            wrapUp?.text ||
            wrapUp?.summary ||
            `Close by revisiting the most important takeaway from ${topic.toLowerCase()} and naming one action students can use right away.`,
        note: wrapUp?.note || "Exit ticket: Write one takeaway and one action step from today’s lesson.",
    };
}

function normalizeStringList(value, fallback = []) {
    if (Array.isArray(value)) {
        return value.filter(Boolean);
    }

    if (typeof value === "string" && value.trim()) {
        return [value.trim()];
    }

    return fallback;
}

// Takes the finished lesson plan object and puts its values into the HTML page.
function renderLessonPlan(lessonPlan) {
    setText("#lesson-title", lessonPlan.title);
    setText("#lesson-summary", lessonPlan.summary);
    setText("#introduction-time", lessonPlan.introduction.time);
    setText("#introduction-copy", lessonPlan.introduction.text);
    setText("#activities-time", sumActivityTimes(lessonPlan.activities) || "Activities");
    setText("#discussion-time", lessonPlan.discussionReflection.time);
    setText("#wrap-up-time", lessonPlan.wrapUp.time);
    setText("#wrap-up-copy", lessonPlan.wrapUp.text);
    setText("#wrap-up-note", lessonPlan.wrapUp.note);

    renderTagList("#lesson-tags", lessonPlan.tags);
    renderSimpleList("#learning-objectives", lessonPlan.learningObjectives);
    renderSimpleList("#introduction-bullets", lessonPlan.introduction.bullets);
    renderActivities("#activities-list", lessonPlan.activities);
    renderSimpleList("#discussion-points", lessonPlan.discussionReflection.bullets);
    renderStandards("#standards-list", lessonPlan.standardsAlignment);
    renderMaterials("#materials-list", lessonPlan.materials);
}

function renderTagList(selector, tags) {
    const container = document.querySelector(selector);

    if (!container) {
        return;
    }

    let paletteIndex = 0;

    container.innerHTML = tags
        .map((tag) => {
            const tagClasses = ["lesson-tag", escapeHtml(tag.type)];

            if (tag.type === "difficulty") {
                const difficultyModifier = getDifficultyModifier(tag.label);

                if (difficultyModifier) {
                    tagClasses.push(escapeHtml(difficultyModifier));
                } else {
                    tagClasses.push(getTagPaletteClass(paletteIndex));
                    paletteIndex += 1;
                }
            } else {
                tagClasses.push(getTagPaletteClass(paletteIndex));
                paletteIndex += 1;
            }

            return `<span class="${tagClasses.join(" ")}">${escapeHtml(tag.label)}</span>`;
        })
        .join("");
}

function getTagPaletteClass(index) {
    const palette = [
        "palette-slate",
        "palette-yellow",
        "palette-red",
        "palette-blue",
        "palette-green",
        "palette-purple",
    ];

    return palette[index % palette.length];
}

function renderSimpleList(selector, items) {
    const container = document.querySelector(selector);

    if (!container) {
        return;
    }

    container.innerHTML = items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
}

function renderActivities(selector, activities) {
    const container = document.querySelector(selector);

    if (!container) {
        return;
    }

    container.innerHTML = activities
        .map(
            (activity) => `
                <article class="activity-card">
                    <div class="activity-topline">
                        <h3 class="activity-title">${escapeHtml(activity.title)}</h3>
                        <span class="activity-time">${escapeHtml(activity.time || "")}</span>
                    </div>
                    <p>${escapeHtml(activity.text)}</p>
                    <ul>
                        ${activity.bullets.map((bullet) => `<li>${escapeHtml(bullet)}</li>`).join("")}
                    </ul>
                </article>
            `
        )
        .join("");
}

function renderStandards(selector, items) {
    const container = document.querySelector(selector);

    if (!container) {
        return;
    }

    container.innerHTML = items
        .map(
            (item) => `
                <div class="standards-item">
                    <span class="item-label">${escapeHtml(item.label)}</span>
                    ${escapeHtml(item.text)}
                </div>
            `
        )
        .join("");
}

function renderMaterials(selector, items) {
    const container = document.querySelector(selector);

    if (!container) {
        return;
    }

    container.innerHTML = items
        .map(
            (item) => `
                <div class="materials-item">
                    <span class="materials-dot" aria-hidden="true"></span>
                    <div>${escapeHtml(item)}</div>
                </div>
            `
        )
        .join("");
}

// Clears any old error states, then shows new ones.
function renderValidationErrors(errors, fields) {
    clearFieldError(fields.topic);
    clearFieldError(fields.difficulty);
    clearFieldError(fields.durationValue);
    clearFieldError(fields.durationUnit);

    if (errors.topic) {
        setFieldError(fields.topic, "#topic-error", errors.topic);
    }

    if (errors.difficulty) {
        setFieldError(fields.difficulty, "#difficulty-error", errors.difficulty);
    }

    if (errors.durationValue || errors.durationUnit) {
        setFieldError(fields.durationValue, "#duration-error", errors.durationValue || errors.durationUnit);
        fields.durationUnit.setAttribute("aria-invalid", "true");
    }
}

function createTagPicker({ root, input, tagList, suggestionsContainer, suggestions, onChange }) {
    const state = {
        values: [],
    };

    renderSuggestions();
    renderSelectedTags();

    input.classList.add("tag-input");

    root.addEventListener("click", () => {
        input.focus();
    });

    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === ",") {
            event.preventDefault();
            addValue(input.value);
        }

        if (event.key === "Backspace" && !input.value.trim() && state.values.length > 0) {
            removeValue(state.values[state.values.length - 1]);
        }
    });

    input.addEventListener("blur", () => {
        addValue(input.value);
    });

    function addValue(rawValue) {
        const normalizedValue = normalizePickerValue(rawValue);

        input.value = "";

        if (!normalizedValue) {
            return;
        }

        if (state.values.some((value) => value.toLowerCase() === normalizedValue.toLowerCase())) {
            return;
        }

        state.values.push(normalizedValue);
        renderSelectedTags();
        renderSuggestions();
        onChange();
    }

    function removeValue(valueToRemove) {
        state.values = state.values.filter((value) => value.toLowerCase() !== valueToRemove.toLowerCase());
        renderSelectedTags();
        renderSuggestions();
        onChange();
    }

    function renderSelectedTags() {
        tagList.innerHTML = state.values
            .map(
                (value) => `
                    <span class="selected-tag">
                        <span>${escapeHtml(value)}</span>
                        <button type="button" data-tag-remove="${escapeHtml(value)}" aria-label="Remove ${escapeHtml(value)}">x</button>
                    </span>
                `
            )
            .join("");

        tagList.querySelectorAll("[data-tag-remove]").forEach((button) => {
            button.addEventListener("click", () => removeValue(button.dataset.tagRemove));
        });
    }

    function renderSuggestions() {
        suggestionsContainer.innerHTML = suggestions
            .map((value) => {
                const selected = state.values.some((item) => item.toLowerCase() === value.toLowerCase());
                return `<button type="button" class="suggestion-chip${selected ? " is-selected" : ""}" data-suggestion="${escapeHtml(value)}">${escapeHtml(toTitleCase(value))}</button>`;
            })
            .join("");

        suggestionsContainer.querySelectorAll("[data-suggestion]").forEach((button) => {
            button.addEventListener("click", () => addValue(button.dataset.suggestion));
        });
    }

    return {
        getValues() {
            return [...state.values];
        },
    };
}

function normalizePickerValue(value) {
    return String(value || "").trim().replace(/\s+/g, " ");
}

function normalizeRequestList(value) {
    if (Array.isArray(value)) {
        return value.filter(Boolean);
    }

    if (typeof value === "string" && value.trim()) {
        return [value.trim()];
    }

    return [];
}

function toTitleCase(value) {
    return String(value || "")
        .toLowerCase()
        .replace(/\b\w/g, (character) => character.toUpperCase());
}

function setFieldError(field, errorSelector, message) {
    const errorElement = document.querySelector(errorSelector);
    field.setAttribute("aria-invalid", "true");

    if (errorElement) {
        errorElement.textContent = message;
    }
}

function clearFieldError(field) {
    if (!field) {
        return;
    }

    field.removeAttribute("aria-invalid");

    const errorElement = document.querySelector(`#${field.id}-error`);

    if (errorElement) {
        errorElement.textContent = "";
    }

    if (field.id === "duration-unit") {
        const durationError = document.querySelector("#duration-error");

        if (durationError) {
            durationError.textContent = "";
        }
    }

    if (field.id === "duration-value") {
        const durationUnit = document.querySelector("#duration-unit");

        if (durationUnit) {
            durationUnit.removeAttribute("aria-invalid");
        }
    }
}

function showMessage(element, message, tone = "success") {
    if (!element) {
        return;
    }

    element.textContent = message;
    element.classList.add("is-visible");
    element.classList.remove("is-error", "is-success");
    element.classList.add(tone === "error" ? "is-error" : "is-success");
}

function hideMessage(element) {
    if (!element) {
        return;
    }

    element.textContent = "";
    element.classList.remove("is-visible", "is-error", "is-success");
}

// Reads text from sessionStorage and tries to turn it back into a Javascript object using JSON.parse()
function safelyParseStorage(storageKey) {
    const storedValue = sessionStorage.getItem(storageKey);

    if (!storedValue) {
        return null;
    }

    try {
        return JSON.parse(storedValue);
    } catch (error) {
        console.warn(`Could not parse sessionStorage item ${storageKey}:`, error);
        return null;
    }
}

function setText(selector, value) {
    const element = document.querySelector(selector);

    if (element && typeof value === "string") {
        element.textContent = value;
    }
}

function convertDurationToMinutes(value, unit) {
    if (unit === "hours") {
        return value * 60;
    }

    if (unit === "days") {
        return value * 8 * 60;
    }

    return value;
}

function formatDuration(value, unit) {
    if (unit === "hours") {
        return `${value} hr`;
    }

    if (unit === "days") {
        return `${value} day${value === 1 ? "" : "s"}`;
    }

    return `${value} min`;
}

function sumActivityTimes(activities) {
    const totalMinutes = activities.reduce((sum, activity) => {
        const match = String(activity.time || "").match(/(\d+)/);

        if (!match) {
            return sum;
        }

        return sum + Number.parseInt(match[1], 10);
    }, 0);

    return totalMinutes > 0 ? `${totalMinutes} min` : "";
}

function inferTagType(index) {
    if (index === 0) {
        return "difficulty";
    }

    if (index === 1) {
        return "topic";
    }

    return "duration";
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

async function requestLessonPlan(payload) {
    const response = await fetch("/generate-lesson-plan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const responseData = await response.json().catch(() => null);

    if (!response.ok) {
        throw new Error(responseData?.error || "Failed to generate lesson plan");
    }

    return responseData;
}

/**
 * JanSetu (जनसेतु) — Frontend Application Controller
 * Orchestrates the Public Landing Page, Authentication & Demo Access,
 * Modern Dashboard, Dedicated Scheme Discovery, and 5-Agent Workflow.
 */

// Global Application State
const state = {
    isAuthenticated: false,
    activeUserId: 1,
    currentUser: null,
    allUsers: [],
    activePage: "dashboard",
    workflowStage: 1,
    selectedScheme: null,
    currentMatches: [],
    recommendations: [],
    intakeAnalysis: null,
    confirmedRules: [],
    eligibilityAssessment: null,
    documentReadiness: null,
    applicationDraft: null,
    submittedApplication: null,
    allSchemes: [],
    allApplications: [],
    allDocuments: [],
    notifications: [],
    chatSessionId: "jansetu_session_" + Math.random().toString(36).substring(2, 9),
    currentLang: localStorage.getItem("jansetu_lang") || "en"
};

// ==============================================================
// Multilingual Translation Engine (5 Languages)
// ==============================================================

function t(key, fallback = "") {
    const lang = state.currentLang || "en";
    if (window.TRANSLATIONS && window.TRANSLATIONS[lang] && window.TRANSLATIONS[lang][key] !== undefined) {
        return window.TRANSLATIONS[lang][key];
    }
    if (window.TRANSLATIONS && window.TRANSLATIONS["en"] && window.TRANSLATIONS["en"][key] !== undefined) {
        return window.TRANSLATIONS["en"][key];
    }
    return fallback || key;
}

async function changeLanguage(langCode, saveToProfile = true) {
    if (!["en", "hi", "mr", "bn", "ta"].includes(langCode)) langCode = "en";
    state.currentLang = langCode;
    localStorage.setItem("jansetu_lang", langCode);

    // Sync all dropdowns
    const appSelect = document.getElementById("app-lang-select");
    if (appSelect) appSelect.value = langCode;
    const landingSelect = document.getElementById("landing-lang-select");
    if (landingSelect) landingSelect.value = langCode;

    // Update document HTML lang attribute
    document.documentElement.lang = langCode;

    // Translate DOM elements with data-i18n
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const val = t(key);
        if (val) {
            const icon = el.querySelector("i");
            if (icon) {
                const iconHtml = icon.outerHTML;
                el.innerHTML = `${iconHtml} <span>${escapeHtml(val)}</span>`;
            } else {
                el.textContent = val;
            }
        }
    });

    // Translate placeholders
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        const val = t(key);
        if (val) el.placeholder = val;
    });

    // Translate titles
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
        const key = el.getAttribute("data-i18n-title");
        const val = t(key);
        if (val) el.title = val;
    });

    // Refresh dynamic components without wiping workflow or form inputs
    refreshDynamicTranslations();

    // Persist to user profile backend if logged in
    if (saveToProfile && state.currentUser && state.currentUser.id) {
        try {
            await fetch(`/api/users/${state.currentUser.id}/language`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ language: langCode })
            });
            if (state.currentUser.raw_attributes) {
                state.currentUser.raw_attributes.preferred_language = langCode;
            }
        } catch (err) {
            console.warn("Could not persist language to user profile:", err);
        }
    }
}

function refreshDynamicTranslations() {
    // 1. Profile mode badges and buttons
    const badgeReadonly = document.getElementById("profile-badge-readonly");
    if (badgeReadonly) badgeReadonly.innerHTML = `<i class="fa-solid fa-lock"></i> <span>${t("profile_readonly_badge", "Verified Profile (Read-Only)")}</span>`;
    const badgeEditing = document.getElementById("profile-badge-editing");
    if (badgeEditing) badgeEditing.innerHTML = `<i class="fa-solid fa-pen-to-square"></i> <span>${t("profile_edit_badge", "Editing Mode Active")}</span>`;
    
    const btnEdit = document.getElementById("btn-edit-profile");
    if (btnEdit) {
        const span = btnEdit.querySelector("span");
        if (span) span.textContent = t("btn_edit_profile", "Edit Profile");
    }
    const btnCancel = document.getElementById("btn-cancel-profile");
    if (btnCancel) {
        const span = btnCancel.querySelector("span");
        if (span) span.textContent = t("btn_cancel", "Cancel");
    }
    const btnSave = document.getElementById("btn-save-profile");
    if (btnSave) {
        const span = btnSave.querySelector("span");
        if (span) span.textContent = t("btn_save_changes", "Save Changes");
    }

    // 2. Mitra Drawer Suggestions
    renderMitraDrawerSuggestions();

    // 3. Schemes Catalog Card Refresh (preserving existing list and state)
    if (state.allSchemes && state.allSchemes.length > 0) {
        const grid = document.getElementById("catalog-schemes-grid");
        if (grid && grid.children.length > 0) {
            renderCatalogSchemes(state.allSchemes);
        }
        renderPublicSchemesPreview();
    }

    // 4. Dashboard Banner text
    if (state.currentUser) {
        updateDashboardBanner();
    }
}

function renderMitraDrawerSuggestions(customPrompts) {
    const container = document.querySelector(".drawer-suggestions");
    if (!container) return;

    const prompts = customPrompts || [
        t("prompt_q1", "What documents are required for PM-KISAN?"),
        t("prompt_q2", "Am I eligible for PM SVANidhi?"),
        t("prompt_q3", "How can I check my application status?")
    ];

    container.innerHTML = prompts.map(p => `
        <button type="button" class="drawer-chip" onclick="sendChatPrompt('${escapeHtml(p).replace(/'/g, "\\'")}')">${escapeHtml(p)}</button>
    `).join("");
}

// ==============================================================
// DOM Content Loaded Initializer
// ==============================================================

document.addEventListener("DOMContentLoaded", async () => {
    setupEventListeners();
    await checkAuthAndInitialize();
});

async function checkAuthAndInitialize() {
    // Initialize language from localStorage or default 'en'
    const savedLang = localStorage.getItem("jansetu_lang") || "en";
    state.currentLang = savedLang;
    changeLanguage(savedLang, false);

    // Check if session exists in localStorage
    const savedUserJson = localStorage.getItem("jansetu_user") || localStorage.getItem("sahayak_user");
    
    // Always load public scheme preview & user personas in background
    await loadUsersAndPersonas();
    await loadSchemesCatalog();

    if (savedUserJson) {
        try {
            const user = JSON.parse(savedUserJson);
            state.isAuthenticated = true;
            state.activeUserId = user.id;
            state.currentUser = user;

            // If user has a preferred language in profile, apply it
            if (user.raw_attributes && user.raw_attributes.preferred_language) {
                state.currentLang = user.raw_attributes.preferred_language;
                localStorage.setItem("jansetu_lang", state.currentLang);
                changeLanguage(state.currentLang, false);
            }

            showPortalApp();
            await refreshUserData(user.id);
            return;
        } catch (e) {
            console.error("Invalid saved session:", e);
            localStorage.removeItem("jansetu_user");
            localStorage.removeItem("sahayak_user");
        }
    }

    // Default: Show Public Landing Page
    showPublicLanding();
}


function setupEventListeners() {
    // Keyboard Escape to close modals
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeAuthModal();
            closeSchemeDetailsModal();
            toggleNotificationsModal(false);
            toggleChatbot(false);
            closeUploadDocModal();
            closeDeleteDocModal();
        }
    });

    // File Drag and Drop Support
    const dropZone = document.getElementById("upload-file-drop-zone");
    const fileInput = document.getElementById("upload-modal-file");
    if (dropZone && fileInput) {
        ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
            dropZone.addEventListener(eventName, e => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ["dragenter", "dragover"].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add("drag-over");
            }, false);
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove("drag-over");
            }, false);
        });

        dropZone.addEventListener("drop", e => {
            const dt = e.dataTransfer;
            const files = dt?.files;
            if (files && files.length > 0) {
                fileInput.files = files;
                handleFileSelection(fileInput);
            }
        }, false);
    }
}

// ==============================================================
// View Switching: Public Landing vs Portal
// ==============================================================

function showPublicLanding() {
    document.getElementById("view-landing").style.display = "flex";
    document.getElementById("view-portal").style.display = "none";
    renderPublicSchemesPreview();
}

function showPortalApp() {
    document.getElementById("view-landing").style.display = "none";
    document.getElementById("view-portal").style.display = "flex";
    navigateToPage(state.activePage || "dashboard");
}

function handleStartWithNeed() {
    if (state.isAuthenticated) {
        showPortalApp();
        navigateToPage("assistant");
    } else {
        openAuthModal("demo");
    }
}

async function startQuickInteractiveDemo() {
    // Instant demo login as Ramesh Kumar (Farmer) and jump to AI Assistant
    await loginAsDemoPersona("ramesh_farmer");
    navigateToPage("assistant");
}

function openPublicDirectory() {
    if (state.isAuthenticated) {
        showPortalApp();
        navigateToPage("schemes");
    } else {
        openAuthModal("demo");
    }
}

// ==============================================================
// Authentication & Demo Session Management
// ==============================================================

function openAuthModal(initialTab = "demo") {
    const modal = document.getElementById("auth-modal");
    modal.style.display = "flex";
    switchAuthTab(`auth-tab-${initialTab}`);
}

function closeAuthModal() {
    document.getElementById("auth-modal").style.display = "none";
}

function switchAuthTab(tabId) {
    document.querySelectorAll(".auth-tab-btn").forEach(btn => {
        btn.classList.toggle("active", btn.getAttribute("data-auth-tab") === tabId);
    });
    document.querySelectorAll(".auth-tab-content").forEach(content => {
        content.classList.toggle("active", content.id === tabId);
    });
    if (tabId === "auth-tab-register" && typeof backToRegistrationForm === "function") {
        backToRegistrationForm();
    }
}


async function loginAsDemoPersona(personaKey) {
    try {
        const res = await fetch("/api/users/demo-session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ persona: personaKey })
        });
        const data = await res.json();
        if (res.ok && data.user) {
            setAuthenticatedUser(data.user);
            closeAuthModal();
            showToast(`Logged in as demo citizen: ${data.user.full_name}`, "success");
        } else {
            showToast(data.detail || "Error establishing demo session", "error");
        }
    } catch (err) {
        console.error("Demo login failed:", err);
        showToast("Backend connection error. Retrying...", "error");
    }
}

async function handleSignInSubmit(event) {
    event.preventDefault();
    const identifier = document.getElementById("signin-identifier").value.trim();
    if (!identifier) return;

    try {
        const res = await fetch("/api/users/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ identifier })
        });
        const data = await res.json();
        if (res.ok && data.user) {
            setAuthenticatedUser(data.user);
            closeAuthModal();
            showToast(`Welcome back, ${data.user.full_name}!`, "success");
        } else {
            showToast(data.detail || "Citizen not found. Please try instant demo access.", "error");
        }
    } catch (err) {
        console.error("Sign in failed:", err);
        showToast("Sign in failed. Check backend connection.", "error");
    }
}

// ==============================================================
// Citizen Registration Controller (5 Sections + Review Step)
// ==============================================================

let pendingRegistrationPayload = null;

function showRegAlert(message, type = "danger") {
    const alertBox = document.getElementById("reg-alert-box");
    if (!alertBox) return;

    let icon = "fa-circle-exclamation";
    if (type === "success") icon = "fa-circle-check";
    if (type === "info") icon = "fa-circle-info";

    alertBox.className = `profile-alert alert-${type}`;
    alertBox.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <div style="flex: 1;">${escapeHtml(message)}</div>
        <button type="button" class="btn-close-alert" onclick="this.parentElement.style.display='none'" style="background:none; border:none; color:inherit; cursor:pointer; font-size:18px; line-height:1;">&times;</button>
    `;
    alertBox.style.display = "flex";
    alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function validateRegistrationForm() {
    // Clear old errors
    document.querySelectorAll("#form-register .has-error").forEach(el => el.classList.remove("has-error"));
    const alertBox = document.getElementById("reg-alert-box");
    if (alertBox) alertBox.style.display = "none";

    const fullName = document.getElementById("reg-fullname")?.value.trim() || "";
    const username = document.getElementById("reg-username")?.value.trim() || "";
    const email = document.getElementById("reg-email")?.value.trim() || "";
    const phone = document.getElementById("reg-phone")?.value.trim() || "";
    const password = document.getElementById("reg-password")?.value || "";
    const confirmPassword = document.getElementById("reg-confirm-password")?.value || "";

    const ageVal = document.getElementById("reg-age")?.value.trim() || "";
    const age = parseInt(ageVal, 10);
    const gender = document.getElementById("reg-gender")?.value || "";

    const occupation = document.getElementById("reg-occupation")?.value.trim() || "";
    const incomeVal = document.getElementById("reg-income")?.value.trim() || "";
    const income = parseFloat(incomeVal);
    const category = document.getElementById("reg-category")?.value || "";
    const bplStatus = document.getElementById("reg-bpl")?.value || "";

    const stateVal = document.getElementById("reg-state")?.value.trim() || "";
    const districtVal = document.getElementById("reg-district")?.value.trim() || "";
    const residence = document.getElementById("reg-residence")?.value || "";

    const landVal = document.getElementById("reg-land")?.value.trim() || "";
    const land = landVal ? parseFloat(landVal) : 0.0;
    const marital = document.getElementById("reg-marital")?.value || "";
    const pwd = document.getElementById("reg-pwd")?.value || "";
    const familyCountVal = document.getElementById("reg-family-count")?.value.trim() || "";
    const familyCount = familyCountVal ? parseInt(familyCountVal, 10) : 1;

    // SECTION A VALIDATION
    if (!fullName || fullName.length < 2) {
        return { isValid: false, message: "Full Name is required (at least 2 characters).", fieldId: "reg-fullname" };
    }
    if (!username || username.length < 3) {
        return { isValid: false, message: "Username is required (at least 3 characters).", fieldId: "reg-username" };
    }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return { isValid: false, message: "Please provide a valid email address.", fieldId: "reg-email" };
    }
    if (phone && !/^[0-9+\-\s]{8,15}$/.test(phone)) {
        return { isValid: false, message: "Please enter a valid phone number (at least 8 digits).", fieldId: "reg-phone" };
    }
    if (!password || password.length < 6) {
        return { isValid: false, message: "Password is required (minimum 6 characters).", fieldId: "reg-password" };
    }
    if (password !== confirmPassword) {
        return { isValid: false, message: "Password and Confirm Password do not match.", fieldId: "reg-confirm-password" };
    }

    // SECTION B VALIDATION
    if (!ageVal || isNaN(age) || age < 1 || age > 120) {
        return { isValid: false, message: "Please provide a valid Age between 1 and 120 years.", fieldId: "reg-age" };
    }
    if (!gender) {
        return { isValid: false, message: "Please select your Gender from the dropdown (no option is preselected).", fieldId: "reg-gender" };
    }

    // SECTION C VALIDATION
    if (!occupation) {
        return { isValid: false, message: "Occupation / Primary Trade is required for scheme eligibility.", fieldId: "reg-occupation" };
    }
    if (!incomeVal || isNaN(income) || income < 0) {
        return { isValid: false, message: "Please provide your Annual Family Income (0 or greater).", fieldId: "reg-income" };
    }
    if (!category) {
        return { isValid: false, message: "Please select your Social Category from the dropdown.", fieldId: "reg-category" };
    }
    if (!bplStatus) {
        return { isValid: false, message: "Please select your BPL / Antyodaya status (Yes, No, or Not Sure).", fieldId: "reg-bpl" };
    }

    // SECTION D VALIDATION
    if (!stateVal) {
        return { isValid: false, message: "State of residence is required.", fieldId: "reg-state" };
    }
    if (!districtVal) {
        return { isValid: false, message: "District is required.", fieldId: "reg-district" };
    }
    if (!residence) {
        return { isValid: false, message: "Please select your Residence Area type (Rural, Semi-Urban, or Urban).", fieldId: "reg-residence" };
    }

    // SECTION E VALIDATION
    if (isNaN(land) || land < 0) {
        return { isValid: false, message: "Agricultural landholding cannot be negative.", fieldId: "reg-land" };
    }
    if (isNaN(familyCount) || familyCount < 1) {
        return { isValid: false, message: "Family members count must be at least 1.", fieldId: "reg-family-count" };
    }

    return {
        isValid: true,
        payload: {
            full_name: fullName,
            username: username,
            email: email,
            phone: phone,
            password: password,
            age: age,
            gender: gender,
            occupation: occupation,
            annual_income: income,
            social_category: category,
            bpl_status: bplStatus,
            is_bpl: bplStatus === "Yes",
            state: stateVal,
            district: districtVal,
            residence_area: residence,
            land_ownership_hectares: land,
            marital_status: marital || "Single",
            is_differently_abled: pwd === "1",
            family_members_count: familyCount
        }
    };
}

function handleReviewRegistration(event) {
    if (event) event.preventDefault();

    const validation = validateRegistrationForm();
    if (!validation.isValid) {
        const inputEl = document.getElementById(validation.fieldId);
        if (inputEl) {
            inputEl.classList.add("has-error");
            inputEl.focus();
        }
        showRegAlert(validation.message, "danger");
        showToast(validation.message, "error");
        return;
    }

    pendingRegistrationPayload = validation.payload;
    renderRegistrationReviewCard(pendingRegistrationPayload);

    // Switch view from form to review
    document.getElementById("reg-step-form").style.display = "none";
    document.getElementById("reg-step-review").style.display = "block";
    const tabEl = document.getElementById("auth-tab-register");
    if (tabEl) tabEl.scrollTop = 0;
}

function backToRegistrationForm() {
    const stepForm = document.getElementById("reg-step-form");
    const stepReview = document.getElementById("reg-step-review");
    if (stepForm) stepForm.style.display = "block";
    if (stepReview) stepReview.style.display = "none";
}

function renderRegistrationReviewCard(p) {
    const container = document.getElementById("reg-review-summary-content");
    if (!container) return;

    container.innerHTML = `
        <div class="reg-review-section">
            <div class="reg-review-section-title"><i class="fa-solid fa-shield-halved"></i> A. Account Information</div>
            <div class="reg-review-grid">
                <div class="reg-review-item"><label>Full Legal Name</label><div class="val">${escapeHtml(p.full_name)}</div></div>
                <div class="reg-review-item"><label>Username</label><div class="val">@${escapeHtml(p.username)}</div></div>
                <div class="reg-review-item"><label>Email Address</label><div class="val">${escapeHtml(p.email)}</div></div>
                <div class="reg-review-item"><label>Mobile Phone</label><div class="val">${escapeHtml(p.phone || 'Not Provided')}</div></div>
            </div>
        </div>

        <div class="reg-review-section">
            <div class="reg-review-section-title"><i class="fa-solid fa-user"></i> B. Personal Information</div>
            <div class="reg-review-grid">
                <div class="reg-review-item"><label>Age</label><div class="val">${p.age} Years</div></div>
                <div class="reg-review-item"><label>Gender</label><div class="val">${escapeHtml(p.gender)}</div></div>
            </div>
        </div>

        <div class="reg-review-section">
            <div class="reg-review-section-title"><i class="fa-solid fa-coins"></i> C. Socio-Economic Information</div>
            <div class="reg-review-grid">
                <div class="reg-review-item"><label>Occupation / Trade</label><div class="val">${escapeHtml(p.occupation)}</div></div>
                <div class="reg-review-item"><label>Annual Family Income</label><div class="val">₹${p.annual_income.toLocaleString('en-IN')}/year</div></div>
                <div class="reg-review-item"><label>Social Category</label><div class="val">${escapeHtml(p.social_category)}</div></div>
                <div class="reg-review-item"><label>BPL / Antyodaya Status</label><div class="val">${escapeHtml(p.bpl_status)}</div></div>
            </div>
        </div>

        <div class="reg-review-section">
            <div class="reg-review-section-title"><i class="fa-solid fa-location-dot"></i> D. Residential Information</div>
            <div class="reg-review-grid">
                <div class="reg-review-item"><label>State</label><div class="val">${escapeHtml(p.state)}</div></div>
                <div class="reg-review-item"><label>District</label><div class="val">${escapeHtml(p.district)}</div></div>
                <div class="reg-review-item"><label>Area Type</label><div class="val">${escapeHtml(p.residence_area)}</div></div>
            </div>
        </div>

        <div class="reg-review-section">
            <div class="reg-review-section-title"><i class="fa-solid fa-id-badge"></i> E. Additional Eligibility Details</div>
            <div class="reg-review-grid">
                <div class="reg-review-item"><label>Agricultural Land</label><div class="val">${p.land_ownership_hectares > 0 ? p.land_ownership_hectares + ' Hectares' : 'None (0.0 ha)'}</div></div>
                <div class="reg-review-item"><label>Family Members</label><div class="val">${p.family_members_count} Members</div></div>
                <div class="reg-review-item"><label>Marital Status</label><div class="val">${escapeHtml(p.marital_status || 'Single')}</div></div>
                <div class="reg-review-item"><label>Differently Abled (PwD)</label><div class="val">${p.is_differently_abled ? 'Yes (40%+ Disability)' : 'No'}</div></div>
            </div>
        </div>
    `;
}

async function executeFinalRegistration() {
    if (!pendingRegistrationPayload) {
        backToRegistrationForm();
        return;
    }

    const submitBtn = document.getElementById("btn-submit-final-register");
    if (submitBtn) {
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Creating Account...`;
        submitBtn.disabled = true;
    }

    try {
        const res = await fetch("/api/users/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(pendingRegistrationPayload)
        });
        const data = await res.json();

        if (res.ok && data.user) {
            setAuthenticatedUser(data.user);
            closeAuthModal();
            showToast(`Welcome ${data.user.full_name}! Account created and profile verified.`, "success");
        } else {
            const errDetail = data.detail || data.message || "Registration failed.";
            backToRegistrationForm();
            showRegAlert(errDetail, "danger");
            showToast(errDetail, "error");
        }
    } catch (err) {
        console.error("Registration error:", err);
        backToRegistrationForm();
        showRegAlert("Connection error during registration. Please check server.", "danger");
        showToast("Registration network error. Please try again.", "error");
    } finally {
        if (submitBtn) {
            submitBtn.innerHTML = `<i class="fa-solid fa-user-check"></i> Confirm & Create Account`;
            submitBtn.disabled = false;
        }
    }
}


function setAuthenticatedUser(user) {
    state.isAuthenticated = true;
    state.activeUserId = user.id;
    state.currentUser = user;
    if (user.raw_attributes && user.raw_attributes.preferred_language) {
        state.currentLang = user.raw_attributes.preferred_language;
        localStorage.setItem("jansetu_lang", state.currentLang);
        changeLanguage(state.currentLang, false);
    }
    localStorage.setItem("jansetu_user", JSON.stringify(user));
    localStorage.setItem("sahayak_user", JSON.stringify(user));
    showPortalApp();
    refreshUserData(user.id);
}


function handleLogout() {
    localStorage.removeItem("jansetu_user");
    localStorage.removeItem("sahayak_user");
    state.isAuthenticated = false;
    state.currentUser = null;
    showPublicLanding();
    showToast("Signed out successfully.");
}

async function loadUsersAndPersonas() {
    try {
        const res = await fetch("/api/users");
        const data = await res.json();
        state.allUsers = data.users || [];

        const select = document.getElementById("persona-select-sidebar");
        if (select) {
            select.innerHTML = "";
            state.allUsers.forEach(u => {
                const opt = document.createElement("option");
                opt.value = u.id;
                opt.textContent = `${u.full_name} (${u.occupation || 'Citizen'})`;
                select.appendChild(opt);
            });
        }
    } catch (err) {
        console.error("Failed to load personas:", err);
    }
}

async function switchPersonaFromSidebar(userId) {
    await switchActivePersona(parseInt(userId));
}

async function switchActivePersona(userId) {
    try {
        const res = await fetch(`/api/users/${userId}`);
        const data = await res.json();
        if (res.ok && data.user) {
            setAuthenticatedUser(data.user);
        }
    } catch (err) {
        console.error("Failed to switch persona:", err);
    }
}

async function refreshUserData(userId) {
    updateTopBarProfile();
    updateDashboardBanner();
    populateProfileForm();
    await Promise.all([
        loadUserApplications(),
        loadUserDocuments(),
        loadNotifications()
    ]);
    updateDashboardMetrics();
    renderActiveApplicationsList();
    renderRecentActivityLog();
}

function updateTopBarProfile() {
    if (!state.currentUser) return;
    const name = state.currentUser.full_name || "Citizen";
    const occupation = state.currentUser.occupation || "Citizen";
    
    const initialEl = document.getElementById("user-avatar-initial");
    const nameEl = document.getElementById("user-display-name");
    const roleEl = document.getElementById("user-display-occupation");

    if (initialEl) initialEl.textContent = name.charAt(0).toUpperCase();
    if (nameEl) nameEl.textContent = name;
    if (roleEl) roleEl.textContent = occupation;

    const select = document.getElementById("persona-select-sidebar");
    if (select) select.value = state.activeUserId;
}

function updateDashboardBanner() {
    if (!state.currentUser) return;
    const nameEl = document.getElementById("dash-citizen-name");
    const summaryEl = document.getElementById("dash-citizen-summary");
    const chipEl = document.getElementById("assistant-citizen-chip");

    const u = state.currentUser;
    const text = `${u.occupation || 'Citizen'} • ${u.state || 'India'} • Income: ₹${(u.annual_income || 100000).toLocaleString('en-IN')}`;
    
    if (nameEl) nameEl.textContent = u.full_name;
    if (summaryEl) summaryEl.textContent = `Profile verified for ${text}. Your 5-agent workforce is ready.`;
    if (chipEl) {
        chipEl.innerHTML = `<i class="fa-solid fa-user-check"></i> <strong>Active Profile:</strong> ${u.full_name} (${u.occupation || 'Citizen'}), ₹${(u.annual_income || 100000).toLocaleString('en-IN')}/yr, ${u.state || 'India'}`;
    }

    // Configure persona-specific Next Best Action
    updateNextBestActionCard();
}

function updateNextBestActionCard() {
    const titleEl = document.getElementById("dash-next-action-title");
    const descEl = document.getElementById("dash-next-action-desc");
    const btnEl = document.getElementById("btn-next-action-cta");
    if (!titleEl || !state.currentUser) return;

    const occ = (state.currentUser.occupation || "").toLowerCase();
    if (occ.includes("farmer")) {
        titleEl.textContent = "Audit Your Eligibility for PM-KISAN ₹6,000 Income Support";
        descEl.textContent = `Based on your agricultural landholding (${state.currentUser.land_ownership_hectares || 1.4} ha in Rajasthan), you meet statutory criteria for ₹6,000 yearly Direct Benefit Transfer.`;
        btnEl.setAttribute("data-query", "I am a farmer and need PM KISAN income support.");
    } else if (occ.includes("vendor") || occ.includes("artisan") || occ.includes("stall")) {
        titleEl.textContent = "Claim ₹10,000 Working Capital via PM SVANidhi";
        descEl.textContent = "Street vendors and urban artisans are eligible for collateral-free micro-credit loans with a 7% interest subsidy.";
        btnEl.setAttribute("data-query", "I run a street cart and need working capital loan.");
    } else if (occ.includes("student")) {
        titleEl.textContent = "Discover Higher Education Scholarship Reimbursements";
        descEl.textContent = "Undergraduate students from weaker economic backgrounds can receive tuition fee reimbursements and book grants.";
        btnEl.setAttribute("data-query", "I am an undergraduate college student needing education scholarship.");
    } else {
        titleEl.textContent = "Explore Housing & Social Welfare Assistance";
        descEl.textContent = "Discover central and state welfare initiatives matching your household income.";
        btnEl.setAttribute("data-query", "I need government welfare assistance for my family.");
    }
}

function handleDashboardNextAction() {
    const btnEl = document.getElementById("btn-next-action-cta");
    const query = btnEl.getAttribute("data-query") || "I need government welfare assistance for my family.";
    navigateToPage("assistant");
    fillAssistantPrompt(query);
    executeSchemeDiscovery();
}

// ==============================================================
// Portal Navigation
// ==============================================================

function navigateToPage(pageId) {
    state.activePage = pageId;

    // Update Sidebar active state
    document.querySelectorAll(".sidebar-item").forEach(item => {
        item.classList.toggle("active", item.getAttribute("data-page") === pageId);
    });

    // Update Page Viewport active panel
    document.querySelectorAll(".page-panel").forEach(panel => {
        panel.classList.toggle("active", panel.id === `page-${pageId}`);
    });

    // Page-specific refreshes
    if (pageId === "schemes") {
        renderCatalogSchemes(state.allSchemes);
    } else if (pageId === "applications") {
        renderApplicationsPage();
    } else if (pageId === "documents") {
        renderDocumentsPage();
    } else if (pageId === "notifications") {
        renderNotificationsPage();
    } else if (pageId === "profile") {
        setProfileEditMode(false);
        populateProfileForm();
    } else if (pageId === "dashboard") {
        updateDashboardMetrics();
    }
}

function handleGlobalSearch(event) {
    if (event.key === "Enter") {
        const query = event.target.value.trim();
        if (!query) return;
        navigateToPage("schemes");
        const catalogSearchInput = document.getElementById("catalog-search-input");
        if (catalogSearchInput) {
            catalogSearchInput.value = query;
            filterCatalogSchemes();
        }
    }
}

// ==============================================================
// Dashboard Metrics & Lists
// ==============================================================

function updateDashboardMetrics() {
    const appsCountEl = document.getElementById("dash-metric-apps");
    const docsCountEl = document.getElementById("dash-metric-docs");
    const actionsCountEl = document.getElementById("dash-metric-actions");
    const sidebarAppCountEl = document.getElementById("sidebar-app-count");

    if (appsCountEl) appsCountEl.textContent = state.allApplications.length;
    if (sidebarAppCountEl) sidebarAppCountEl.textContent = state.allApplications.length;
    if (docsCountEl) docsCountEl.textContent = state.allDocuments.length;
    if (actionsCountEl) actionsCountEl.textContent = state.allApplications.length === 0 ? "1" : "0";
}

function renderActiveApplicationsList() {
    const container = document.getElementById("dash-active-apps-list");
    if (!container) return;

    if (state.allApplications.length === 0) {
        container.innerHTML = `
            <div class="empty-state-box">
                <div class="empty-state-icon"><i class="fa-regular fa-folder-open"></i></div>
                <h4>No Applications In Progress</h4>
                <p>You haven't initiated any welfare scheme application yet. Run the AI Assistant to discover schemes and create your first draft.</p>
                <button class="btn btn-primary btn-sm" onclick="navigateToPage('assistant')">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Start Scheme Discovery
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = state.allApplications.slice(0, 3).map(app => `
        <div class="app-record-card" style="margin-bottom: 10px; padding: 14px 18px;">
            <div class="app-record-info">
                <h4>${escapeHtml(app.scheme_name || 'Government Scheme')}</h4>
                <span class="app-ref-tag">${escapeHtml(app.application_ref || app.reference_no || 'JS-2025')}</span>
                <div class="app-record-meta">Applied on: ${new Date(app.submitted_at || app.created_at || Date.now()).toLocaleDateString()}</div>
            </div>
            <div>
                <span class="status-chip success">${escapeHtml(app.status || 'SUBMITTED')}</span>
                <button class="btn btn-outline btn-sm ml-2" onclick="navigateToPage('applications')">Track &rarr;</button>
            </div>
        </div>
    `).join("");
}

function renderRecentActivityLog() {
    const container = document.getElementById("dash-activity-log");
    if (!container) return;

    const activities = [
        { title: "Scheme Matcher Agent indexed 89 schemes", sub: "Qdrant dense vector collection verified with 384-dimensional embeddings." },
        { title: "Statutory Eligibility Rule Audit", sub: "Evaluated statutory age, landownership and income ceilings." },
        { title: "Document Readiness Scrutiny", sub: "Demo locker verified with Masked Aadhaar and bank proof." }
    ];

    if (state.allApplications.length > 0) {
        const latest = state.allApplications[0];
        activities.unshift({
            title: `Application Prepared: ${latest.application_ref}`,
            sub: `Draft for ${latest.scheme_name} registered in SQLite tracking registry.`
        });
    }

    container.innerHTML = activities.map(a => `
        <div class="activity-item">
            <div class="activity-dot"></div>
            <div class="activity-content">
                <strong>${escapeHtml(a.title)}</strong>
                <span>${escapeHtml(a.sub)}</span>
            </div>
        </div>
    `).join("");
}

// ==============================================================
// Schemes Catalog (Dedicated Discovery Interface)
// ==============================================================

async function loadSchemesCatalog() {
    try {
        const res = await fetch("/api/schemes");
        const data = await res.json();
        state.allSchemes = data.schemes || [];
        renderCatalogSchemes(state.allSchemes);
        renderPublicSchemesPreview();
    } catch (err) {
        console.error("Failed to fetch schemes catalog:", err);
    }
}

function renderCatalogSchemes(schemesToRender) {
    const grid = document.getElementById("catalog-schemes-grid");
    const countBadge = document.getElementById("catalog-count-badge");
    if (!grid) return;

    if (countBadge) countBadge.textContent = `${schemesToRender.length} Schemes`;

    if (schemesToRender.length === 0) {
        grid.innerHTML = `
            <div class="empty-state-box" style="grid-column: 1 / -1;">
                <div class="empty-state-icon"><i class="fa-solid fa-magnifying-glass"></i></div>
                <h4>No Matching Schemes Found</h4>
                <p>Try searching with another keyword (e.g. Kisan, Awas, Scholar, Loan, Pension) or reset filters.</p>
                <button class="btn btn-secondary btn-sm" onclick="resetCatalogFilters()">Reset All Filters</button>
            </div>
        `;
        return;
    }

    grid.innerHTML = schemesToRender.map(s => createSchemeCardHtml(s, false)).join("");
}

function renderPublicSchemesPreview() {
    const container = document.getElementById("public-schemes-preview");
    if (!container || state.allSchemes.length === 0) return;

    // Pick 3 popular diverse schemes for public preview
    const previewList = state.allSchemes.slice(0, 3);
    container.innerHTML = previewList.map(s => createSchemeCardHtml(s, false, true)).join("");
}

function createSchemeCardHtml(scheme, isRecommendation = false, isPublic = false) {
    const benefits = scheme.benefits || "Financial assistance and welfare subsidies.";
    const level = scheme.level || "Central";
    const stateName = scheme.state || "All India";
    const matchScore = scheme.match_score || 85;
    const isRec = scheme.is_recommended || isRecommendation;

    return `
        <div class="scheme-card ${isRec ? 'is-recommended' : ''}" data-scheme-id="${scheme.id}">
            ${isRec ? `<div class="recommended-ribbon"><i class="fa-solid fa-star"></i> Recommended Match (${scheme.match_percentage || matchScore + '%'})</div>` : ''}
            
            <div class="scheme-card-top">
                <div class="scheme-meta-row">
                    <span class="scheme-level-tag">${escapeHtml(level)} • ${escapeHtml(stateName)}</span>
                    <span class="scheme-match-score">${escapeHtml(scheme.category || 'Welfare')}</span>
                </div>
                
                <h3 class="scheme-title">${escapeHtml(scheme.name)}</h3>
                ${scheme.name_hindi ? `<span class="scheme-hindi-title">${escapeHtml(scheme.name_hindi)}</span>` : ''}
                
                <div class="scheme-benefit-pill">
                    <i class="fa-solid fa-gift"></i>
                    <span>${escapeHtml(benefits.length > 75 ? benefits.substring(0, 75) + '...' : benefits)}</span>
                </div>

                <p class="scheme-desc">${escapeHtml(scheme.short_description || '')}</p>
                
                ${scheme.match_rationale ? `
                    <div class="scheme-highlight-box">
                        <strong><i class="fa-solid fa-circle-check" style="color: var(--color-emerald)"></i> Why this matches:</strong>
                        <div>${escapeHtml(scheme.match_rationale)}</div>
                    </div>
                ` : ''}

                ${scheme.official_url ? `
                    <a href="${escapeHtml(scheme.official_url)}" target="_blank" rel="noopener noreferrer" class="scheme-source-link">
                        <span>${t("official_portal", "Official Source Portal")}</span> <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                ` : ''}
            </div>

            <div class="scheme-card-actions">
                <button class="btn btn-secondary btn-sm" onclick="openSchemeDetailsModal(${scheme.id || scheme.scheme_id})">
                    <i class="fa-solid fa-circle-info"></i> <span>${t("btn_view_details", "Details")}</span>
                </button>
                <button class="btn btn-primary btn-sm" onclick="${isPublic ? 'openAuthModal(\'demo\')' : `selectSchemeForWorkflow(${scheme.id || scheme.scheme_id})`}">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> <span>${t("btn_start_application", "Select & Apply")}</span>
                </button>
            </div>

        </div>
    `;
}

function filterCatalogSchemes() {
    const searchVal = (document.getElementById("catalog-search-input")?.value || "").toLowerCase().trim();
    const catVal = document.getElementById("catalog-category-filter")?.value || "All";
    const levelVal = document.getElementById("catalog-level-filter")?.value || "All";

    const filtered = state.allSchemes.filter(s => {
        const matchesQuery = !searchVal || 
            s.name.toLowerCase().includes(searchVal) ||
            (s.name_hindi && s.name_hindi.includes(searchVal)) ||
            (s.short_description && s.short_description.toLowerCase().includes(searchVal)) ||
            (s.benefits && s.benefits.toLowerCase().includes(searchVal)) ||
            (s.code && s.code.toLowerCase().includes(searchVal));

        const matchesCat = (catVal === "All") || (s.category && s.category.toLowerCase().includes(catVal.toLowerCase()));
        const matchesLevel = (levelVal === "All") || (s.level && s.level.toLowerCase() === levelVal.toLowerCase());

        return matchesQuery && matchesCat && matchesLevel;
    });

    renderCatalogSchemes(filtered);
}

function resetCatalogFilters() {
    if (document.getElementById("catalog-search-input")) document.getElementById("catalog-search-input").value = "";
    if (document.getElementById("catalog-category-filter")) document.getElementById("catalog-category-filter").value = "All";
    if (document.getElementById("catalog-level-filter")) document.getElementById("catalog-level-filter").value = "All";
    renderCatalogSchemes(state.allSchemes);
}

// ==============================================================
// Scheme Details Modal
// ==============================================================

function openSchemeDetailsModal(schemeId) {
    const sId = Number(schemeId);
    const scheme = state.allSchemes.find(s => s.id === sId || s.scheme_id === sId) ||
                   state.currentMatches.find(s => s.id === sId || s.scheme_id === sId) ||
                   state.allSchemes.find(s => s.id === schemeId);
    if (!scheme) return;

    scheme.id = scheme.id || scheme.scheme_id || sId;
    scheme.scheme_id = scheme.scheme_id || scheme.id || sId;
    state.selectedScheme = scheme;

    document.getElementById("modal-scheme-level").textContent = `${scheme.level || 'Central'} Scheme • ${scheme.state || 'All India'}`;
    document.getElementById("modal-scheme-name").textContent = scheme.name;
    document.getElementById("modal-scheme-ministry").textContent = scheme.ministry || "Government of India";
    document.getElementById("modal-scheme-benefits").textContent = scheme.benefits || "Direct welfare benefits.";
    document.getElementById("modal-scheme-description").textContent = scheme.full_description || scheme.short_description || "";

    const eligList = document.getElementById("modal-scheme-eligibility");
    eligList.innerHTML = "";
    const rules = scheme.eligibility_criteria?.key_rules || [];
    if (rules.length > 0) {
        rules.forEach(r => {
            const li = document.createElement("li");
            li.textContent = r;
            eligList.appendChild(li);
        });
    } else {
        eligList.innerHTML = "<li>Standard Indian citizen statutory eligibility guidelines apply.</li>";
    }

    const docsContainer = document.getElementById("modal-scheme-documents");
    docsContainer.innerHTML = "";
    const docs = scheme.required_documents || [];
    if (docs.length > 0) {
        docs.forEach(d => {
            const span = document.createElement("span");
            span.className = "tag";
            span.textContent = d;
            docsContainer.appendChild(span);
        });
    } else {
        docsContainer.innerHTML = "<span class=\"tag\">Identity Proof (Aadhaar)</span><span class=\"tag\">Bank Passbook</span>";
    }

    const urlLink = document.getElementById("modal-scheme-url");
    if (scheme.official_url) {
        urlLink.href = scheme.official_url;
        urlLink.style.display = "inline-flex";
    } else {
        urlLink.style.display = "none";
    }

    document.getElementById("scheme-details-modal").style.display = "flex";
}

function closeSchemeDetailsModal() {
    document.getElementById("scheme-details-modal").style.display = "none";
}

function startWorkflowWithSchemeFromModal() {
    closeSchemeDetailsModal();
    if (!state.isAuthenticated) {
        openAuthModal("demo");
        return;
    }
    if (state.selectedScheme) {
        selectSchemeForWorkflow(state.selectedScheme.id || state.selectedScheme.scheme_id);
    }
}

// ==============================================================
// 5-AGENT WORKFLOW IMPLEMENTATION
// ==============================================================

function fillAssistantPrompt(text) {
    const input = document.getElementById("assistant-need-input");
    if (input) {
        input.value = text;
        input.focus();
    }
}

function goToWorkflowStage(stageNum) {
    state.workflowStage = stageNum;

    // Update Stepper
    document.querySelectorAll(".step-item").forEach(item => {
        const step = parseInt(item.getAttribute("data-step"));
        item.classList.remove("active", "completed");
        if (step === stageNum) {
            item.classList.add("active");
        } else if (step < stageNum) {
            item.classList.add("completed");
        }
    });

    // Update Stage Tag
    const tagEl = document.getElementById("workflow-current-agent-tag");
    const agentNames = [
        "Agent 1: Need Intake Active",
        "Agent 1: Scheme Discovery Results",
        "Agent 2: Statutory Eligibility Audit",
        "Agent 3: Document Readiness Scrutiny",
        "Agent 4: Application Drafter & Consent",
        "Agent 5: Tracker & Registry Record"
    ];
    if (tagEl) tagEl.textContent = agentNames[stageNum - 1] || "Agent Active";

    // Show active stage content
    document.querySelectorAll(".workflow-stage-content").forEach(content => {
        content.classList.toggle("active", content.id === `workflow-stage-${stageNum}`);
    });
}

// Stage 1 -> 2: Need Intake & Discovery
async function executeSchemeDiscovery() {
    const input = document.getElementById("assistant-need-input");
    const query = input?.value.trim();
    if (!query || query.length < 5) {
        showToast("Please describe your need or situation in a few words.", "error");
        input?.focus();
        return;
    }

    goToWorkflowStage(2);

    const eventTitle = document.getElementById("discovery-event-title");
    const eventSub = document.getElementById("discovery-event-sub");
    if (eventTitle) eventTitle.textContent = "Understanding your need & extracting criteria...";
    if (eventSub) eventSub.textContent = "Extracting trade, income range, category, and state applicability.";

    try {
        const res = await fetch("/api/workflow/intake-and-match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: state.activeUserId,
                user_query: query
            })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Scheme discovery pipeline failed");

        state.intakeAnalysis = data.intake_analysis;
        state.recommendations = data.recommendations || [];
        state.currentMatches = data.results || data.recommendations || [];

        // Render Extracted Criteria Summary
        renderExtractedCriteriaCard(data.intake_analysis);

        // Render 6-7 Matched Schemes
        renderMatchedSchemes(state.currentMatches);

        if (eventTitle) eventTitle.textContent = "Scheme Discovery Completed";
        if (eventSub) eventSub.textContent = `Retrieved and evaluated ${state.currentMatches.length} schemes from Qdrant vector index.`;

    } catch (err) {
        console.error("Discovery error:", err);
        showToast("Error retrieving schemes. Falling back to local catalog.", "error");
        // Fallback to top 6 catalog schemes
        renderMatchedSchemes(state.allSchemes.slice(0, 6));
    }
}

function renderExtractedCriteriaCard(analysis) {
    const container = document.getElementById("extracted-criteria-container");
    if (!container || !analysis) return;

    const chips = [
        { label: "Identified Need", val: analysis.extracted_need || "Financial Support" },
        { label: "Sector / Trade", val: analysis.identified_category || "General Welfare" },
        { label: "Beneficiary Category", val: state.currentUser?.social_category || "General" },
        { label: "State Focus", val: state.currentUser?.state || "All India" }
    ];

    container.innerHTML = `
        <div class="extracted-criteria-header">
            <i class="fa-solid fa-microchip"></i>
            <span>Agent 1 Criteria Extraction Result</span>
        </div>
        <div class="criteria-chips-row">
            ${chips.map(c => `
                <div class="criteria-chip">
                    <span>${c.label}:</span> <strong>${escapeHtml(c.val)}</strong>
                </div>
            `).join("")}
        </div>
    `;
}

function renderMatchedSchemes(matches) {
    const container = document.getElementById("matched-schemes-container");
    const countEl = document.getElementById("results-count");
    if (!container) return;

    if (countEl) countEl.textContent = matches.length;

    if (matches.length === 0) {
        container.innerHTML = `
            <div class="empty-state-box" style="grid-column: 1 / -1;">
                <h4>No matching schemes found</h4>
                <p>Try refining your request or search with another citizen need.</p>
                <button class="btn btn-secondary btn-sm" onclick="goToWorkflowStage(1)">Change Description</button>
            </div>
        `;
        return;
    }

    container.innerHTML = matches.map(s => createSchemeCardHtml(s, s.is_recommended)).join("");
}

// Stage 2 -> 3: Select Scheme & Run Eligibility Audit
async function selectSchemeForWorkflow(schemeId) {
    const sId = Number(schemeId) || (state.selectedScheme ? Number(state.selectedScheme.id || state.selectedScheme.scheme_id) : 1);
    const scheme = state.allSchemes.find(s => s.id === sId || s.scheme_id === sId) || 
                   state.currentMatches.find(s => s.id === sId || s.scheme_id === sId) ||
                   state.allSchemes[0] ||
                   state.currentMatches[0];
    if (!scheme) return;

    scheme.id = scheme.id || scheme.scheme_id || sId;
    scheme.scheme_id = scheme.scheme_id || scheme.id || sId;
    state.selectedScheme = scheme;

    // Transition to Assistant tab if called from catalog
    if (state.activePage !== "assistant") {
        navigateToPage("assistant");
    }

    goToWorkflowStage(3);

    const titleEl = document.getElementById("eligibility-scheme-name");
    if (titleEl) titleEl.textContent = `Auditing Eligibility: ${scheme.name}`;

    try {
        const res = await fetch("/api/workflow/audit-eligibility", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: Number(state.activeUserId) || 1,
                scheme_id: Number(scheme.id || scheme.scheme_id) || 1
            })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Eligibility audit failed");

        state.eligibilityAssessment = data.eligibility;
        renderEligibilityAudit(data.eligibility);

    } catch (err) {
        console.error("Eligibility audit error:", err);
        showToast("Error auditing eligibility. Displaying statutory checks.", "error");
    }
}

function renderEligibilityAudit(assessment) {
    const banner = document.getElementById("eligibility-verdict-banner");
    const rulesContainer = document.getElementById("statutory-rules-container");
    const declContainer = document.getElementById("declarations-checklist-container");
    if (!banner || !rulesContainer) return;

    const verdict = (assessment?.verdict || assessment?.overall_verdict || "CONDITIONALLY_ELIGIBLE").toUpperCase();
    const isEligible = verdict === "ELIGIBLE";
    banner.className = `verdict-banner ${isEligible ? 'eligible' : 'conditional'}`;
    banner.innerHTML = `
        <i class="fa-solid ${isEligible ? 'fa-circle-check' : 'fa-triangle-exclamation'}"></i>
        <div class="verdict-info">
            <h4>${isEligible ? 'Statutory Eligibility Met' : (verdict === 'INELIGIBLE' ? 'Eligibility Warning — Criteria Mismatch' : 'Conditional Eligibility — Confirmations Needed')}</h4>
            <p>${escapeHtml(assessment?.summary || 'The citizen profile aligns with statutory guidelines.')}</p>
        </div>
    `;

    // Render Rules Evaluation
    const rawRules = assessment?.rules_audit || assessment?.evaluated_criteria || assessment?.checklist || [];
    const rules = rawRules.length > 0 ? rawRules : [
        { rule_text: "Applicant Age statutory range", citizen_fact: `${state.currentUser?.age || 35} Years`, status: "PASSED" },
        { rule_text: "Occupation trade category", citizen_fact: state.currentUser?.occupation || "Citizen", status: "PASSED" },
        { rule_text: "Annual income ceiling", citizen_fact: `₹${(state.currentUser?.annual_income || 100000).toLocaleString('en-IN')}`, status: "PASSED" },
        { rule_text: "Agricultural Landholding check", citizen_fact: `${state.currentUser?.land_ownership_hectares || 0} ha`, status: "PASSED" }
    ];

    rulesContainer.innerHTML = rules.map(r => {
        const ruleTitle = r.rule_text || r.rule || r.criterion || "Statutory Criterion";
        const ruleFact = r.citizen_fact || r.profile_val || r.explanation || r.reason || "Verified against citizen profile";
        const status = (r.status || "PASSED").toUpperCase();
        const badgeClass = status === "PASSED" ? "passed" : (status === "FAILED" ? "failed" : "self_declaration");

        let uploadActionBtn = "";
        const lower = ruleTitle.toLowerCase();
        let targetCategory = "other";
        let targetName = "Supporting Document";
        if (lower.includes("income") || lower.includes("economic") || lower.includes("ceiling") || lower.includes("tax")) {
            targetCategory = "income_certificate";
            targetName = "Income Certificate Proof";
        } else if (lower.includes("land") || lower.includes("hectare") || lower.includes("khasra") || lower.includes("acre")) {
            targetCategory = "land_record";
            targetName = "Land Record / Khatauni";
        } else if (lower.includes("caste") || lower.includes("social") || lower.includes("category")) {
            targetCategory = "caste_certificate";
            targetName = "Caste Certificate";
        } else if (lower.includes("vending") || lower.includes("trade") || lower.includes("occupation") || lower.includes("farmer")) {
            targetCategory = "vending_certificate";
            targetName = "Trade / Vending Certificate";
        } else if (lower.includes("age") || lower.includes("identity") || lower.includes("citizen")) {
            targetCategory = "aadhaar";
            targetName = "Identity Proof (Aadhaar/Voter)";
        }

        if (status !== "PASSED") {
            uploadActionBtn = `
                <button type="button" class="btn btn-outline btn-xs" style="margin-top: 6px; font-size: 11px; padding: 3px 8px; border-radius: 4px; display: inline-flex; align-items: center; gap: 4px;" onclick="openUploadDocModal('${targetCategory}', '${escapeHtml(targetName)}')">
                    <i class="fa-solid fa-cloud-arrow-up"></i>
                    <span>Upload Proof</span>
                </button>
            `;
        }

        return `
            <div class="rule-audit-row">
                <div class="rule-desc" style="flex: 1;">
                    <strong>${escapeHtml(ruleTitle)}</strong>
                    <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Citizen Context: ${escapeHtml(ruleFact)}</div>
                    ${uploadActionBtn}
                </div>
                <span class="rule-status-badge ${badgeClass}">${escapeHtml(status)}</span>
            </div>
        `;
    }).join("");

    // Render Self Declarations
    const rawDeclarations = assessment?.actionable_declarations || assessment?.required_confirmations || [];
    const declarations = rawDeclarations.length > 0 ? rawDeclarations : [
        "I declare that I am not an income tax payee for the current assessment year.",
        "I affirm that neither I nor any family member holds an institutional government post.",
        "I confirm that all bank account and landholding details provided are true and accurate."
    ];

    if (declContainer) {
        declContainer.innerHTML = declarations.map((d, idx) => `
            <div class="declaration-item">
                <input type="checkbox" id="decl-check-${idx}" class="decl-checkbox" checked value="${escapeHtml(d)}">
                <label for="decl-check-${idx}">
                    <strong>Affirmation ${idx + 1}:</strong> ${escapeHtml(d)}
                </label>
            </div>
        `).join("");
    }
}

// Stage 3 -> 4: Proceed to Documents Checklist
async function proceedToDocumentChecklist() {
    // Collect self-declarations
    state.confirmedRules = [];
    document.querySelectorAll(".decl-checkbox:checked").forEach(cb => {
        state.confirmedRules.push(cb.value);
    });

    goToWorkflowStage(4);

    const sid = Number(state.selectedScheme?.id || state.selectedScheme?.scheme_id) || 1;

    try {
        const res = await fetch("/api/workflow/audit-documents", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: Number(state.activeUserId) || 1,
                scheme_id: sid
            })
        });

        const data = await res.json();
        if (res.ok) {
            state.documentReadiness = data.document_readiness;
            renderDocumentChecklist(data.document_readiness);
        }
    } catch (err) {
        console.error("Document audit failed:", err);
    }
}

function renderDocumentChecklist(readiness) {
    const meter = document.getElementById("docs-readiness-meter");
    const container = document.getElementById("docs-checklist-container");
    if (!meter || !container) return;

    const score = readiness?.readiness_percentage !== undefined ? readiness.readiness_percentage : (readiness?.readiness_score || 80);
    const readyCount = readiness?.ready_count !== undefined ? readiness.ready_count : (readiness?.ready_documents?.length || 2);
    const totalRequired = readiness?.total_required !== undefined ? readiness.total_required : ((readiness?.checklist?.length) || 3);
    const missingCount = Math.max(0, totalRequired - readyCount);

    meter.innerHTML = `
        <div class="meter-stat">
            <h4>Document Readiness: ${readiness?.overall_status === 'READY_TO_APPLY' || readiness?.is_ready_to_apply || score >= 50 ? 'Application Ready' : 'Few Proofs Required'}</h4>
            <p>${readyCount} of ${totalRequired} verified documents in demo locker • ${missingCount > 0 ? `${missingCount} proofs can be generated below` : 'All mandatory proofs satisfied'}</p>
        </div>
        <div class="meter-score">${score}% Ready</div>
    `;

    let allDocs = [];
    if (readiness?.checklist && readiness.checklist.length > 0) {
        allDocs = readiness.checklist.map(d => ({
            name: d.document_name,
            verified: (d.status || '').toUpperCase() === 'READY',
            status: d.status,
            badge: d.badge || (d.status === 'READY' ? 'Verified Demo Document' : 'Action Required'),
            notes: d.notes || ''
        }));
    } else {
        const readyDocs = (readiness?.ready_documents || [
            { document_name: "Aadhaar Card (Identity Proof)", status: "AVAILABLE", verified: true },
            { document_name: "Bank Passbook / Statement", status: "AVAILABLE", verified: true }
        ]).map(d => ({ name: d.document_name || d.name, verified: true, notes: "Verified via demo locker" }));
        
        const missingDocs = (readiness?.missing_documents || [
            { document_name: "Land Record / Trade Certificate", status: "MISSING", verified: false }
        ]).map(d => ({ name: d.document_name || d.name, verified: false, notes: "Generate sample proof below" }));
        
        allDocs = [...readyDocs, ...missingDocs];
    }

    container.innerHTML = allDocs.map(d => {
        const isMissing = !d.verified;
        const statusChip = d.verified
            ? `<span class="status-chip success">Ready</span>`
            : `<span class="status-chip danger">Missing</span>`;

        const reqName = d.name || "";
        const lowerReq = reqName.toLowerCase();
        let suggestedCategory = "other";
        if (lowerReq.includes("form") || lowerReq.includes("kcc") || lowerReq.includes("application")) {
            suggestedCategory = "application_form";
        } else if (lowerReq.includes("photo") || lowerReq.includes("passport")) {
            suggestedCategory = "photo";
        } else if (lowerReq.includes("land") || lowerReq.includes("lease") || lowerReq.includes("deed") || lowerReq.includes("revenue") || lowerReq.includes("khasra")) {
            suggestedCategory = "land_record";
        } else if (lowerReq.includes("bank") || lowerReq.includes("passbook") || lowerReq.includes("statement") || lowerReq.includes("account")) {
            suggestedCategory = "bank_passbook";
        } else if (lowerReq.includes("income") || lowerReq.includes("salary") || lowerReq.includes("tax")) {
            suggestedCategory = "income_certificate";
        } else if (lowerReq.includes("caste") || lowerReq.includes("category")) {
            suggestedCategory = "caste_certificate";
        } else if (lowerReq.includes("aadhaar") || lowerReq.includes("voter") || lowerReq.includes("identity")) {
            suggestedCategory = "aadhaar";
        }

        const safeReqName = escapeHtml(reqName).replace(/'/g, "\\'");
        const uploadBtn = isMissing
            ? `<button class="btn btn-primary btn-sm" style="margin-top:6px;" onclick="openUploadDocModal('${suggestedCategory}', '${safeReqName}', '${safeReqName}')">
                   <i class="fa-solid fa-upload"></i> Upload Document
               </button>`
            : '';

        return `
        <div class="doc-check-item">
            <div style="flex:1;">
                <strong>${escapeHtml(d.name)}</strong>
                <div style="font-size: 12px; color: var(--text-muted); margin-top:3px;">
                    ${escapeHtml(d.notes || (d.verified ? 'Verified via Document Locker' : 'Upload a document or generate a demo proof below'))}
                </div>
                ${uploadBtn}
            </div>
            ${statusChip}
        </div>`;
    }).join("");
}

async function quickGenerateDoc(docType) {
    try {
        const res = await fetch(`/api/documents/generate-demo/${state.activeUserId}?doc_type=${docType}`, {
            method: "POST"
        });
        const data = await res.json();
        if (res.ok) {
            showToast(`Generated demo ${docType.replace('_', ' ')}!`, "success");
            await loadUserDocuments();
            await proceedToDocumentChecklist();
        }
    } catch (err) {
        console.error("Failed to generate demo doc:", err);
    }
}

async function generateAllDemoDocs() {
    const types = ["aadhaar", "bank_passbook", "land_record", "vending_certificate", "income_certificate"];
    for (const t of types) {
        await quickGenerateDoc(t);
    }
    showToast("Complete set of demo documents verified in locker!", "success");
}

// Stage 4 -> 5: Application Draft & Consent
async function proceedToApplicationDraft() {
    goToWorkflowStage(5);

    const sid = Number(state.selectedScheme?.id || state.selectedScheme?.scheme_id) || 1;

    try {
        const res = await fetch("/api/workflow/generate-draft", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: Number(state.activeUserId) || 1,
                scheme_id: sid,
                user_query: state.intakeAnalysis?.extracted_need || "Welfare support",
                confirmed_criteria: state.confirmedRules
            })
        });

        const data = await res.json();
        if (res.ok) {
            state.applicationDraft = data.application_draft;
            renderApplicationDraft(data.application_draft);
        }
    } catch (err) {
        console.error("Draft generation failed:", err);
        renderFallbackApplicationDraft();
    }
}

function renderApplicationDraft(draft) {
    const container = document.getElementById("draft-form-box");
    if (!container) return;

    const u = state.currentUser || {};
    const s = state.selectedScheme || {};
    const appData = draft?.applicant_summary || draft?.applicant_details || {};
    const draftTitle = draft?.application_title || `Official Application for ${s.name || 'Welfare Scheme'}`;
    const authority = draft?.target_authority || s.ministry || "Government Department";

    container.innerHTML = `
        <div style="margin-bottom: 14px; padding: 12px 16px; background: var(--color-blue-soft); border-radius: var(--radius-md); border-left: 4px solid var(--color-blue);">
            <strong style="color: var(--color-navy); font-size: 15px;"><i class="fa-solid fa-file-signature"></i> ${escapeHtml(draftTitle)}</strong>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">Designated Authority: ${escapeHtml(authority)}</div>
        </div>
        <div class="draft-form-grid">
            <div class="form-group">
                <label>Citizen Full Name:</label>
                <input type="text" id="draft-name" value="${escapeHtml(appData.name || u.full_name || '')}" required>
            </div>
            <div class="form-group">
                <label>Masked Aadhaar Number (Demo):</label>
                <input type="text" id="draft-aadhaar" value="XXXX-XXXX-9012" readonly>
            </div>
            <div class="form-group">
                <label>Occupation / Trade:</label>
                <input type="text" id="draft-occupation" value="${escapeHtml(appData.occupation || u.occupation || '')}" required>
            </div>
            <div class="form-group">
                <label>Annual Household Income (₹):</label>
                <input type="number" id="draft-income" value="${appData.annual_income || u.annual_income || 120000}" required>
            </div>
            <div class="form-group">
                <label>Target Scheme Code:</label>
                <input type="text" id="draft-schemecode" value="${escapeHtml(s.code || 'GOV-SCHEME')}" readonly>
            </div>
            <div class="form-group">
                <label>Target State / Jurisdiction:</label>
                <input type="text" id="draft-jurisdiction" value="${escapeHtml(s.state || u.state || 'Rajasthan')}" readonly>
            </div>
            <div class="form-group draft-full-width">
                <label>Synthesized Statement of Need (Editable):</label>
                <textarea id="draft-statement" rows="3">${escapeHtml(draft?.statement_of_purpose || draft?.statement_of_need || `Application for financial assistance under ${s.name}. The applicant meets statutory eligibility criteria.`)}</textarea>
            </div>
        </div>
    `;

    // Reset consent checkbox
    const chk = document.getElementById("chk-workflow-consent");
    const submitBtn = document.getElementById("btn-submit-workflow-app");
    if (chk) chk.checked = false;
    if (submitBtn) submitBtn.disabled = true;
}

function renderFallbackApplicationDraft() {
    renderApplicationDraft({
        applicant_details: {
            name: state.currentUser?.full_name,
            occupation: state.currentUser?.occupation,
            annual_income: state.currentUser?.annual_income
        },
        statement_of_purpose: `Formal application for ${state.selectedScheme?.name}.`
    });
}

function handleConsentToggle(checkbox) {
    const submitBtn = document.getElementById("btn-submit-workflow-app");
    if (submitBtn) {
        submitBtn.disabled = !checkbox.checked;
    }
}

// Stage 5 -> 6: Submit Simulated Application (Tracker Agent)
async function executeSimulatedSubmission() {
    const chk = document.getElementById("chk-workflow-consent");
    if (!chk || !chk.checked) {
        showToast("Explicit citizen approval is mandatory before submission.", "error");
        return;
    }

    const applicantData = {
        name: document.getElementById("draft-name")?.value || state.currentUser?.full_name,
        occupation: document.getElementById("draft-occupation")?.value || state.currentUser?.occupation,
        annual_income: parseFloat(document.getElementById("draft-income")?.value) || state.currentUser?.annual_income,
        statement: document.getElementById("draft-statement")?.value || ""
    };

    const sid = Number(state.selectedScheme?.id || state.selectedScheme?.scheme_id) || 1;

    try {
        const res = await fetch("/api/workflow/submit-simulated", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: Number(state.activeUserId) || 1,
                scheme_id: sid,
                explicit_approval: true,
                applicant_data: applicantData,
                eligibility_answers: state.confirmedRules,
                draft_summary: `Application package for ${state.selectedScheme?.name || 'Welfare Scheme'}`
            })
        });

        const data = await res.json();
        if (res.ok) {
            state.submittedApplication = data;
            goToWorkflowStage(6);
            renderTrackingResults(data);
            showToast("Simulated application registered in tracking registry!", "success");
            // Refresh applications list & metrics
            await loadUserApplications();
            updateDashboardMetrics();
        } else {
            showToast(data.detail || "Submission simulation failed.", "error");
        }
    } catch (err) {
        console.error("Submission error:", err);
        showToast("Error processing simulated submission.", "error");
    }
}

function renderTrackingResults(data) {
    const refBox = document.getElementById("workflow-ref-box");
    const timelineBox = document.getElementById("workflow-timeline-box");
    if (!refBox || !timelineBox) return;

    const ref = data.reference_no || data.application_ref || (data.application && (data.application.reference_no || data.application.application_ref)) || `JS-2025-${Math.floor(10000 + Math.random() * 90000)}`;

    refBox.innerHTML = `
        <div class="ref-label">Simulated Application Reference ID</div>
        <div class="ref-number">${escapeHtml(ref)}</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">Persisted in SQLite Demo Registry</div>
    `;

    const rawMilestones = (data.application && data.application.tracking_history) || data.milestones || data.tracking_history || [
        { title: "Application Package Prepared & Signed", desc: "Citizen consent recorded with verified mock documents.", status: "COMPLETED" },
        { title: "Block Officer Preliminary Scrutiny", desc: "Automated rule verification against state database.", status: "PENDING" },
        { title: "Field Verification & Inspection", desc: "Scheduled for Gram Sevak / Ward Scrutiny.", status: "SCHEDULED" },
        { title: "Statutory Sanction & Order Issuance", desc: "Pending department review.", status: "UPCOMING" },
        { title: "Direct Benefit Transfer (DBT) Disbursement", desc: "Aadhaar-seeded bank account credit.", status: "UPCOMING" }
    ];

    timelineBox.innerHTML = rawMilestones.map((m, idx) => `
        <div class="timeline-step-row">
            <div class="timeline-step-icon ${m.status === 'COMPLETED' ? '' : 'pending'}">
                <i class="fa-solid ${m.status === 'COMPLETED' ? 'fa-check' : 'fa-clock'}"></i>
            </div>
            <div class="timeline-step-details">
                <strong>${escapeHtml(m.title || m.step || 'Scrutiny Milestone')}</strong>
                <span>${escapeHtml(m.desc || m.details || m.notes || 'In progress')}</span>
            </div>
        </div>
    `).join("");
}

function resetWorkflowToStart() {
    state.selectedScheme = null;
    state.workflowStage = 1;
    goToWorkflowStage(1);
    const input = document.getElementById("assistant-need-input");
    if (input) input.value = "";
}

// ==============================================================
// Persistent Data: Applications, Documents, Notifications
// ==============================================================

async function loadUserApplications() {
    try {
        const res = await fetch(`/api/applications/user/${state.activeUserId}`);
        const data = await res.json();
        state.allApplications = data.applications || [];
    } catch (err) {
        console.error("Failed to load applications:", err);
    }
}

function renderApplicationsPage() {
    const container = document.getElementById("applications-full-list");
    if (!container) return;

    if (state.allApplications.length === 0) {
        container.innerHTML = `
            <div class="empty-state-box">
                <div class="empty-state-icon"><i class="fa-regular fa-folder-open"></i></div>
                <h4>No Welfare Applications Submitted</h4>
                <p>You have not registered any demo applications. Run the AI Assistant to discover schemes and create your first draft.</p>
                <button class="btn btn-primary btn-sm" onclick="navigateToPage('assistant')">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Discover Schemes
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = state.allApplications.map(app => `
        <div class="app-record-card">
            <div class="app-record-info">
                <h4>${escapeHtml(app.scheme_name || 'Welfare Scheme')}</h4>
                <span class="app-ref-tag">${escapeHtml(app.reference_no || app.application_ref || 'JS-2025')}</span>
                <div class="app-record-meta">Applied on: ${new Date(app.submitted_at || app.created_at || Date.now()).toLocaleDateString()} • Jurisdiction: ${escapeHtml(app.jurisdiction || 'Rajasthan')}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span class="status-chip success">${escapeHtml(app.status || 'SUBMITTED')}</span>
                <button class="btn btn-outline btn-sm" onclick="showAppTrackingModal('${escapeHtml(app.reference_no || app.application_ref)}')">
                    <i class="fa-solid fa-timeline"></i> View Milestones
                </button>
            </div>
        </div>
    `).join("");
}

function showAppTrackingModal(refNumber) {
    showToast(`Tracking status for ${refNumber}: Preliminary Scrutiny In Progress`, "success");
}


async function loadUserDocuments() {
    try {
        const res = await fetch(`/api/documents/user/${state.activeUserId}`);
        const data = await res.json();
        state.allDocuments = data.documents || [];
    } catch (err) {
        console.error("Failed to load documents:", err);
    }
}

// ==============================================================
// Document Card Helpers
// ==============================================================

function getDocIcon(docType) {
    const icons = {
        aadhaar: "fa-id-card",
        bank_passbook: "fa-money-check",
        vending_certificate: "fa-stamp",
        land_record: "fa-mountain-sun",
        income_certificate: "fa-receipt",
        caste_certificate: "fa-users",
        ration_card: "fa-book",
        college_id: "fa-graduation-cap",
        other: "fa-file"
    };
    return icons[docType?.toLowerCase()] || "fa-file-shield";
}

function getDocStatusBadge(status) {
    const map = {
        VERIFIED_DEMO: { cls: "success", label: "Verified (Demo)" },
        PENDING_REVIEW: { cls: "warning", label: "Pending Review" },
        VERIFIED:       { cls: "success", label: "Verified" },
        REJECTED:       { cls: "danger",  label: "Rejected" }
    };
    return map[status] || { cls: "unknown", label: status || "Unknown" };
}

function formatDocDate(dateStr) {
    if (!dateStr) return "—";
    try {
        return new Date(dateStr).toLocaleDateString("en-IN", {
            day: "2-digit", month: "short", year: "numeric"
        });
    } catch { return dateStr; }
}

function renderDocumentsPage() {
    const container = document.getElementById("user-docs-container");
    if (!container) return;

    if (state.allDocuments.length === 0) {
        container.innerHTML = `
            <div class="empty-state-box" style="grid-column: 1 / -1;">
                <div class="empty-state-icon"><i class="fa-solid fa-folder-open"></i></div>
                <h4>No Documents in Locker</h4>
                <p>Upload a document or generate pre-verified mock documents to pass readiness checks.</p>
                <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-top:12px;">
                    <button class="btn btn-primary btn-sm" onclick="openUploadDocModal()">
                        <i class="fa-solid fa-upload"></i> Upload Document
                    </button>
                    <button class="btn btn-outline btn-sm" onclick="generateAllDemoDocs()">
                        <i class="fa-solid fa-magic"></i> Auto-Generate Demo Set
                    </button>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = state.allDocuments.map(doc => {
        const docType = doc.doc_type || doc.document_type || "other";
        const docName = doc.doc_name || doc.document_name || docType.replace(/_/g, " ").toUpperCase();
        const status  = doc.status || "VERIFIED_DEMO";
        const badge   = getDocStatusBadge(status);
        const icon    = getDocIcon(docType);
        const dateStr = formatDocDate(doc.created_at);
        const hasFile = doc.file_path && doc.file_path.trim().length > 0;
        const catLabel = docType.replace(/_/g, " ").replace(/\w/g, l => l.toUpperCase());

        return `
        <div class="user-doc-card" id="doc-card-${doc.id}">
            <div class="doc-type-icon">
                <i class="fa-solid ${escapeHtml(icon)}"></i>
            </div>
            <div class="doc-card-info">
                <strong class="doc-card-name">${escapeHtml(docName)}</strong>
                <span class="doc-card-meta">
                    <i class="fa-solid fa-tag" style="font-size:10px;"></i> ${escapeHtml(catLabel)}
                    &nbsp;•&nbsp;
                    <i class="fa-regular fa-calendar" style="font-size:10px;"></i> ${escapeHtml(dateStr)}
                </span>
            </div>
            <div class="doc-card-actions">
                <span class="status-chip ${badge.cls}" style="margin-bottom:6px;">${badge.label}</span>
                <div class="doc-action-btns">
                    <button class="btn btn-outline btn-sm doc-action-btn" title="View Document / Credential" onclick="viewDocument(${doc.id})">
                        <i class="fa-solid fa-eye"></i> View
                    </button>
                    <button class="btn btn-danger-outline btn-sm doc-action-btn" title="Delete document" onclick="promptDeleteDocument(${doc.id}, '${escapeHtml(docName).replace(/'/g,"\'")}')">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>`;
    }).join("");
}

// ==============================================================
// Upload Document Modal
// ==============================================================

let _pendingDeleteDocId = null;
let _pendingDeleteDocName = "";
let _currentUploadTargetRequirement = "";

function openUploadDocModal(prefillCategory = "", prefillDisplayName = "", targetRequirement = "") {
    const modal = document.getElementById("upload-doc-modal");
    if (!modal) return;

    _currentUploadTargetRequirement = targetRequirement || prefillDisplayName || "";

    // Reset form
    document.getElementById("upload-doc-form").reset();
    document.getElementById("upload-modal-error").style.display = "none";
    document.getElementById("upload-modal-error").textContent = "";
    document.getElementById("upload-file-label").textContent = "Click to browse or drag & drop";
    document.getElementById("upload-file-drop-zone").classList.remove("file-selected");
    document.getElementById("btn-upload-submit").disabled = false;
    document.getElementById("upload-btn-text").textContent = "Upload Document";

    // Show or hide target requirement banner
    const banner = document.getElementById("upload-target-requirement-banner");
    const bannerText = document.getElementById("upload-target-req-text");
    if (banner && bannerText) {
        if (_currentUploadTargetRequirement) {
            bannerText.textContent = _currentUploadTargetRequirement;
            banner.style.display = "block";
        } else {
            banner.style.display = "none";
        }
    }

    if (prefillCategory) {
        const sel = document.getElementById("upload-modal-category");
        if (sel) sel.value = prefillCategory;
    }

    if (prefillDisplayName) {
        const nameInput = document.getElementById("upload-modal-display-name");
        if (nameInput) nameInput.value = prefillDisplayName;
    }

    modal.style.display = "flex";
    setTimeout(() => {
        const focusTarget = prefillDisplayName ? document.getElementById("upload-file-drop-zone") : document.getElementById("upload-modal-display-name");
        focusTarget?.focus();
    }, 100);
}

function closeUploadDocModal() {
    const modal = document.getElementById("upload-doc-modal");
    if (modal) modal.style.display = "none";
}

function handleUploadModalBackdrop(e) {
    if (e.target === document.getElementById("upload-doc-modal")) {
        closeUploadDocModal();
    }
}

function handleFileSelection(input) {
    const label = document.getElementById("upload-file-label");
    const dropZone = document.getElementById("upload-file-drop-zone");
    const nameInput = document.getElementById("upload-modal-display-name");
    if (input.files && input.files[0]) {
        const file = input.files[0];
        label.textContent = file.name;
        dropZone.classList.add("file-selected");
        if (nameInput && !nameInput.value.trim()) {
            nameInput.value = _currentUploadTargetRequirement || file.name.replace(/\.[^/.]+$/, "");
        }
    } else {
        label.textContent = "Click to browse or drag & drop";
        dropZone.classList.remove("file-selected");
    }
}

async function handleUploadDocFormSubmit(event) {
    event.preventDefault();
    const errorEl = document.getElementById("upload-modal-error");
    errorEl.style.display = "none";
    errorEl.textContent = "";

    const category = document.getElementById("upload-modal-category").value;
    const displayName = document.getElementById("upload-modal-display-name").value.trim();
    const fileInput = document.getElementById("upload-modal-file");
    const file = fileInput.files[0];

    // Client-side validation
    if (!category) {
        showUploadError("Please select a document category."); return;
    }
    if (!displayName) {
        showUploadError("Please enter a display name for the document."); return;
    }
    if (!file) {
        showUploadError("Please select a file to upload."); return;
    }
    const allowedExts = [".pdf", ".jpg", ".jpeg", ".png"];
    const fileExt = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (!allowedExts.includes(fileExt)) {
        showUploadError(`Unsupported file type: ${fileExt}. Please upload PDF, JPG, JPEG, or PNG.`); return;
    }

    // Start uploading
    const submitBtn = document.getElementById("btn-upload-submit");
    const btnText = document.getElementById("upload-btn-text");
    submitBtn.disabled = true;
    btnText.textContent = "Uploading...";

    try {
        const activeUid = Number(state.activeUserId || state.currentUser?.id) || 1;
        const formData = new FormData();
        formData.append("user_id", activeUid);
        formData.append("doc_type", category);
        formData.append("doc_name", displayName);
        formData.append("target_requirement", _currentUploadTargetRequirement || displayName);
        formData.append("file", file);

        const res = await fetch("/api/documents/upload", {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        if (res.ok && data.success) {
            showToast(`✅ "${displayName}" uploaded & verified successfully!`, "success");
            closeUploadDocModal();
            await loadUserDocuments();
            renderDocumentsPage();

            // If we're on the Stage 3 Eligibility Audit, re-run audit with the new document!
            if (state.workflowStage === 3 && state.selectedScheme) {
                await selectSchemeForWorkflow(state.selectedScheme.id || state.selectedScheme.scheme_id);
                showToast("Eligibility audit updated with uploaded proof!", "success");
            }

            // If we're on workflow stage 4, refresh the document checklist
            if (state.workflowStage === 4 && state.selectedScheme) {
                await proceedToDocumentChecklist();
            }
        } else {
            showUploadError(data.detail || data.message || "Upload failed. Please try again.");
        }
    } catch (err) {
        console.error("Upload error:", err);
        showUploadError("Network error. Please check your connection and try again.");
    } finally {
        submitBtn.disabled = false;
        btnText.textContent = "Upload Document";
    }
}

function showUploadError(msg) {
    const errorEl = document.getElementById("upload-modal-error");
    if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = "block";
    }
}

// ==============================================================
// View Document
// ==============================================================

function viewDocument(docId) {
    const activeUid = Number(state.activeUserId || state.currentUser?.id) || 1;
    const url = `/api/documents/view/${docId}?user_id=${activeUid}`;
    window.open(url, "_blank", "noopener,noreferrer");
}

// ==============================================================
// Delete Document
// ==============================================================

function promptDeleteDocument(docId, docName) {
    _pendingDeleteDocId = docId;
    _pendingDeleteDocName = docName;

    const nameEl = document.getElementById("delete-doc-name-preview");
    if (nameEl) nameEl.textContent = `"${docName}"`;

    const modal = document.getElementById("delete-doc-modal");
    if (modal) modal.style.display = "flex";
}

function closeDeleteDocModal() {
    _pendingDeleteDocId = null;
    _pendingDeleteDocName = "";
    const modal = document.getElementById("delete-doc-modal");
    if (modal) modal.style.display = "none";
}

function handleDeleteModalBackdrop(e) {
    if (e.target === document.getElementById("delete-doc-modal")) {
        closeDeleteDocModal();
    }
}

async function confirmDeleteDocument() {
    if (!_pendingDeleteDocId) return;

    const btn = document.getElementById("btn-confirm-delete");
    if (btn) { btn.disabled = true; btn.textContent = "Deleting..."; }

    try {
        const res = await fetch(`/api/documents/${_pendingDeleteDocId}?user_id=${state.activeUserId}`, {
            method: "DELETE"
        });
        const data = await res.json();

        if (res.ok && data.success) {
            showToast(`🗑️ "${_pendingDeleteDocName}" deleted successfully.`, "info");
            closeDeleteDocModal();
            await loadUserDocuments();
            renderDocumentsPage();

            // Refresh checklist if on stage 4
            if (state.workflowStage === 4 && state.selectedScheme) {
                await proceedToDocumentChecklist();
            }
        } else {
            showToast(data.detail || "Could not delete the document.", "error");
            closeDeleteDocModal();
        }
    } catch (err) {
        console.error("Delete error:", err);
        showToast("Network error while deleting. Please try again.", "error");
        closeDeleteDocModal();
    } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fa-solid fa-trash"></i> Yes, Delete'; }
    }
}

async function handleDocUpload(event) {
    // Legacy: redirect to modal
    event.preventDefault();
    openUploadDocModal();
}


async function loadNotifications() {
    try {
        const res = await fetch(`/api/notifications/user/${state.activeUserId}`);
        const data = await res.json();
        state.notifications = data.notifications || [];
        const countBadge = document.getElementById("topbar-notify-count");
        if (countBadge) countBadge.textContent = state.notifications.length;
    } catch (err) {
        console.error("Failed to load notifications:", err);
    }
}

function renderNotificationsPage() {
    const container = document.getElementById("notifications-full-list");
    if (!container) return;

    if (state.notifications.length === 0) {
        container.innerHTML = `
            <div class="empty-state-box">
                <div class="empty-state-icon"><i class="fa-regular fa-bell"></i></div>
                <h4>No New Notifications</h4>
                <p>Status updates regarding scheme scrutiny and disbursements will appear here.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = state.notifications.map(n => `
        <div class="notification-row">
            <div class="notification-icon-box"><i class="fa-solid fa-bell"></i></div>
            <div>
                <strong style="font-size: 14px; color: var(--text-main);">${escapeHtml(n.title)}</strong>
                <p style="font-size: 13px; color: var(--text-muted); margin: 3px 0;">${escapeHtml(n.message)}</p>
                <span style="font-size: 11px; color: var(--text-light);">${new Date(n.created_at).toLocaleString()}</span>
            </div>
        </div>
    `).join("");
}

function toggleNotificationsModal(show) {
    const modal = document.getElementById("notifications-modal");
    if (!modal) return;
    modal.style.display = show ? "flex" : "none";
    if (show) {
        const container = document.getElementById("modal-notifications-container");
        if (container) {
            if (!state.notifications || state.notifications.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 32px 16px; color: var(--text-muted);">
                        <i class="fa-regular fa-bell-slash" style="font-size: 32px; margin-bottom: 10px; display: block; color: #94a3b8;"></i>
                        <p style="margin: 0; font-size: 14px;">No active alerts or notifications right now.</p>
                    </div>
                `;
            } else {
                container.innerHTML = state.notifications.map(n => {
                    const timeStr = n.created_at ? new Date(n.created_at).toLocaleString("en-IN", {
                        day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"
                    }) : "Recent";
                    return `
                    <div class="notification-modal-item">
                        <div class="notification-modal-icon">
                            <i class="fa-solid fa-bell"></i>
                        </div>
                        <div class="notification-modal-body">
                            <div class="notification-modal-title">${escapeHtml(n.title)}</div>
                            <p class="notification-modal-desc">${escapeHtml(n.message)}</p>
                            <span class="notification-modal-time"><i class="fa-regular fa-clock"></i> ${escapeHtml(timeStr)}</span>
                        </div>
                    </div>`;
                }).join("");
            }
        }
    }
}

// ==============================================================
// Profile Page (Read-Only Default View & Edit Mode Controller)
// ==============================================================

function setProfileEditMode(isEditing) {
    state.isProfileEditing = !!isEditing;
    populateProfileForm(state.isProfileEditing);

    const alertBox = document.getElementById("profile-alert-box");
    if (alertBox) alertBox.style.display = "none";

    // Clear any validation error highlights
    document.querySelectorAll("#form-edit-profile .has-error").forEach(el => el.classList.remove("has-error"));

    if (state.isProfileEditing) {
        const firstField = document.getElementById("prof-name");
        if (firstField) {
            firstField.focus();
            firstField.select();
        }
        showToast("Edit mode enabled. Fields are now editable.", "info");
    }
}

function cancelProfileEdit() {
    // Discard any unsaved changes by resetting fields from state.currentUser
    state.isProfileEditing = false;
    populateProfileForm(false);

    const alertBox = document.getElementById("profile-alert-box");
    if (alertBox) alertBox.style.display = "none";

    document.querySelectorAll("#form-edit-profile .has-error").forEach(el => el.classList.remove("has-error"));
    showToast("Editing cancelled. Unsaved changes discarded.", "info");
}

function populateProfileForm(isEditing = false) {
    if (!state.currentUser) return;
    const u = state.currentUser;

    // 1. Update Hero Persona Summary Card
    const heroAvatar = document.getElementById("prof-hero-avatar");
    if (heroAvatar) heroAvatar.textContent = (u.full_name || "C")[0].toUpperCase();

    const heroName = document.getElementById("prof-hero-name");
    if (heroName) heroName.textContent = u.full_name || "Citizen";

    const heroUser = document.getElementById("prof-hero-username");
    if (heroUser) heroUser.textContent = `@${u.username || 'citizen'}`;

    const heroOcc = document.getElementById("prof-hero-occ");
    if (heroOcc) heroOcc.textContent = u.occupation || "Citizen";

    const heroInc = document.getElementById("prof-hero-inc");
    if (heroInc) heroInc.textContent = `₹${(u.annual_income || 0).toLocaleString('en-IN')}/yr`;

    const heroLoc = document.getElementById("prof-hero-loc");
    if (heroLoc) heroLoc.textContent = `${u.district || 'Jaipur'}, ${u.state || 'Rajasthan'}`;

    const heroCat = document.getElementById("prof-hero-cat");
    if (heroCat) heroCat.textContent = `${u.social_category || 'General'}${u.is_bpl ? ' • BPL' : ''}`;

    // 2. Helper to set form values
    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.value = val !== undefined && val !== null ? val : "";
    };

    // Personal Details
    setVal("prof-name", u.full_name);
    setVal("prof-email", u.email || "");
    setVal("prof-phone", u.phone || "");

    // Demographic Details
    setVal("prof-age", u.age || 35);
    setVal("prof-gender", u.gender || "Male");
    setVal("prof-category", u.social_category || "General");
    setVal("prof-marital", u.marital_status || "Married");
    setVal("prof-pwd", u.is_differently_abled ? "1" : "0");
    setVal("prof-family-count", u.family_members_count || 4);

    // Occupational Details
    setVal("prof-occupation", u.occupation || "");
    setVal("prof-land", u.land_ownership_hectares !== undefined ? u.land_ownership_hectares : 0.0);

    // Financial Details
    setVal("prof-income", u.annual_income !== undefined ? u.annual_income : 120000);
    const bplEl = document.getElementById("prof-bpl");
    if (bplEl) bplEl.checked = !!u.is_bpl;

    // Residential Details
    setVal("prof-residence", u.residence_area || "Urban");
    setVal("prof-state", u.state || "Rajasthan");
    setVal("prof-district", u.district || "Jaipur");

    // 3. Toggle Disabled state on all form controls
    const fieldIds = [
        "prof-name", "prof-email", "prof-phone",
        "prof-age", "prof-gender", "prof-category", "prof-marital", "prof-pwd", "prof-family-count",
        "prof-occupation", "prof-land",
        "prof-income", "prof-bpl",
        "prof-residence", "prof-state", "prof-district"
    ];

    fieldIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.disabled = !isEditing;
        }
    });

    // 4. Update Form CSS Class
    const formEl = document.getElementById("form-edit-profile");
    if (formEl) {
        if (isEditing) {
            formEl.classList.remove("is-readonly");
            formEl.classList.add("is-editing");
        } else {
            formEl.classList.remove("is-editing");
            formEl.classList.add("is-readonly");
        }
    }

    // 5. Toggle Header & Bottom Action Controls
    const badgeReadonly = document.getElementById("profile-badge-readonly");
    const badgeEditing = document.getElementById("profile-badge-editing");
    const btnEdit = document.getElementById("btn-edit-profile");
    const editActions = document.getElementById("profile-edit-actions");

    const btnBottomEdit = document.getElementById("btn-bottom-edit");
    const bottomEditGroup = document.getElementById("profile-bottom-edit-group");
    const modeNotice = document.getElementById("profile-mode-notice");

    if (badgeReadonly) badgeReadonly.style.display = isEditing ? "none" : "inline-flex";
    if (badgeEditing) badgeEditing.style.display = isEditing ? "inline-flex" : "none";
    if (btnEdit) btnEdit.style.display = isEditing ? "none" : "inline-flex";
    if (editActions) editActions.style.display = isEditing ? "inline-flex" : "none";

    if (btnBottomEdit) btnBottomEdit.style.display = isEditing ? "none" : "inline-flex";
    if (bottomEditGroup) bottomEditGroup.style.display = isEditing ? "inline-flex" : "none";

    if (modeNotice) {
        if (isEditing) {
            modeNotice.innerHTML = `<i class="fa-solid fa-pen-to-square"></i> <span>You are in <strong>Edit Mode</strong>. Review your changes carefully and click <strong>Save Changes</strong> or <strong>Cancel</strong>.</span>`;
        } else {
            modeNotice.innerHTML = `<i class="fa-solid fa-circle-info"></i> <span>This profile is in <strong>Read-Only Mode</strong>. Click <strong>Edit Profile</strong> to modify your details.</span>`;
        }
    }
}

function showProfileAlert(message, type = "danger") {
    const alertBox = document.getElementById("profile-alert-box");
    if (!alertBox) return;

    let icon = "fa-circle-exclamation";
    if (type === "success") icon = "fa-circle-check";
    if (type === "info") icon = "fa-circle-info";

    alertBox.className = `profile-alert alert-${type}`;
    alertBox.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <div style="flex: 1;">${escapeHtml(message)}</div>
        <button type="button" class="btn-close-alert" onclick="this.parentElement.style.display='none'" style="background:none; border:none; color:inherit; cursor:pointer; font-size:18px; line-height:1;">&times;</button>
    `;
    alertBox.style.display = "flex";
    alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function validateProfileForm(payload) {
    // Clear old error highlights
    document.querySelectorAll("#form-edit-profile .has-error").forEach(el => el.classList.remove("has-error"));

    // 1. Full name validation
    if (!payload.full_name || payload.full_name.trim().length < 2) {
        return { isValid: false, message: "Full Name is required (minimum 2 characters).", fieldId: "prof-name" };
    }

    // 2. Email validation (if filled)
    if (payload.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email)) {
        return { isValid: false, message: "Please enter a valid email address.", fieldId: "prof-email" };
    }

    // 3. Phone validation (if filled)
    if (payload.phone && !/^[0-9+\-\s]{8,15}$/.test(payload.phone)) {
        return { isValid: false, message: "Please enter a valid phone number (at least 8 digits).", fieldId: "prof-phone" };
    }

    // 4. Age validation
    if (isNaN(payload.age) || payload.age < 1 || payload.age > 120) {
        return { isValid: false, message: "Age must be a valid number between 1 and 120 years.", fieldId: "prof-age" };
    }

    // 5. Occupation validation
    if (!payload.occupation || payload.occupation.trim().length === 0) {
        return { isValid: false, message: "Occupation / Trade is required for welfare scheme evaluation.", fieldId: "prof-occupation" };
    }

    // 6. Annual income validation
    if (isNaN(payload.annual_income) || payload.annual_income < 0) {
        return { isValid: false, message: "Annual income must be a non-negative number.", fieldId: "prof-income" };
    }

    // 7. Agricultural land validation
    if (isNaN(payload.land_ownership_hectares) || payload.land_ownership_hectares < 0) {
        return { isValid: false, message: "Agricultural land ownership must be 0 or greater.", fieldId: "prof-land" };
    }

    // 8. Family members count validation
    if (isNaN(payload.family_members_count) || payload.family_members_count < 1) {
        return { isValid: false, message: "Family members count must be at least 1.", fieldId: "prof-family-count" };
    }

    // 9. State & District validation
    if (!payload.state || payload.state.trim().length === 0) {
        return { isValid: false, message: "State of residence is required.", fieldId: "prof-state" };
    }
    if (!payload.district || payload.district.trim().length === 0) {
        return { isValid: false, message: "District is required.", fieldId: "prof-district" };
    }

    return { isValid: true };
}

async function handleProfileSave(event) {
    event.preventDefault();

    const payload = {
        full_name: document.getElementById("prof-name").value.trim(),
        email: document.getElementById("prof-email").value.trim(),
        phone: document.getElementById("prof-phone").value.trim(),
        age: parseInt(document.getElementById("prof-age").value),
        gender: document.getElementById("prof-gender").value,
        social_category: document.getElementById("prof-category").value,
        marital_status: document.getElementById("prof-marital").value,
        is_differently_abled: document.getElementById("prof-pwd").value === "1",
        family_members_count: parseInt(document.getElementById("prof-family-count").value) || 4,
        occupation: document.getElementById("prof-occupation").value.trim(),
        land_ownership_hectares: parseFloat(document.getElementById("prof-land").value) || 0.0,
        annual_income: parseFloat(document.getElementById("prof-income").value),
        is_bpl: document.getElementById("prof-bpl").checked,
        residence_area: document.getElementById("prof-residence").value,
        state: document.getElementById("prof-state").value.trim(),
        district: document.getElementById("prof-district").value.trim()
    };

    // Client-side Validation before sending
    const validation = validateProfileForm(payload);
    if (!validation.isValid) {
        const errorInput = document.getElementById(validation.fieldId);
        if (errorInput) {
            errorInput.classList.add("has-error");
            errorInput.focus();
        }
        showProfileAlert(validation.message, "danger");
        showToast(validation.message, "error");
        return;
    }

    // Set buttons to saving state
    const saveBtn = document.getElementById("btn-save-profile");
    const bottomSaveBtn = document.getElementById("btn-bottom-save");
    if (saveBtn) saveBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> <span>Saving...</span>`;
    if (bottomSaveBtn) bottomSaveBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Saving...`;

    try {
        const res = await fetch(`/api/users/${state.activeUserId}/profile`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok && data.user) {
            // Update state and persistence
            state.currentUser = data.user;
            localStorage.setItem("jansetu_user", JSON.stringify(data.user));
            localStorage.setItem("sahayak_user", JSON.stringify(data.user));

            // Sync allUsers array
            const userIndex = state.allUsers.findIndex(u => u.id === data.user.id);
            if (userIndex !== -1) {
                state.allUsers[userIndex] = data.user;
            }

            // Invalidate stale eligibility audit in workflow state so re-assessment uses fresh profile
            if (state.workflowStage >= 3) {
                state.eligibilityAssessment = null;
            }

            // Update global UI sections: Topbar, Dashboard, Metrics
            updateTopBarProfile();
            updateDashboardBanner();
            updateDashboardMetrics();

            // Return to read-only view
            setProfileEditMode(false);

            showProfileAlert("Profile updated and saved to database successfully! Your AI Workforce eligibility checks have been updated.", "success");
            showToast("Citizen profile saved successfully!", "success");
        } else {
            const errDetail = data.detail || "Server error while updating profile.";
            showProfileAlert(errDetail, "danger");
            showToast(errDetail, "error");
        }
    } catch (err) {
        console.error("Failed to save profile:", err);
        showProfileAlert("Network or server connection error. Please try again.", "danger");
        showToast("Error updating profile. Check server connection.", "error");
    } finally {
        if (saveBtn) saveBtn.innerHTML = `<i class="fa-solid fa-floppy-disk"></i> <span>Save Changes</span>`;
        if (bottomSaveBtn) bottomSaveBtn.innerHTML = `<i class="fa-solid fa-floppy-disk"></i> Save Changes`;
    }
}


// ==============================================================
// Secondary Chatbot: JanSetu Mitra Drawer
// ==============================================================

function toggleChatbot(show) {
    const drawer = document.getElementById("chatbot-sidebar");
    if (drawer) {
        drawer.classList.toggle("open", show);
    }
}

function sendChatPrompt(text) {
    const input = document.getElementById("chat-input-field");
    if (input) {
        input.value = text;
        handleSendChatMessage(new Event("submit"));
    }
}

async function handleSendChatMessage(event) {
    event.preventDefault();
    const input = document.getElementById("chat-input-field");
    const msg = input?.value.trim();
    if (!msg) return;

    appendChatMessage("user", msg);
    input.value = "";

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: state.chatSessionId,
                user_id: state.activeUserId,
                message: msg,
                language: state.currentLang || "en"
            })
        });

        const data = await res.json();
        const replyText = data.reply || data.response;
        if (res.ok && replyText) {
            appendChatMessage("bot", replyText);
            if (data.suggested_prompts && Array.isArray(data.suggested_prompts)) {
                renderMitraDrawerSuggestions(data.suggested_prompts);
            }
        } else {
            appendChatMessage("bot", t("mitra_error", "I am having trouble connecting right now. Please explore schemes in the Scheme Directory."));
        }

    } catch (err) {
        console.error("Chat error:", err);
        appendChatMessage("bot", "Backend service offline. Please try again later.");
    }
}

function formatChatMarkdown(text) {
    if (!text) return "";
    let safe = text.replace(/\r\n/g, "\n");
    safe = escapeHtml(safe);

    // Convert ### or ## or Scheme: into a sleek scheme badge card
    safe = safe.replace(/^(?:#{1,4}\s*|Scheme:\s*)(.*?)$/gm, (match, title) => {
        const cleanTitle = title.replace(/\*\*/g, "").replace(/\*/g, "").trim();
        return `<div class="chat-scheme-badge"><i class="fa-solid fa-award"></i> <span>${cleanTitle}</span></div>`;
    });

    // Bold tags: **bold** -> <strong>bold</strong>
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Remove any remaining stray markdown asterisks or hashes
    safe = safe.replace(/\*{1,3}/g, "");
    safe = safe.replace(/#{1,6}\s*/g, "");

    // Structured section headers
    safe = safe.replace(/^(Related Welfare Initiatives:|Mandatory Documents Checklist:|Eligibility Requirements:|Key Benefits:|Next Steps:|Checklist Guidance:|Application procedure:)\s*$/gm,
        '<div class="chat-section-header">$1</div>');

    // Bullet points: • or -
    safe = safe.replace(/^[•\-\*]\s*(.*?)$/gm, `
        <div class="chat-bullet-row">
            <span class="chat-bullet-dot">•</span>
            <span class="chat-bullet-text">$1</span>
        </div>
    `);

    // Official portal URLs
    safe = safe.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener" class="chat-portal-link"><i class="fa-solid fa-arrow-up-right-from-square"></i> $1</a>');

    // Spacing & line breaks
    safe = safe.replace(/\n\n+/g, "<div class='chat-spacer'></div>");
    safe = safe.replace(/\n/g, "<br>");

    return safe;
}

function appendChatMessage(sender, text) {
    const container = document.getElementById("chat-messages");
    if (!container) return;

    const div = document.createElement("div");
    div.className = `chat-bubble ${sender}-message`;
    const formattedContent = sender === 'bot' ? formatChatMarkdown(text) : escapeHtml(text).replace(/\n/g, '<br>');
    div.innerHTML = `
        <div class="msg-author">${sender === 'user' ? 'You' : '<i class="fa-solid fa-robot"></i> JanSetu Mitra'}</div>
        <div class="msg-content">${formattedContent}</div>
    `;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// ==============================================================
// Utility Functions
// ==============================================================

function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-check' : (type === 'error' ? 'fa-triangle-exclamation' : 'fa-circle-info')}"></i> <span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 250);
    }, 3800);
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

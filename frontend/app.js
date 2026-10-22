/**
 * Sahayak (सहायक) — Frontend Application Controller
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
    chatSessionId: "sahayak_session_" + Math.random().toString(36).substring(2, 9)
};

// ==============================================================
// DOM Content Loaded Initializer
// ==============================================================

document.addEventListener("DOMContentLoaded", async () => {
    setupEventListeners();
    await checkAuthAndInitialize();
});

async function checkAuthAndInitialize() {
    // Check if session exists in localStorage
    const savedUserJson = localStorage.getItem("sahayak_user");
    
    // Always load public scheme preview & user personas in background
    await loadUsersAndPersonas();
    await loadSchemesCatalog();

    if (savedUserJson) {
        try {
            const user = JSON.parse(savedUserJson);
            state.isAuthenticated = true;
            state.activeUserId = user.id;
            state.currentUser = user;
            showPortalApp();
            await refreshUserData(user.id);
            return;
        } catch (e) {
            console.error("Invalid saved session:", e);
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
            closeUploadModal();
            closeViewDocModal();
            closeDeleteModal();
            toggleNotificationsModal(false);
            toggleChatbot(false);
        }
    });
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

async function handleRegisterSubmit(event) {
    event.preventDefault();
    const payload = {
        full_name: document.getElementById("reg-fullname").value.trim(),
        username: document.getElementById("reg-username").value.trim(),
        email: document.getElementById("reg-email").value.trim(),
        phone: document.getElementById("reg-phone").value.trim(),
        occupation: document.getElementById("reg-occupation").value.trim(),
        annual_income: parseFloat(document.getElementById("reg-income").value) || 120000
    };

    try {
        const res = await fetch("/api/users/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok && data.user) {
            setAuthenticatedUser(data.user);
            closeAuthModal();
            showToast(`Citizen profile created: ${data.user.full_name}!`, "success");
        } else {
            showToast(data.detail || "Registration failed.", "error");
        }
    } catch (err) {
        console.error("Registration failed:", err);
        showToast("Registration failed. Please use demo access.", "error");
    }
}

function setAuthenticatedUser(user) {
    state.isAuthenticated = true;
    state.activeUserId = user.id;
    state.currentUser = user;
    localStorage.setItem("sahayak_user", JSON.stringify(user));
    showPortalApp();
    refreshUserData(user.id);
}

function handleLogout() {
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
                        <span>Official Source Portal</span> <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                ` : ''}
            </div>

            <div class="scheme-card-actions">
                <button class="btn btn-secondary btn-sm" onclick="openSchemeDetailsModal(${scheme.id})">
                    <i class="fa-solid fa-circle-info"></i> Details
                </button>
                <button class="btn btn-primary btn-sm" onclick="${isPublic ? 'openAuthModal(\'demo\')' : `selectSchemeForWorkflow(${scheme.id})`}">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Select & Apply
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
    const scheme = state.allSchemes.find(s => s.id === schemeId);
    if (!scheme) return;

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
        selectSchemeForWorkflow(state.selectedScheme.id);
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
    const scheme = state.allSchemes.find(s => s.id === schemeId) || state.currentMatches.find(s => s.id === schemeId);
    if (!scheme) return;

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
                user_id: state.activeUserId,
                scheme_id: scheme.id
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
        return `
            <div class="rule-audit-row">
                <div class="rule-desc">
                    <strong>${escapeHtml(ruleTitle)}</strong>
                    <div style="font-size: 12px; color: var(--text-muted)">Citizen Context: ${escapeHtml(ruleFact)}</div>
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

    try {
        const res = await fetch("/api/workflow/audit-documents", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: state.activeUserId,
                scheme_id: state.selectedScheme.id
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

    const score = readiness?.readiness_percentage !== undefined ? readiness.readiness_percentage : 0;
    const readyCount = readiness?.ready_count !== undefined ? readiness.ready_count : 0;
    const totalRequired = readiness?.total_required !== undefined ? readiness.total_required : 1;
    const missingCount = readiness?.missing_count !== undefined ? readiness.missing_count : Math.max(0, totalRequired - readyCount);

    meter.innerHTML = `
        <div class="meter-stat">
            <h4>Document Readiness: ${readiness?.overall_status === 'READY_TO_APPLY' || score >= 50 ? 'Application Ready' : 'Few Proofs Required'}</h4>
            <p>${readyCount} of ${totalRequired} required documents available in citizen locker • ${missingCount > 0 ? `<strong style="color: var(--color-rose);">${missingCount} Missing</strong> (upload required files below)` : '<strong style="color: var(--color-emerald);">All mandatory proofs satisfied</strong>'}</p>
        </div>
        <div class="meter-score-wrap">
            <div class="meter-score">${score}% Ready</div>
            <div class="meter-progress-track">
                <div class="meter-progress-fill" style="width: ${Math.min(100, Math.max(0, score))}%;"></div>
            </div>
        </div>
    `;

    const checklist = readiness?.checklist || [];
    if (checklist.length === 0) {
        container.innerHTML = `<div class="empty-state-box" style="padding: 20px;"><p>No specific documents required for this scheme.</p></div>`;
        return;
    }

    container.innerHTML = checklist.map(d => {
        const isMissing = d.is_missing || (d.status || '').toUpperCase() === 'MISSING';
        const isUploaded = (d.status || '').toUpperCase() === 'UPLOADED';
        const isReady = (d.status || '').toUpperCase() === 'READY' || (d.status || '').toUpperCase() === 'VERIFIED';
        const docName = d.document_name || "Statutory Document";
        const docTypeKey = d.doc_type_key || "";
        const docId = d.doc_id;

        let statusChipHtml = '';
        let actionBtnHtml = '';

        if (isMissing) {
            statusChipHtml = `<span class="status-chip missing"><i class="fa-solid fa-triangle-exclamation"></i> Missing</span>`;
            actionBtnHtml = `
                <button type="button" class="btn btn-primary btn-sm btn-upload-missing" onclick="openUploadModalForMissing('${escapeHtml(docName)}', '${escapeHtml(docTypeKey)}')">
                    <i class="fa-solid fa-cloud-arrow-up"></i> Upload Document
                </button>
            `;
        } else if (isUploaded) {
            statusChipHtml = `<span class="status-chip uploaded"><i class="fa-solid fa-clock"></i> Uploaded (Pending Review)</span>`;
            actionBtnHtml = `
                <div style="display: flex; gap: 6px; align-items: center;">
                    <button type="button" class="btn btn-outline btn-sm" onclick="viewDocument(${docId})">
                        <i class="fa-regular fa-eye"></i> View
                    </button>
                    <button type="button" class="btn btn-outline btn-sm" onclick="openUploadModalForMissing('${escapeHtml(docName)}', '${escapeHtml(docTypeKey)}')">
                        <i class="fa-solid fa-repeat"></i> Replace
                    </button>
                </div>
            `;
        } else {
            statusChipHtml = `<span class="status-chip success"><i class="fa-solid fa-circle-check"></i> Ready</span>`;
            actionBtnHtml = docId ? `
                <button type="button" class="btn btn-outline btn-sm" onclick="viewDocument(${docId})">
                    <i class="fa-regular fa-eye"></i> View
                </button>
            ` : '';
        }

        return `
            <div class="doc-check-item ${isMissing ? 'item-missing' : (isUploaded ? 'item-uploaded' : 'item-ready')}">
                <div class="doc-check-details">
                    <div class="doc-title-row">
                        <strong class="doc-check-title">${escapeHtml(docName)}</strong>
                        ${statusChipHtml}
                    </div>
                    <div class="doc-notes-row">
                        ${escapeHtml(d.notes || (isMissing ? 'Required document is unavailable in your locker.' : 'Verified in your citizen locker.'))}
                    </div>
                </div>
                <div class="doc-check-actions">
                    ${actionBtnHtml}
                </div>
            </div>
        `;
    }).join("");
}

function openUploadModalForMissing(docName, docTypeKey) {
    openUploadModal(docTypeKey, docName);
}

async function refreshDocumentReadiness() {
    if (!state.selectedScheme) return;
    try {
        const res = await fetch("/api/workflow/audit-documents", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: state.activeUserId,
                scheme_id: state.selectedScheme.id
            })
        });
        const data = await res.json();
        if (res.ok) {
            state.documentReadiness = data.document_readiness;
            renderDocumentChecklist(data.document_readiness);
        }
    } catch (err) {
        console.error("Failed to refresh document readiness:", err);
    }
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

    try {
        const res = await fetch("/api/workflow/generate-draft", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: state.activeUserId,
                scheme_id: state.selectedScheme.id,
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

    try {
        const res = await fetch("/api/workflow/submit-simulated", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: state.activeUserId,
                scheme_id: state.selectedScheme.id,
                explicit_approval: true,
                applicant_data: applicantData,
                eligibility_answers: state.confirmedRules,
                draft_summary: `Application package for ${state.selectedScheme.name}`
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

let currentDocFilter = "all";

function filterDocsView(filterType) {
    currentDocFilter = filterType;
    document.querySelectorAll(".summary-pill").forEach(pill => pill.classList.remove("active"));
    const activePill = document.getElementById(`pill-filter-${filterType}`);
    if (activePill) activePill.classList.add("active");
    renderDocumentsPage();
}

function formatCategoryLabel(cat) {
    if (!cat) return "Statutory Document";
    const labels = {
        "aadhaar": "Aadhaar Card (Identity Proof)",
        "bank_passbook": "Bank Account Passbook / Statement",
        "land_record": "Land Ownership Record (Khatauni / Khasra)",
        "income_certificate": "Income Certificate",
        "vending_certificate": "Certificate of Vending / Trade Proof",
        "caste_certificate": "Caste / Category Certificate",
        "ration_card": "Ration Card / NFSA ID",
        "educational_certificate": "Educational Marksheet / Fee Receipt",
        "disability_certificate": "Disability Certificate / UDID",
        "other": "Other Supporting Proof"
    };
    return labels[cat.toLowerCase()] || cat.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatDocDate(dateStr) {
    if (!dateStr) return "Recorded Demo";
    try {
        const d = new Date(dateStr.replace(' ', 'T'));
        if (isNaN(d.getTime())) return dateStr;
        return d.toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric"
        });
    } catch (e) {
        return dateStr;
    }
}

function getFileIconClass(doc) {
    const ext = (doc.file_path || '').split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'fa-file-pdf text-danger';
    if (['jpg', 'jpeg', 'png'].includes(ext)) return 'fa-file-image text-primary';
    const type = (doc.doc_type || '').toLowerCase();
    if (type.includes('aadhaar')) return 'fa-id-card text-navy';
    if (type.includes('bank')) return 'fa-money-check text-success';
    if (type.includes('land')) return 'fa-mountain-sun text-warning';
    return 'fa-file-shield text-blue';
}

function renderDocumentsPage() {
    const container = document.getElementById("user-docs-container");
    if (!container) return;

    const totalCountEl = document.getElementById("docs-count-total");
    const verifiedCountEl = document.getElementById("docs-count-verified");
    const uploadedCountEl = document.getElementById("docs-count-uploaded");

    const total = state.allDocuments.length;
    const verified = state.allDocuments.filter(d => (d.status || '').toUpperCase().includes('VERIFIED')).length;
    const uploaded = state.allDocuments.filter(d => (d.status || '').toUpperCase() === 'UPLOADED' || (d.status || '').toUpperCase() === 'PENDING_VERIFICATION').length;

    if (totalCountEl) totalCountEl.textContent = total;
    if (verifiedCountEl) verifiedCountEl.textContent = verified;
    if (uploadedCountEl) uploadedCountEl.textContent = uploaded;

    let filtered = state.allDocuments;
    if (currentDocFilter === "verified") {
        filtered = state.allDocuments.filter(d => (d.status || '').toUpperCase().includes('VERIFIED'));
    } else if (currentDocFilter === "uploaded") {
        filtered = state.allDocuments.filter(d => (d.status || '').toUpperCase() === 'UPLOADED' || (d.status || '').toUpperCase() === 'PENDING_VERIFICATION');
    }

    if (filtered.length === 0) {
        container.innerHTML = `
            <tr>
                <td colspan="5">
                    <div class="empty-state-box" style="padding: 36px 16px;">
                        <div class="empty-state-icon"><i class="fa-solid fa-folder-open"></i></div>
                        <h4>${currentDocFilter === 'all' ? 'No Documents Found in Locker' : `No ${currentDocFilter} documents found`}</h4>
                        <p>Upload your official identity and statutory proofs (PDF, JPG, PNG) or generate a demo set for instant testing.</p>
                        <div style="display: flex; gap: 10px; justify-content: center; margin-top: 14px;">
                            <button type="button" class="btn btn-primary btn-sm" onclick="openUploadModal()">
                                <i class="fa-solid fa-cloud-arrow-up"></i> Upload Document
                            </button>
                            <button type="button" class="btn btn-outline btn-sm" onclick="generateAllDemoDocs()">
                                <i class="fa-solid fa-magic"></i> Auto-Generate Demo Set
                            </button>
                        </div>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    container.innerHTML = filtered.map(doc => {
        const isUploaded = (doc.status || '').toUpperCase() === 'UPLOADED' || (doc.status || '').toUpperCase() === 'PENDING_VERIFICATION';
        const statusChip = isUploaded
            ? `<span class="status-chip uploaded"><i class="fa-solid fa-clock"></i> Uploaded (Pending Review)</span>`
            : `<span class="status-chip success"><i class="fa-solid fa-circle-check"></i> Verified Demo</span>`;

        const categoryFormatted = formatCategoryLabel(doc.doc_type);
        const dateFormatted = formatDocDate(doc.created_at);
        const fileNameSnippet = doc.file_path ? doc.file_path.split('/').pop() : 'Verified Locker Proof';

        return `
            <tr class="doc-table-row" id="doc-row-${doc.id}">
                <td>
                    <div class="doc-name-cell">
                        <div class="doc-icon-mini"><i class="fa-solid ${getFileIconClass(doc)}"></i></div>
                        <div>
                            <strong class="doc-primary-name">${escapeHtml(doc.doc_name || 'Document')}</strong>
                            <div class="doc-filesize-sub">${escapeHtml(fileNameSnippet)}</div>
                        </div>
                    </div>
                </td>
                <td>
                    <span class="category-tag">${escapeHtml(categoryFormatted)}</span>
                </td>
                <td>
                    <span class="date-text"><i class="fa-regular fa-calendar" style="margin-right: 4px; opacity: 0.7;"></i>${escapeHtml(dateFormatted)}</span>
                </td>
                <td>
                    ${statusChip}
                </td>
                <td style="text-align: right;">
                    <div class="doc-actions-inline">
                        <button type="button" class="btn btn-outline btn-xs" onclick="viewDocument(${doc.id})" title="Preview or inspect document">
                            <i class="fa-regular fa-eye"></i> View Document
                        </button>
                        <button type="button" class="btn btn-outline-danger btn-xs" onclick="confirmDeleteDocument(${doc.id}, '${escapeHtml(doc.doc_name || 'Document')}')" title="Delete from locker">
                            <i class="fa-regular fa-trash-can"></i> Delete
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join("");
}

// ==============================================================
// Modal Controls: Upload, View, Delete
// ==============================================================

function handleModalOverlayClick(event, modalId) {
    if (event.target && event.target.id === modalId) {
        if (modalId === 'upload-doc-modal') closeUploadModal();
        else if (modalId === 'view-doc-modal') closeViewDocModal();
        else if (modalId === 'delete-doc-modal') closeDeleteModal();
    }
}

function openUploadModal(categoryHint = "", displayNameHint = "") {
    const modal = document.getElementById("upload-doc-modal");
    if (!modal) return;

    document.getElementById("form-upload-document")?.reset();
    clearSelectedFile();

    const errBox = document.getElementById("upload-modal-error");
    const succBox = document.getElementById("upload-modal-success");
    if (errBox) errBox.style.display = "none";
    if (succBox) succBox.style.display = "none";

    const catSelect = document.getElementById("upload-modal-category");
    const nameInput = document.getElementById("upload-modal-docname");

    if (catSelect && categoryHint) {
        catSelect.value = categoryHint;
    }
    if (nameInput) {
        nameInput.value = displayNameHint || (categoryHint ? formatCategoryLabel(categoryHint) : "");
        nameInput.setAttribute("data-auto", displayNameHint ? "false" : "true");
    }

    modal.style.display = "flex";
}

function closeUploadModal() {
    const modal = document.getElementById("upload-doc-modal");
    if (modal) modal.style.display = "none";
    clearSelectedFile();
}

function handleUploadCategoryChange() {
    const cat = document.getElementById("upload-modal-category")?.value;
    const nameInput = document.getElementById("upload-modal-docname");
    if (cat && nameInput && (!nameInput.value.trim() || nameInput.getAttribute("data-auto") === "true")) {
        nameInput.value = formatCategoryLabel(cat);
        nameInput.setAttribute("data-auto", "true");
    }
}

function handleFileSelection(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    const dropTitle = document.getElementById("drop-zone-title");
    const dropDesc = document.getElementById("drop-zone-desc");
    const dropPreview = document.getElementById("drop-zone-preview");
    const fileNameEl = document.getElementById("drop-zone-filename");
    const fileSizeEl = document.getElementById("drop-zone-filesize");
    const nameInput = document.getElementById("upload-modal-docname");

    const sizeFormatted = file.size < 1024 * 1024
        ? `${(file.size / 1024).toFixed(1)} KB`
        : `${(file.size / (1024 * 1024)).toFixed(2)} MB`;

    if (dropTitle) dropTitle.style.display = "none";
    if (dropDesc) dropDesc.style.display = "none";
    if (dropPreview) dropPreview.style.display = "flex";
    if (fileNameEl) fileNameEl.innerHTML = `<i class="fa-solid fa-file"></i> ${escapeHtml(file.name)}`;
    if (fileSizeEl) fileSizeEl.textContent = sizeFormatted;

    // Suggest clean document display name if still blank or auto
    if (nameInput && (!nameInput.value.trim() || nameInput.getAttribute("data-auto") === "true")) {
        const baseName = file.name.substring(0, file.name.lastIndexOf('.')) || file.name;
        nameInput.value = baseName;
        nameInput.setAttribute("data-auto", "false");
    }
}

function clearSelectedFile(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    const fileInput = document.getElementById("upload-modal-file");
    if (fileInput) fileInput.value = "";

    const dropTitle = document.getElementById("drop-zone-title");
    const dropDesc = document.getElementById("drop-zone-desc");
    const dropPreview = document.getElementById("drop-zone-preview");

    if (dropTitle) dropTitle.style.display = "block";
    if (dropDesc) dropDesc.style.display = "block";
    if (dropPreview) dropPreview.style.display = "none";
}

async function handleUploadDocumentSubmit(event) {
    event.preventDefault();
    const errBox = document.getElementById("upload-modal-error");
    const succBox = document.getElementById("upload-modal-success");
    const submitBtn = document.getElementById("btn-submit-upload");
    const submitText = document.getElementById("btn-upload-text");

    if (errBox) errBox.style.display = "none";
    if (succBox) succBox.style.display = "none";

    const category = document.getElementById("upload-modal-category")?.value;
    const displayName = document.getElementById("upload-modal-docname")?.value.trim();
    const fileInput = document.getElementById("upload-modal-file");
    const file = fileInput?.files && fileInput.files[0];

    if (!category) {
        showUploadError("Please select a valid document category.");
        return;
    }
    if (!displayName) {
        showUploadError("Please specify a Document Display Name.");
        return;
    }
    if (!file) {
        showUploadError("Please select a document file (PDF, JPG, JPEG, or PNG).");
        return;
    }

    const validExts = [".pdf", ".jpg", ".jpeg", ".png"];
    const ext = "." + file.name.split('.').pop().toLowerCase();
    if (!validExts.includes(ext)) {
        showUploadError(`Invalid file format '${ext}'. Only PDF, JPG, JPEG, and PNG files are supported.`);
        return;
    }

    if (file.size > 15 * 1024 * 1024) {
        showUploadError("File size exceeds 15MB limit. Please upload a smaller file.");
        return;
    }

    const formData = new FormData();
    formData.append("user_id", state.activeUserId);
    formData.append("doc_type", category);
    formData.append("doc_name", displayName);
    formData.append("file", file);

    if (submitBtn) submitBtn.disabled = true;
    if (submitText) submitText.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Uploading...`;

    try {
        const res = await fetch("/api/documents/upload", {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Failed to upload document");
        }

        showToast(`Document '${displayName}' uploaded successfully!`, "success");
        closeUploadModal();

        // 100% Synchronization: Refresh DB records, Documents page, Document Readiness, and metrics
        await loadUserDocuments();
        renderDocumentsPage();
        await refreshDocumentReadiness();
        updateDashboardMetrics();

    } catch (err) {
        console.error("Upload error:", err);
        showUploadError(err.message || "Upload failed. Please check backend connection.");
    } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (submitText) submitText.textContent = "Upload Document";
    }
}

function showUploadError(msg) {
    const errBox = document.getElementById("upload-modal-error");
    if (errBox) {
        errBox.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> <span>${escapeHtml(msg)}</span>`;
        errBox.style.display = "flex";
    }
    showToast(msg, "error");
}

async function viewDocument(docId) {
    let doc = state.allDocuments.find(d => d.id === docId);
    if (!doc) {
        try {
            const res = await fetch(`/api/documents/${docId}`);
            const data = await res.json();
            doc = data.document;
        } catch (e) {
            console.error(e);
        }
    }
    if (!doc) {
        showToast("Document details not found", "error");
        return;
    }

    const modal = document.getElementById("view-doc-modal");
    const titleEl = document.getElementById("view-doc-title");
    const tagsEl = document.getElementById("view-doc-tags");
    const previewArea = document.getElementById("view-doc-preview-area");
    const metaEl = document.getElementById("view-doc-metadata");
    const btnDownload = document.getElementById("btn-view-doc-download");
    const btnOpen = document.getElementById("btn-view-doc-open");

    if (titleEl) titleEl.textContent = doc.doc_name || "Official Document";

    const isUploaded = (doc.status || '').toUpperCase() === 'UPLOADED' || (doc.status || '').toUpperCase() === 'PENDING_VERIFICATION';
    const categoryLabel = formatCategoryLabel(doc.doc_type);

    if (tagsEl) {
        tagsEl.innerHTML = `
            <span class="category-tag">${escapeHtml(categoryLabel)}</span>
            <span class="status-chip ${isUploaded ? 'uploaded' : 'success'}">${isUploaded ? 'Uploaded (Pending Review)' : 'Verified Demo'}</span>
            <span class="date-tag"><i class="fa-regular fa-calendar"></i> ${formatDocDate(doc.created_at)}</span>
        `;
    }

    const hasPhysicalFile = !!doc.file_path;
    const fileUrl = `/api/documents/${doc.id}/file`;
    const downloadUrl = `/api/documents/${doc.id}/download`;

    if (btnDownload) {
        if (hasPhysicalFile) {
            btnDownload.href = downloadUrl;
            btnDownload.style.display = "inline-flex";
        } else {
            btnDownload.style.display = "none";
        }
    }

    if (btnOpen) {
        if (hasPhysicalFile) {
            btnOpen.href = fileUrl;
            btnOpen.style.display = "inline-flex";
        } else {
            btnOpen.style.display = "none";
        }
    }

    // Render Preview
    if (previewArea) {
        const filePath = (doc.file_path || '').toLowerCase();
        if (filePath.endsWith('.png') || filePath.endsWith('.jpg') || filePath.endsWith('.jpeg')) {
            previewArea.innerHTML = `
                <div class="image-preview-wrapper">
                    <img src="${fileUrl}" alt="${escapeHtml(doc.doc_name)}" class="preview-img-element" onerror="this.onerror=null; this.src='/static/placeholder-doc.svg';" />
                </div>
            `;
        } else if (filePath.endsWith('.pdf')) {
            previewArea.innerHTML = `
                <div class="pdf-preview-wrapper">
                    <iframe src="${fileUrl}#toolbar=1" class="preview-iframe-element" title="PDF Document Preview"></iframe>
                </div>
            `;
        } else {
            // Simulated Official Certificate for demo records
            const ocr = doc.verified_ocr_data || {};
            previewArea.innerHTML = `
                <div class="demo-certificate-preview">
                    <div class="cert-header">
                        <div class="cert-emblem"><i class="fa-solid fa-landmark-flag"></i></div>
                        <div class="cert-title">
                            <h4>GOVERNMENT STATUTORY DEMO RECORD</h4>
                            <span>${escapeHtml(categoryLabel.toUpperCase())}</span>
                        </div>
                        <div class="cert-seal"><i class="fa-solid fa-stamp"></i> OFFICIAL DEMO SEAL</div>
                    </div>
                    <div class="cert-body">
                        <div class="cert-field-row">
                            <span class="cert-label">Document Display Name:</span>
                            <strong class="cert-value">${escapeHtml(doc.doc_name)}</strong>
                        </div>
                        <div class="cert-field-row">
                            <span class="cert-label">Citizen / Beneficiary:</span>
                            <strong class="cert-value">${escapeHtml(ocr.holder_name || ocr.applicant_name || ocr.vendor_name || ocr.owner_name || state.currentUser?.full_name || 'Citizen')}</strong>
                        </div>
                        <div class="cert-field-row">
                            <span class="cert-label">Certificate / Identification No:</span>
                            <strong class="cert-value cert-code">${escapeHtml(ocr.aadhaar_masked || ocr.cov_number || ocr.cert_id || ocr.khasra_no || ocr.account_masked || `JS-DOC-${doc.id}`)}</strong>
                        </div>
                        <div class="cert-field-row">
                            <span class="cert-label">Verification Status:</span>
                            <span class="cert-status-badge ${isUploaded ? 'pending' : 'verified'}">${isUploaded ? 'UPLOADED (PENDING REVIEW)' : 'STATUTORILY VERIFIED'}</span>
                        </div>
                    </div>
                    <div class="cert-footer">
                        <span>Persisted in JanSetu SQLite Database • Synchronized across Documents and Document Readiness Agent</span>
                    </div>
                </div>
            `;
        }
    }

    // Metadata Grid
    if (metaEl) {
        const ocr = doc.verified_ocr_data || {};
        let extraFields = '';
        Object.entries(ocr).forEach(([k, v]) => {
            if (typeof v !== 'object' && v !== null && k !== 'file_name' && k !== 'verification_status' && k !== 'saved_filename') {
                const label = k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                extraFields += `<div class="meta-item"><span>${escapeHtml(label)}:</span> <strong>${escapeHtml(String(v))}</strong></div>`;
            }
        });

        metaEl.innerHTML = `
            <div class="metadata-grid">
                <div class="meta-item"><span>Document ID:</span> <strong>#${doc.id}</strong></div>
                <div class="meta-item"><span>Category:</span> <strong>${escapeHtml(categoryLabel)}</strong></div>
                <div class="meta-item"><span>Status:</span> <strong>${isUploaded ? 'Uploaded (In Review)' : 'Verified Demo'}</strong></div>
                <div class="meta-item"><span>Created Date:</span> <strong>${formatDocDate(doc.created_at)}</strong></div>
                ${extraFields}
            </div>
        `;
    }

    if (modal) modal.style.display = "flex";
}

function closeViewDocModal() {
    const modal = document.getElementById("view-doc-modal");
    if (modal) modal.style.display = "none";
    const previewArea = document.getElementById("view-doc-preview-area");
    if (previewArea) previewArea.innerHTML = "";
}

function confirmDeleteDocument(docId, docName) {
    state.documentToDelete = { id: docId, name: docName };
    const modal = document.getElementById("delete-doc-modal");
    const nameTarget = document.getElementById("delete-doc-name-target");
    if (nameTarget) nameTarget.textContent = `"${docName}"`;
    if (modal) modal.style.display = "flex";
}

function closeDeleteModal() {
    const modal = document.getElementById("delete-doc-modal");
    if (modal) modal.style.display = "none";
    state.documentToDelete = null;
}

async function executeDeleteDocument() {
    if (!state.documentToDelete || !state.documentToDelete.id) return;
    const docId = state.documentToDelete.id;
    const docName = state.documentToDelete.name;
    const btn = document.getElementById("btn-confirm-delete");

    if (btn) btn.disabled = true;

    try {
        const res = await fetch(`/api/documents/${docId}?user_id=${state.activeUserId}`, {
            method: "DELETE"
        });
        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Failed to delete document");
        }

        showToast(`Document '${docName}' deleted from locker.`, "success");
        closeDeleteModal();

        // 100% Synchronization: Refresh DB records, Documents page, Document Readiness, and metrics
        await loadUserDocuments();
        renderDocumentsPage();
        await refreshDocumentReadiness();
        updateDashboardMetrics();

    } catch (err) {
        console.error("Delete error:", err);
        showToast(err.message || "Failed to delete document", "error");
    } finally {
        if (btn) btn.disabled = false;
    }
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
            container.innerHTML = state.notifications.map(n => `
                <div style="padding: 10px 0; border-bottom: 1px solid var(--border-subtle)">
                    <strong style="font-size: 13px;">${escapeHtml(n.title)}</strong>
                    <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">${escapeHtml(n.message)}</p>
                </div>
            `).join("") || "<p style='font-size: 13px; color: var(--text-muted)'>No active alerts.</p>";
        }
    }
}

// Profile Page
function populateProfileForm() {
    if (!state.currentUser) return;
    const u = state.currentUser;
    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.value = val !== undefined ? val : "";
    };

    setVal("prof-name", u.full_name);
    setVal("prof-age", u.age || 35);
    setVal("prof-gender", u.gender || "Male");
    setVal("prof-occupation", u.occupation || "Worker");
    setVal("prof-income", u.annual_income || 120000);
    setVal("prof-category", u.social_category || "General");
    setVal("prof-residence", u.residence_area || "Urban");
    setVal("prof-land", u.land_ownership_hectares || 0.0);
    setVal("prof-location", `${u.district || 'Jaipur'}, ${u.state || 'Rajasthan'}`);

    const bplEl = document.getElementById("prof-bpl");
    if (bplEl) bplEl.checked = !!u.is_bpl;
}

async function handleProfileSave(event) {
    event.preventDefault();
    const payload = {
        age: parseInt(document.getElementById("prof-age").value),
        gender: document.getElementById("prof-gender").value,
        occupation: document.getElementById("prof-occupation").value,
        annual_income: parseFloat(document.getElementById("prof-income").value),
        social_category: document.getElementById("prof-category").value,
        residence_area: document.getElementById("prof-residence").value,
        land_ownership_hectares: parseFloat(document.getElementById("prof-land").value),
        is_bpl: document.getElementById("prof-bpl").checked
    };

    try {
        const res = await fetch(`/api/users/${state.activeUserId}/profile`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok && data.user) {
            setAuthenticatedUser(data.user);
            showToast("Citizen profile saved successfully!", "success");
        }
    } catch (err) {
        console.error("Failed to save profile:", err);
        showToast("Error updating profile.", "error");
    }
}

// ==============================================================
// Secondary Chatbot: Sahayak Mitra Drawer
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
                message: msg
            })
        });

        const data = await res.json();
        const replyText = data.reply || data.response;
        if (res.ok && replyText) {
            appendChatMessage("bot", replyText);
        } else {
            appendChatMessage("bot", "I am having trouble connecting right now. Please explore schemes in the Scheme Directory.");
        }
    } catch (err) {
        console.error("Chat error:", err);
        appendChatMessage("bot", "Backend service offline. Please try again later.");
    }
}

function appendChatMessage(sender, text) {
    const container = document.getElementById("chat-messages");
    if (!container) return;

    const div = document.createElement("div");
    div.className = `chat-bubble ${sender}-message`;
    div.innerHTML = `
        <div class="msg-author">${sender === 'user' ? 'You' : '<i class="fa-solid fa-robot"></i> Sahayak Mitra'}</div>
        <div class="msg-content">${escapeHtml(text).replace(/\n/g, '<br>')}</div>
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

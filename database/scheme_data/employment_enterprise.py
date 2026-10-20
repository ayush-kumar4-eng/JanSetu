"""
Employment, Livelihoods & Micro-Enterprise Schemes Dataset (Verified Official Data)
Sources: Ministry of Housing and Urban Affairs (pmsvanidhi.mohua.gov.in), Ministry of MSME (msme.gov.in),
Ministry of Rural Development (nrega.nic.in, rural.nic.in), Ministry of Skill Development and Entrepreneurship.
"""

EMPLOYMENT_SCHEMES = [
    {
        "code": "PM-SVANIDHI",
        "name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "name_hindi": "पीएम स्वनिधि योजना (स्ट्रीट वेंडर्स)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Housing and Urban Affairs",
        "category": "Employment & Skill Development",
        "target_audience": "Urban street vendors, hawkers, thela-walas, and small roadside merchants",
        "short_description": "Affordable collateral-free working capital loan of ₹10,000, ₹20,000, and ₹50,000 with 7% interest subsidy and digital cashback.",
        "full_description": "PM SVANidhi was launched to empower urban street vendors to resume their livelihoods and transition into the formal financial fold. Vendors can avail an initial working capital loan of up to ₹10,000. On timely repayment, they graduate to second tranche of ₹20,000 and third tranche of ₹50,000, with a 7% interest subvention and up to ₹1,200 annual cashback on digital transactions.",
        "benefits": "Collateral-free working capital credit: 1st tranche up to ₹10,000 (1 yr tenure), 2nd tranche up to ₹20,000, 3rd tranche up to ₹50,000. 7% per annum interest subsidy directly credited via DBT. Cashback up to ₹100 per month (₹1,200/year) on UPI digital transactions.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 65,
            "max_annual_income": 300000,
            "eligible_occupations": ["Street Vendor", "Hawker", "Food Stall Owner", "Artisan", "Small Trader", "Cobbler", "Barber", "Daily Wage Earner"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be engaged in street vending in urban or peri-urban areas.",
                "Possession of Certificate of Vending (CoV) / Identity Card issued by Urban Local Bodies (ULB) OR a Letter of Recommendation (LoR).",
                "Operational bank account linked with Aadhaar.",
                "No previous default in formal institutional micro-loans."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Voter ID / Ration Card",
            "Certificate of Vending (CoV) or Letter of Recommendation (LoR) from ULB/Town Vending Committee",
            "Active Bank Account Passbook",
            "Passport Size Photograph"
        ],
        "application_process": "1. Verify vending status via Town Vending Committee survey list or obtain LoR from ULB. 2. Submit loan application online at pmsvanidhi.mohua.gov.in or through CSC. 3. Select preferred lending bank/NBFC. 4. Digital sanction and direct disbursement into account.",
        "official_url": "https://pmsvanidhi.mohua.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Housing and Urban Affairs & myScheme Portal",
        "tags": "street vendor, loan, working capital, small business, urban, collateral-free, mudra, subsidy"
    },
    {
        "code": "PM-VISHWAKARMA",
        "name": "PM Vishwakarma Scheme",
        "name_hindi": "पीएम विश्वकर्मा योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Micro, Small and Medium Enterprises",
        "category": "Employment & Skill Development",
        "target_audience": "Traditional artisans and craftspeople working with hands and tools across 18 designated trades",
        "short_description": "₹15,000 free toolkit grant, 5-7 days skill training with ₹500/day stipend, and up to ₹3 Lakh collateral-free loan at concessional 5% interest.",
        "full_description": "Central sector scheme designed to uplift and preserve the guru-shishya parampara of traditional artisans and craftspeople. Covers 18 trades (Carpenters, Blacksmiths, Potters, Sculptors, Cobblers, Masons, Barbers, Tailors, Washermen, etc.) with end-to-end support including PM Vishwakarma Certificate & ID, basic/advanced skill training, modern toolkits, collateral-free enterprise loans, and marketing support.",
        "benefits": "Free PM Vishwakarma Certificate and ID Card. Basic skill training (5-7 days) with ₹500/day stipend. ₹15,000 digital toolkit incentive voucher. Collateral-free enterprise loan up to ₹1,00,000 (1st tranche) and ₹2,00,000 (2nd tranche) at concessional 5% interest rate (8% interest subvention paid by MoMSME).",
        "max_benefit_amount": 300000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 70,
            "max_annual_income": None,
            "eligible_occupations": ["Carpenter", "Blacksmith", "Armourer", "Hammer and Tool Kit Maker", "Locksmith", "Sculptor", "Goldsmith", "Potter", "Cobbler", "Mason", "Basket/Mat Maker", "Doll & Toy Maker", "Barber", "Garland Maker", "Washerman", "Tailor", "Fishing Net Maker"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "An artisan or craftsperson working with their hands and tools in one of the 18 designated family-based traditional trades.",
                "Minimum age of 18 years on date of application.",
                "Beneficiary should not have availed loans under similar credit-based schemes like PMEGP, PM SVANidhi, or Mudra in the past 5 years.",
                "Only one member of the family is eligible."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Mobile number linked to Aadhaar",
            "Bank Account Passbook",
            "Ration Card (for family composition verification)",
            "Trade verification proof / Gram Panchayat recommendation"
        ],
        "application_process": "1. Free biometric registration at Common Service Centre (CSC) on pmvishwakarma.gov.in. 2. Three-stage verification: Gram Panchayat / ULB level, District Implementation Committee, and Screening Committee. 3. Certificate issued, training initiated, and credit sanctioned.",
        "official_url": "https://pmvishwakarma.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of MSME & National Council for Vocational Education and Training",
        "tags": "vishwakarma, artisan, craftsperson, carpenter, blacksmith, potter, tailor, toolkit grant, 5 percent loan"
    },
    {
        "code": "PMEGP",
        "name": "Prime Minister's Employment Generation Programme (PMEGP)",
        "name_hindi": "प्रधानमंत्री रोजगार सृजन कार्यक्रम",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Micro, Small and Medium Enterprises",
        "category": "Employment & Skill Development",
        "target_audience": "Prospective entrepreneurs, rural youth, women, and self-help groups establishing new micro-enterprises",
        "short_description": "15% to 35% government capital subsidy on bank-financed micro-enterprise projects up to ₹50 Lakh (manufacturing) and ₹20 Lakh (services).",
        "full_description": "PMEGP is a credit-linked subsidy programme administered by Khadi and Village Industries Commission (KVIC) as the national nodal agency. It facilitates self-employment generation by establishing micro-enterprises in non-farm sectors through bank loans and upfront margin money capital subsidies.",
        "benefits": "Capital subsidy of 15% (urban) to 25% (rural) for General category; and 25% (urban) to 35% (rural) for Special categories (SC, ST, OBC, Women, Ex-Servicemen, Divyangjan, Minorities). Maximum project cost up to ₹50 Lakh for manufacturing and ₹20 Lakh for service units.",
        "max_benefit_amount": 1750000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 65,
            "max_annual_income": None,
            "eligible_occupations": ["Entrepreneur", "Artisan", "Self Employed", "Unemployed Youth"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Individual must be at least 18 years old. No income ceiling for setting up projects.",
                "For projects costing above ₹10 Lakh in manufacturing and above ₹5 Lakh in service sector, beneficiary must possess minimum Class 8 pass qualification.",
                "Only new projects (greenfield units) are sanctioned. Existing units are not eligible for first-stage subsidy."
            ]
        },
        "required_documents": [
            "Aadhaar Card and PAN Card",
            "Detailed Project Report (DPR) with machinery quotations",
            "Class 8 / Higher Educational Marksheet",
            "Special Category Certificate (Caste / Disability / Ex-Servicemen certificate if applicable)",
            "Rural Area Certificate from Gram Panchayat / Tehsildar (for rural subsidy rate)"
        ],
        "application_process": "1. Apply online on PMEGP e-Portal (kviconline.gov.in/pmegpeportal). 2. Submit DPR and select financing bank branch. 3. District Task Force Committee (DTFC) reviews application. 4. Bank conducts appraisal and releases loan with KVIC subsidy parked as TDR for 3 years.",
        "official_url": "https://www.kviconline.gov.in/pmegpeportal",
        "verification_date": "2026-10-20",
        "source": "Khadi and Village Industries Commission (KVIC) & MoMSME",
        "tags": "pmegp, business subsidy, kvic, micro enterprise, start business, manufacturing loan, margin money"
    },
    {
        "code": "MGNREGA",
        "name": "Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA)",
        "name_hindi": "महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी अधिनियम (मनरेगा)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Rural Development",
        "category": "Employment & Skill Development",
        "target_audience": "Adult members of rural households willing to do unskilled manual work",
        "short_description": "Legal guarantee of at least 100 days of wage employment in a financial year to every rural household doing unskilled manual work.",
        "full_description": "MGNREGA is the world's largest social security and public works programme. It guarantees 100 days of wage employment per financial year to adult members of any rural household volunteering for unskilled manual labor, creating durable community assets like ponds, wells, check dams, and rural roads.",
        "benefits": "Statutory wage rate (₹230 to ₹375 per day depending on state) credited directly into bank/post office account via DBT within 15 days of work. Entitled to unemployment allowance if employment is not provided within 15 days of application.",
        "max_benefit_amount": 37500,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Daily Wage Earner", "Agricultural Labourer", "Rural Worker", "Unskilled Labourer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be an adult resident of a rural area in the respective Gram Panchayat.",
                "Willing to undertake unskilled manual labour.",
                "Must hold a valid MGNREGA Job Card issued by the Gram Panchayat.",
                "Aadhaar-based Payment System (ABPS) enabled bank account."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "MGNREGA Job Card",
            "Bank / Post Office Account Passbook (ABPS enabled)",
            "Passport Size Photograph"
        ],
        "application_process": "1. Submit written application or oral request for work to Gram Panchayat / Programme Officer. 2. Dated receipt issued to applicant. 3. Work allocated within 5 km radius within 15 days. 4. Fortnightly muster roll measurement and wage DBT credit.",
        "official_url": "https://nrega.nic.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Rural Development (nrega.nic.in)",
        "tags": "mgnrega, nrega, guaranteed work, rural employment, daily wage, job card, dbt wage"
    },
    {
        "code": "MUDRA-SHISHU",
        "name": "Pradhan Mantri Mudra Yojana - Shishu Loan (PMMY)",
        "name_hindi": "प्रधानमंत्री मुद्रा योजना - शिशु ऋण",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Micro-entrepreneurs, small shopkeepers, fruit/vegetable vendors, and self-employed individuals",
        "short_description": "Collateral-free institutional micro loan up to ₹50,000 for setting up or running small business activities.",
        "full_description": "PMMY was launched to fund the unfunded by bringing non-corporate small business enterprises into formal banking fold. Under the Shishu category, first-time entrepreneurs and small shopkeepers can secure micro credit up to ₹50,000 with zero processing fees and no third-party collateral.",
        "benefits": "Collateral-free loan up to ₹50,000 repayable in flexible monthly installments up to 5 years. Zero processing fee for Shishu category loans. Mudra RuPay debit card issued for working capital withdrawals.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 65,
            "max_annual_income": None,
            "eligible_occupations": ["Street Vendor", "Shopkeeper", "Artisan", "Tailor", "Driver", "Small Business Owner"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Borrower must be an Indian citizen with a viable non-farm income generating business plan.",
                "Must not be a defaulter to any commercial bank, cooperative bank, or NBFC.",
                "Loan must be utilized for business activity (working capital or small asset purchase)."
            ]
        },
        "required_documents": [
            "Aadhaar Card / Voter ID",
            "Proof of residence and business address",
            "Passport size photographs",
            "Quotation of machinery/items to be purchased or business outline",
            "Bank Account statement for past 6 months (if existing account holder)"
        ],
        "application_process": "1. Apply online via Udyami Mitra / JanSamarth portal (jansamarth.in) or visit any commercial bank/MFI. 2. Fill standard 1-page PMMY Shishu application. 3. Bank sanctions loan and issues Mudra card within 7-10 working days.",
        "official_url": "https://www.mudra.org.in",
        "verification_date": "2026-10-20",
        "source": "MUDRA & Department of Financial Services, Ministry of Finance",
        "tags": "mudra loan, shishu, collateral free loan, 50000 loan, small shop, micro credit, pmmy"
    },
    {
        "code": "MUDRA-KISHORE",
        "name": "Pradhan Mantri Mudra Yojana - Kishore Loan (PMMY)",
        "name_hindi": "प्रधानमंत्री मुद्रा योजना - किशोर ऋण",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Growing small business enterprises requiring equipment purchase or working capital expansion",
        "short_description": "Collateral-free business enterprise loans from ₹50,000 to ₹5,00,000 with flexible tenures up to 5 years.",
        "full_description": "The Kishore category under PMMY caters to micro and small business enterprises that are already established and looking to expand operations, purchase equipment, or increase working capital. Loans are guaranteed by the Credit Guarantee Fund for Micro Units (CGFMU).",
        "benefits": "Credit facility between ₹50,000 and ₹5,00,000 without requiring physical collateral. Interest rates tied to bank benchmark MCLR/EBLR. Repayment tenure up to 60 months with moratorium option.",
        "max_benefit_amount": 500000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 65,
            "max_annual_income": None,
            "eligible_occupations": ["Business Owner", "Trader", "Manufacturer", "Service Provider", "Small Workshop Owner"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Small enterprise with a viable business model requiring credit between ₹50,000 and ₹5 Lakh.",
                "No past loan defaults in CIBIL/Credit bureau records.",
                "Must be registered (Udyam Registration recommended)."
            ]
        },
        "required_documents": [
            "Aadhaar Card and PAN Card",
            "Udyam Registration Certificate",
            "Business address proof and lease deed/utility bill",
            "Bank statements for last 12 months",
            "Projected balance sheet / sales estimates for next financial year"
        ],
        "application_process": "1. Apply through JanSamarth portal (jansamarth.in) or visit bank branch. 2. Upload KYC and business performance figures. 3. In-principle approval and sanction within 14 days.",
        "official_url": "https://www.mudra.org.in",
        "verification_date": "2026-10-20",
        "source": "MUDRA & Department of Financial Services",
        "tags": "mudra kishore, business expansion, equipment loan, working capital, collateral free, 5 lakh loan"
    },
    {
        "code": "PMKVY",
        "name": "Pradhan Mantri Kaushal Vikas Yojana 4.0 (PMKVY)",
        "name_hindi": "प्रधानमंत्री कौशल विकास योजना 4.0",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Skill Development and Entrepreneurship",
        "category": "Employment & Skill Development",
        "target_audience": "School/college dropouts, unemployed youth, and informal workers seeking certified vocational skills",
        "short_description": "Free industry-aligned certified skill training, assessment, NSDC certification, post-placement support, and accident insurance.",
        "full_description": "PMKVY 4.0 is the flagship outcome-based skill training scheme of the Ministry of Skill Development and Entrepreneurship (MSDE) executed by National Skill Development Corporation (NSDC). It offers Short Term Training (STT) and Recognition of Prior Learning (RPL) in modern domains including Industry 4.0, AI, robotics, healthcare, drone technology, green energy, and construction.",
        "benefits": "100% free government-sponsored training and assessment. Sector Skill Council / NCVET recognized certificate. Daily conveyance allowance and ₹500 stipend upon passing certification. Direct placement linkages with industry employers.",
        "max_benefit_amount": 10000,
        "eligibility_criteria": {
            "min_age": 15,
            "max_age": 45,
            "max_annual_income": None,
            "eligible_occupations": ["Unemployed Youth", "Student", "Drop-out", "Informal Worker"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Indian national aged 15 to 45 years with an Aadhaar card and active bank account.",
                "Unemployed youth or school/college dropouts possessing foundational educational qualification required for the specific job role.",
                "Must attend minimum 70% mandatory practical and theory training classes at accredited centre."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Educational Marksheets (8th/10th/12th as applicable to course)",
            "Bank Account Passbook (Aadhaar linked)",
            "Passport size photographs"
        ],
        "application_process": "1. Register on Skill India Digital portal (skillindiadigital.gov.in). 2. Find accredited PMKVY training centre and desired course job role. 3. Complete course module and undergo biometric assessment. 4. Digital Certificate delivered on Skill India Locker.",
        "official_url": "https://www.skillindiadigital.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Skill Development Corporation (NSDC) & MSDE",
        "tags": "skill training, pmkvy, free vocational course, certified electrician, computer course, job placement"
    }
]

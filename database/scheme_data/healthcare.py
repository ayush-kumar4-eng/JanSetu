"""
Healthcare & Wellness Schemes Dataset (Verified Official Data)
Sources: National Health Authority (pmjay.gov.in), Ministry of Health and Family Welfare (mohfw.gov.in),
Department of Pharmaceuticals (janaushadhi.gov.in).
"""

HEALTHCARE_SCHEMES = [
    {
        "code": "PM-JAY",
        "name": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (AB-PMJAY)",
        "name_hindi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Health and Family Welfare",
        "category": "Health & Wellness",
        "target_audience": "Bottom 40% vulnerable families identified by SECC 2011 and senior citizens aged 70 and above",
        "short_description": "Cashless health insurance cover of up to ₹5,00,000 per family per year for secondary and tertiary hospitalization.",
        "full_description": "AB-PMJAY is the world's largest government-funded health assurance scheme. It provides a health cover of ₹5 Lakh per family per year for secondary and tertiary care hospitalization across public and empaneled private hospitals. All senior citizens aged 70 and above are also entitled to a distinct ₹5 Lakh top-up cover irrespective of income.",
        "benefits": "Cashless and paperless access to 1,949 medical procedures covering diagnostics, surgeries, ICU, implants, medicine, and post-hospitalization for 15 days, up to ₹5,00,000 per family per year. No cap on family size or age.",
        "max_benefit_amount": 500000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All", "Daily Wage Earner", "Street Vendor", "Domestic Worker", "Construction Worker", "Agricultural Labourer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Families listed in the Socio-Economic Caste Census (SECC 2011) database (D1 to D7 deprivation criteria in rural areas and 11 occupational categories in urban areas).",
                "Senior citizens aged 70 and above are universally eligible under the expanded Ayushman Vaya Vandana card regardless of socio-economic status.",
                "NFSA ration card holders in participating states are automatically eligible."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Ration Card / Family ID document",
            "Active mobile number linked to Aadhaar"
        ],
        "application_process": "1. Check eligibility on mera.pmjay.gov.in or beneficiary.nha.gov.in using Aadhaar/Ration Card. 2. Visit any empaneled hospital or CSC. 3. Ayushman Mitra verifies biometrics and issues Ayushman PVC Card / Digital Card.",
        "official_url": "https://beneficiary.nha.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Health Authority (NHA) & myScheme Portal",
        "tags": "ayushman bharat, pmjay, health insurance, hospitalization, cashless medical, free treatment, 5 lakh"
    },
    {
        "code": "PMBJP",
        "name": "Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP)",
        "name_hindi": "प्रधानमंत्री भारतीय जनऔषधि परियोजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Chemicals and Fertilizers",
        "category": "Health & Wellness",
        "target_audience": "All citizens seeking affordable high-quality generic medicines and surgical items",
        "short_description": "Quality generic medicines and surgical consumables sold at 50% to 90% lower prices than branded medicines through Kendra outlets.",
        "full_description": "PMBJP was launched by the Pharmaceuticals & Medical Devices Bureau of India (PMBI) to make quality generic medicines accessible and affordable to all. Jan Aushadhi Kendras offer more than 2,000 generic medicines and 300 surgical items conforming to WHO-GMP standards at steep discounts.",
        "benefits": "Price reduction of 50% to 90% compared to branded market medicines. Oxo-biodegradable sanitary napkins (Suvidha) available at ₹1 per pad. Blood pressure, diabetes, cardiac, and oncology medicines available at fractional prices.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Open to all Indian citizens without any income or category restrictions.",
                "Doctor's prescription required for Schedule H and H1 prescription drugs.",
                "OTC items, nutraceuticals, and sanitary pads available without prescription."
            ]
        },
        "required_documents": [
            "Valid Doctor's Prescription (for prescription medications)"
        ],
        "application_process": "Walk-in to any of the 10,000+ Jan Aushadhi Kendras across India with prescription, or locate nearest outlet via 'Jan Aushadhi Sugam' mobile application.",
        "official_url": "https://janaushadhi.gov.in",
        "verification_date": "2026-10-20",
        "source": "Pharmaceuticals & Medical Devices Bureau of India (PMBI)",
        "tags": "janaushadhi, cheap medicine, generic medicine, pharmacy, health, suvidha pad, affordable healthcare"
    },
    {
        "code": "JSSK",
        "name": "Janani Shishu Suraksha Karyakram (JSSK)",
        "name_hindi": "जननी शिशु सुरक्षा कार्यक्रम",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Health and Family Welfare",
        "category": "Health & Wellness",
        "target_audience": "All pregnant women delivering in public health institutions and sick infants up to 1 year of age",
        "short_description": "Completely free and cashless delivery (including C-section), free drugs, diagnostics, blood, diet, and transport.",
        "full_description": "JSSK guarantees zero out-of-pocket expenses for pregnant women delivering in government health facilities, including normal deliveries and caesarean sections. The entitlement extends to sick infants up to one year of age accessing public health institutions.",
        "benefits": "100% free delivery and C-section; free drugs, consumables, and diagnostic tests; free provision of blood; free diet during stay (up to 3 days for normal delivery, 7 days for caesarean); and free transport from home to hospital, inter-facility transfer, and drop back home.",
        "max_benefit_amount": 15000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 45,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a pregnant woman accessing care at any public health institution (PHC, CHC, District Hospital, Medical College).",
                "Sick infants up to 1 year of age treated at public facilities are also fully covered.",
                "No income ceiling, caste criteria, or parity limitation."
            ]
        },
        "required_documents": [
            "Mother and Child Tracking System (MCTS) / RCH Card (MCP Card)",
            "Aadhaar Card of mother"
        ],
        "application_process": "Approach any government hospital, Primary Health Centre (PHC), or Community Health Centre (CHC). Contact local ASHA or ANM worker, or call National Ambulance Service (108/102).",
        "official_url": "https://nhm.gov.in/index1.php?lang=1&level=2&sublinkid=842&lid=309",
        "verification_date": "2026-10-20",
        "source": "National Health Mission (NHM) & MoHFW",
        "tags": "maternity, pregnancy, free delivery, infant care, jssk, c-section, ambulance, nhm"
    },
    {
        "code": "JSY",
        "name": "Janani Suraksha Yojana (JSY)",
        "name_hindi": "जननी सुरक्षा योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Health and Family Welfare",
        "category": "Health & Wellness",
        "target_audience": "Poor pregnant women delivering in health institutions to reduce maternal and neonatal mortality",
        "short_description": "Cash assistance of ₹1,400 (rural) and ₹1,000 (urban) directly to pregnant women upon institutional delivery.",
        "full_description": "JSY is a safe motherhood intervention under the National Health Mission (NHM). It promotes institutional delivery among poor pregnant women through conditional cash transfer. States are categorized into Low Performing States (LPS) and High Performing States (HPS) with special incentives.",
        "benefits": "Cash incentive of ₹1,400 for rural mothers and ₹1,000 for urban mothers in Low Performing States (LPS); ₹700 (rural) and ₹600 (urban) for BPL/SC/ST mothers in High Performing States. ASHA incentive of ₹600 included for escorting mother.",
        "max_benefit_amount": 1400,
        "eligibility_criteria": {
            "min_age": 19,
            "max_age": 45,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All", "SC", "ST", "BPL"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Delivery must take place in a government health centre or accredited private hospital.",
                "In Low Performing States (e.g. UP, Bihar, Rajasthan, MP, Odisha, Jharkhand, Chhattisgarh, Uttarakhand, Assam, J&K), all pregnant women are eligible regardless of age, caste, or birth parity.",
                "In High Performing States, assistance is restricted to BPL and SC/ST mothers up to 2 live births."
            ]
        },
        "required_documents": [
            "Mother-Child Protection (MCP) Card",
            "Aadhaar Card",
            "BPL Ration Card (for HPS states)",
            "Bank Account Passbook (Aadhaar linked)",
            "Discharge slip / Birth certificate from hospital"
        ],
        "application_process": "1. Register pregnancy with local ASHA / ANM within first trimester. 2. Undergo required ANC checkups. 3. Deliver baby at public/accredited hospital. 4. Medical Officer sanctions DBT cash payment into bank account prior to discharge.",
        "official_url": "https://nhm.gov.in/index1.php?lang=1&level=3&lid=309&sublinkid=841",
        "verification_date": "2026-10-20",
        "source": "National Health Mission & Ministry of Health and Family Welfare",
        "tags": "jsy, institutional delivery, safe motherhood, pregnancy cash transfer, asha, infant care"
    },
    {
        "code": "NIKSHAY-POSHAN",
        "name": "Ni-Kshay Poshan Yojana (NPY)",
        "name_hindi": "निक्षय पोषण योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Health and Family Welfare",
        "category": "Health & Wellness",
        "target_audience": "All notified Tuberculosis (TB) patients undergoing treatment in public or private health facilities",
        "short_description": "Direct financial incentive of ₹500 to ₹1,000 per month for nutritional support to TB patients throughout treatment duration.",
        "full_description": "Centrally sponsored scheme under the National Tuberculosis Elimination Programme (NTEP). Provides nutritional support to tuberculosis patients to combat undernutrition, enhance recovery, and prevent treatment interruption.",
        "benefits": "Direct financial transfer of ₹500 per month (recently enhanced to ₹1,000/month in designated categories) deposited directly into the patient's bank account for each month of active anti-TB treatment (minimum 6 months = ₹3,000+).",
        "max_benefit_amount": 6000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a diagnosed Tuberculosis patient registered and notified on the Ni-kshay web portal.",
                "Both public sector and private sector notified patients are eligible.",
                "Must be undergoing active medical treatment under DOTS / NTEP protocol."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Ni-Kshay Patient ID (generated by treating doctor/clinic)",
            "Bank Account Passbook (Aadhaar linked)",
            "Diagnostic / Sputum test report"
        ],
        "application_process": "1. Patient is diagnosed and notified on Ni-Kshay portal by public dispensary or private doctor. 2. Health worker / Senior Treatment Supervisor (STS) enters patient's bank account details on nikshay.in. 3. Monthly DBT amounts credited directly via PFMS.",
        "official_url": "https://www.nikshay.in",
        "verification_date": "2026-10-20",
        "source": "Central TB Division (CTD) & MoHFW",
        "tags": "tb, tuberculosis, nutrition support, nikshay, poshan, dbt, chronic illness, health"
    },
    {
        "code": "PMSMA",
        "name": "Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA)",
        "name_hindi": "प्रधानमंत्री सुरक्षित मातृत्व अभियान",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Health and Family Welfare",
        "category": "Health & Wellness",
        "target_audience": "All pregnant women in their 2nd or 3rd trimester visiting designated public health facilities",
        "short_description": "Free, comprehensive, and quality antenatal care (ANC) package on the 9th of every month by OBGYN specialists.",
        "full_description": "PMSMA provides assured, comprehensive, and quality antenatal care free of cost to all pregnant women on the 9th of every month. It aims to detect and manage high-risk pregnancies (HRP) early, through expert screening by specialized obstetricians and gynecologists.",
        "benefits": "Free comprehensive diagnostic tests (blood, urine, ultrasound, hemoglobin, blood sugar) and expert clinical check-ups by specialist doctors. High-risk pregnancies tagged with red stickers on MCP card for priority referral and institutional delivery tracking.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 45,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Woman must be pregnant and in her 2nd or 3rd trimester (after 3 months of pregnancy).",
                "Available at designated public health facilities (District Hospitals, Sub-District Hospitals, CHCs, and PHCs) on the 9th day of each calendar month."
            ]
        },
        "required_documents": [
            "Mother and Child Protection (MCP) Card",
            "Aadhaar Card",
            "Previous ultrasound or blood reports (if any)"
        ],
        "application_process": "Visit the nearest government hospital, CHC, or PHC on the 9th of any month. Register at the PMSMA special registration desk for free clinical examinations and lab investigations.",
        "official_url": "https://pmsma.nhp.gov.in",
        "verification_date": "2026-10-20",
        "source": "MoHFW & National Health Portal",
        "tags": "pregnancy, anc, antenatal care, high risk pregnancy, ultrasound, free checkup, pmsma"
    },
    {
        "code": "MISSION-INDRA-DHANUSH",
        "name": "Intensified Mission Indradhanush (IMI)",
        "name_hindi": "सघन मिशन इन्द्रधनुष",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Health and Family Welfare",
        "category": "Health & Wellness",
        "target_audience": "Children up to 2 years of age and pregnant women who missed routine immunization doses",
        "short_description": "Free vaccination against 12 vaccine-preventable life-threatening diseases for pregnant women and children up to 2 years.",
        "full_description": "Mission Indradhanush aims to ensure full immunization with all available vaccines for children up to two years of age and pregnant women in underserved, remote, and tribal areas. Protects against 12 life-threatening diseases including Diphtheria, Pertussis, Tetanus, Polio, Measles, Rubella, and Hepatitis B.",
        "benefits": "100% free immunization covering BCG, OPV, Pentavalent, Rotavirus, PCV, MR, and Td vaccines. Prevents childhood mortality and chronic disability.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 5,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Children from birth up to 5 years of age who have dropped out or missed routine immunization doses.",
                "Pregnant women needing Tetanus and adult Diphtheria (Td) immunization.",
                "No income or category restriction."
            ]
        },
        "required_documents": [
            "Mother & Child Protection (MCP) / Immunization Card",
            "Aadhaar Card of Parent (optional, no child denied for lack of ID)"
        ],
        "application_process": "Approach local Anganwadi centre, Village Health Sanitation and Nutrition Day (VHSND) session, or public dispensary during special IMI rounds.",
        "official_url": "https://nhm.gov.in/index1.php?lang=1&level=2&sublinkid=824&lid=220",
        "verification_date": "2026-10-20",
        "source": "Universal Immunization Programme (UIP) & MoHFW",
        "tags": "vaccination, immunization, child health, polio, measles, infant care, mission indradhanush"
    }
]

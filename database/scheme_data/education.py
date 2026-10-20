"""
Education & Scholarship Schemes Dataset (Verified Official Data)
Sources: National Scholarship Portal (scholarships.gov.in), Ministry of Social Justice and Empowerment,
Ministry of Tribal Affairs, Ministry of Education, AICTE, DST.
"""

EDUCATION_SCHEMES = [
    {
        "code": "NSP-POSTMATRIC-SC",
        "name": "Post-Matric Scholarship for SC Students (PMS-SC)",
        "name_hindi": "अनुसूचित जाति के छात्रों के लिए मैट्रिक उपरांत छात्रवृत्ति",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Social Justice and Empowerment",
        "category": "Education & Learning",
        "target_audience": "Scheduled Caste (SC) students studying at post-matriculation or post-secondary stages",
        "short_description": "Full compulsory non-refundable tuition fees and annual maintenance allowance up to ₹13,500 transferred directly via DBT.",
        "full_description": "Centrally sponsored scheme providing financial assistance to Scheduled Caste students studying at post-matriculation or post-secondary stage to enable them to complete their education. Covers full academic fees and monthly maintenance allowances according to course groupings (Group 1 to 4).",
        "benefits": "100% reimbursement of compulsory non-refundable fees (tuition, library, exam fees) directly to institution, plus annual academic maintenance allowance ranging from ₹4,000 to ₹13,500 per year directly to student's Aadhaar-seeded bank account.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 14,
            "max_age": 35,
            "max_annual_income": 250000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["SC"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must belong to Scheduled Caste (SC) community.",
                "Total family income from all sources must not exceed ₹2.50 Lakh per annum.",
                "Student must have passed Matriculation / Class 10 and be enrolled in a recognized post-secondary course in an accredited college/university.",
                "Must not be recipient of any other central/state government scholarship."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Valid Caste Certificate issued by Competent Authority",
            "Current Income Certificate (less than 1 year old)",
            "Class 10 / Previous Academic Marksheet",
            "College/University Fee Receipt and Admission Letter",
            "Bank Account Passbook (Aadhaar linked)"
        ],
        "application_process": "1. Register on National Scholarship Portal (scholarships.gov.in) with OTR (One-Time Registration). 2. Submit PMS-SC application with academic and fee details. 3. Verification by Institution Nodal Officer (INO). 4. Verification by District/State Nodal Officer and DBT disbursement.",
        "official_url": "https://scholarships.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Scholarship Portal (scholarships.gov.in) & MoSJE",
        "tags": "scholarship, sc, post matric, college, university, fees, maintenance allowance, nsp"
    },
    {
        "code": "NSP-POSTMATRIC-OBC",
        "name": "Post-Matric Scholarship for OBC / EBC / DNT Students",
        "name_hindi": "अन्य पिछड़ा वर्ग (ओबीसी) के छात्रों के लिए मैट्रिक उपरांत छात्रवृत्ति",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Social Justice and Empowerment",
        "category": "Education & Learning",
        "target_audience": "Other Backward Class (OBC), Economically Backward Class (EBC), and De-Notified Tribes (DNT) students in post-matric studies",
        "short_description": "Financial assistance covering college tuition fees and study maintenance allowance up to ₹10,000 per year.",
        "full_description": "Centrally sponsored scheme to provide financial assistance to OBC, EBC, and DNT students studying at post-matriculation or post-secondary stage. Aimed at substantially increasing Gross Enrolment Ratio (GER) of disadvantaged backward classes in higher education.",
        "benefits": "Maintenance allowance up to ₹10,000 per annum for hostellers (₹5,000 for day scholars) along with reimbursement of mandatory non-refundable study fees charged by recognized institutions.",
        "max_benefit_amount": 35000,
        "eligibility_criteria": {
            "min_age": 15,
            "max_age": 35,
            "max_annual_income": 250000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["OBC", "General"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must belong to OBC (Non-Creamy Layer), EBC, or DNT category.",
                "Total annual parental/family income must not exceed ₹2.50 Lakh.",
                "Enrolled in recognized undergraduate, postgraduate, diploma, or professional courses."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "OBC Non-Creamy Layer / EBC Caste Certificate",
            "Income Certificate issued by Tehsildar / Sub-Divisional Magistrate",
            "Previous Class Marksheet",
            "College Fee Structure & Admission Receipt",
            "Bank Account Passbook"
        ],
        "application_process": "1. Apply via National Scholarship Portal (scholarships.gov.in). 2. Complete institute level e-verification. 3. District Welfare Officer approval. 4. DBT payment directly to student account.",
        "official_url": "https://scholarships.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Scholarship Portal (scholarships.gov.in) & MoSJE",
        "tags": "scholarship, obc, ebc, non creamy layer, higher education, college fees, maintenance"
    },
    {
        "code": "NSP-POSTMATRIC-ST",
        "name": "Post-Matric Scholarship for ST Students (PMS-ST)",
        "name_hindi": "अनुसूचित जनजाति के छात्रों के लिए मैट्रिक उपरांत छात्रवृत्ति",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Tribal Affairs",
        "category": "Education & Learning",
        "target_audience": "Scheduled Tribe (ST) students pursuing recognized post-secondary education",
        "short_description": "Complete tuition fee coverage and monthly maintenance allowance up to ₹1,200/month for tribal students in higher education.",
        "full_description": "Centrally sponsored scheme dedicated to tribal youth to support higher educational pursuits from class 11 through post-graduate and doctorate levels. Eliminates economic hurdles for ST youth across India.",
        "benefits": "100% compulsory tuition fee reimbursement directly to institution, plus maintenance allowance up to ₹1,200/month (hosteller) and ₹550/month (day scholar), book grants, and study tour allowances.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 14,
            "max_age": 35,
            "max_annual_income": 250000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["ST"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Tribal", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must belong to a notified Scheduled Tribe (ST).",
                "Total annual family income must not exceed ₹2,50,000.",
                "Studying in a recognized government or private UGC/AICTE approved educational institution."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Scheduled Tribe (ST) Certificate",
            "Annual Family Income Certificate",
            "Fee receipt and Institute Verification form",
            "Bank Passbook seeded with Aadhaar"
        ],
        "application_process": "1. Register on NSP (scholarships.gov.in). 2. Submit PMS-ST application. 3. College verification through INO login. 4. State Tribal Welfare Department approves and sanctions funds via DBT.",
        "official_url": "https://tribal.nic.in",
        "verification_date": "2026-10-20",
        "source": "National Scholarship Portal & Ministry of Tribal Affairs",
        "tags": "scholarship, tribal, st, higher education, college, tribal welfare, fees"
    },
    {
        "code": "NSP-NMMSS",
        "name": "National Means-cum-Merit Scholarship Scheme (NMMSS)",
        "name_hindi": "राष्ट्रीय साधन-सह-योग्यता छात्रवृत्ति योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Education",
        "category": "Education & Learning",
        "target_audience": "Meritorious students of economically weaker sections studying in Class 9 to 12 in Government/Local Body schools",
        "short_description": "₹12,000 per annum (₹1,000 per month) scholarship from Class 9 to 12 to arrest school dropout rates after elementary level.",
        "full_description": "Centrally sponsored scheme launched by Department of School Education and Literacy to award 100,000 scholarships each year to meritorious students of economically weaker sections to arrest dropouts at class 8 and encourage continuation of secondary education.",
        "benefits": "₹12,000 per annum (₹1,000/month) transferred directly to student's bank account via DBT from Class 9 to Class 12 (4 continuous years upon satisfactory academic renewal).",
        "max_benefit_amount": 12000,
        "eligibility_criteria": {
            "min_age": 12,
            "max_age": 18,
            "max_annual_income": 350000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Student must have scored minimum 55% marks (50% for SC/ST) in Class 7 examination.",
                "Total annual parental income must not exceed ₹3,50,000.",
                "Must qualify the state-level NMMSS selection test conducted in Class 8.",
                "Must be studying in Government, Local Body, or Government-aided school (KVS, NVS, and private residential schools are excluded)."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Class 7 & Class 8 Marksheet",
            "NMMSS Selection Examination Merit Roll Card",
            "Parental Income Certificate",
            "Bonafide Student Certificate from School Headmaster",
            "Bank Account Passbook in student's name"
        ],
        "application_process": "1. Appear and qualify State-level NMMSS written test. 2. Register on National Scholarship Portal (scholarships.gov.in). 3. School Headmaster verifies enrollment in Class 9. 4. Yearly renewal on NSP on scoring minimum 55% in subsequent classes.",
        "official_url": "https://scholarships.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Scholarship Portal & Department of School Education and Literacy",
        "tags": "school scholarship, nmmss, merit scholarship, class 9 to 12, dropout prevention, dbt"
    },
    {
        "code": "PM-YASASVI",
        "name": "PM Young Achievers Scholarship Award Scheme for Vibrant India (PM-YASASVI)",
        "name_hindi": "पीएम यशस्वी छात्रवृत्ति योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Social Justice and Empowerment",
        "category": "Education & Learning",
        "target_audience": "OBC, EBC, and DNT students studying in Class 9, 10, 11, and 12 in Top Class identified schools",
        "short_description": "Scholarship of ₹75,000 per year for Class 9-10 and ₹1,25,000 per year for Class 11-12 covering school tuition and hostel fees.",
        "full_description": "PM-YASASVI is an umbrella scheme by MoSJE for Other Backward Classes (OBC), Economically Backward Classes (EBC), and De-Notified Nomadic Tribes (DNT). It offers top-class school education scholarships covering full school tuition, hostel, and study material fees.",
        "benefits": "₹75,000 per annum for Class 9 and 10 students; ₹1,25,000 per annum for Class 11 and 12 students studying in identified top-class schools across India.",
        "max_benefit_amount": 125000,
        "eligibility_criteria": {
            "min_age": 13,
            "max_age": 20,
            "max_annual_income": 250000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["OBC", "General"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must belong to OBC, EBC, or DNT category.",
                "Annual family income must not exceed ₹2.50 Lakh.",
                "Must be studying in one of the identified Top Class Schools listed on the YASASVI portal."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Caste Certificate (OBC/EBC/DNT)",
            "Parental Income Certificate",
            "Previous Class Marksheet",
            "School Bonafide Certificate",
            "Bank Account Details"
        ],
        "application_process": "1. Apply online on National Scholarship Portal under PM-YASASVI Top Class School Education. 2. Selection based on merit / qualifying criteria. 3. School e-verification and DBT payment.",
        "official_url": "https://yet.nta.ac.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & MoSJE",
        "tags": "yasasvi, obc scholarship, top class school, school education, class 9 to 12, merit award"
    },
    {
        "code": "CSSS",
        "name": "Central Sector Scheme of Scholarship for College and University Students (CSSS)",
        "name_hindi": "कॉलेज और विश्वविद्यालय के छात्रों के लिए केंद्रीय क्षेत्र छात्रवृत्ति योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Education",
        "category": "Education & Learning",
        "target_audience": "Meritorious students who have completed Class 12 in top 20th percentile and enrolled in regular degree courses",
        "short_description": "₹12,000 per year for 3 years of graduation and ₹20,000 per year for post-graduation degree studies.",
        "full_description": "Department of Higher Education scheme to provide financial assistance to meritorious students from low-income families to meet day-to-day expenses while pursuing higher studies in college and universities. 82,000 fresh scholarships awarded each year (50% reserved for girls).",
        "benefits": "₹12,000 per annum for the first three years of undergraduate degree; ₹20,000 per annum at the postgraduate level. For 5-year integrated professional courses, ₹20,000/year paid in 4th and 5th year.",
        "max_benefit_amount": 20000,
        "eligibility_criteria": {
            "min_age": 17,
            "max_age": 25,
            "max_annual_income": 450000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Student must be above the 80th percentile of successful candidates in the relevant stream in Class 12 from state/central board.",
                "Must be pursuing regular (non-correspondence/distance) degree course recognized by AIU/UGC/AICTE.",
                "Total parental annual income must not exceed ₹4.50 Lakh.",
                "Must not be in receipt of any other scholarship."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Class 12 Board Marksheet & Certificate",
            "Income Certificate issued by Revenue Authority",
            "College Admission Slip & Bonafide Certificate",
            "Aadhaar-seeded Bank Account Passbook"
        ],
        "application_process": "1. Apply on NSP (scholarships.gov.in). 2. System verifies Class 12 board roll number and percentile automatically. 3. College verification. 4. Direct DBT payment to student account.",
        "official_url": "https://scholarships.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Scholarship Portal & Department of Higher Education",
        "tags": "scholarship, college, university, graduation, merit scholarship, csss, higher education"
    },
    {
        "code": "AICTE-PRAGATI",
        "name": "AICTE Pragati Scholarship Scheme for Girl Students",
        "name_hindi": "एआईसीटीई प्रगति छात्रवृत्ति योजना (छात्राओं हेतु)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Education",
        "category": "Education & Learning",
        "target_audience": "Girl students admitted to first year or second year (lateral entry) of technical degree or diploma courses",
        "short_description": "₹50,000 per year for every year of technical study (Degree or Diploma) to empower girl students in STEM and engineering.",
        "full_description": "Implemented by All India Council for Technical Education (AICTE) to provide assistance for advancement of girls pursuing technical education. Covers up to 10,000 scholarships annually across degree and diploma engineering programmes.",
        "benefits": "₹50,000 per annum for every year of study (maximum 4 years for degree and 3 years for diploma) paid as a lump-sum amount towards college fees, computer purchase, books, and equipment.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 16,
            "max_age": 28,
            "max_annual_income": 800000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Candidate must be female.",
                "Admitted to 1st year of Degree/Diploma course OR 2nd year of Degree/Diploma through lateral entry in an AICTE approved institution.",
                "Maximum two girl children per family eligible.",
                "Total family income from all sources must be less than ₹8 Lakh per annum."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Class 10 & 12 Marksheets / Diploma Marksheet",
            "Central/State admission seat allotment letter for engineering/polytechnic",
            "Tuition fee receipt",
            "Family Income Certificate (below ₹8 Lakh)",
            "Affidavit declaring only up to 2 girl children in family availing benefit"
        ],
        "application_process": "1. Apply via National Scholarship Portal (scholarships.gov.in). 2. Institute Nodal Officer e-verifies enrolment in AICTE approved programme. 3. AICTE releases ₹50,000 directly to student bank account via DBT.",
        "official_url": "https://www.aicte-india.org/schemes/students-development-schemes/pragati",
        "verification_date": "2026-10-20",
        "source": "AICTE Official Portal & National Scholarship Portal",
        "tags": "aicte, pragati, girl student, engineering, diploma, polytechnic, stem, technical education"
    },
    {
        "code": "AICTE-SAKSHAM",
        "name": "AICTE Saksham Scholarship Scheme for Differently Abled Students",
        "name_hindi": "एआईसीटीई सक्षम छात्रवृत्ति योजना (दिव्यांग छात्रों हेतु)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Education",
        "category": "Education & Learning",
        "target_audience": "Specially-abled students with disability not less than 40% studying technical degree or diploma courses",
        "short_description": "₹50,000 per year scholarship for every year of technical study for differently-abled students in AICTE colleges.",
        "full_description": "AICTE initiative aimed at providing encouragement and support to specially abled children to pursue technical education. Provides all eligible applicants with financial support to purchase books, software, assistive devices, and meet educational expenses.",
        "benefits": "₹50,000 per annum for the entire duration of the course (4 years for Degree, 3 years for Diploma) credited directly into Aadhaar-linked bank account.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 16,
            "max_age": 35,
            "max_annual_income": 800000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must possess a valid Disability Certificate with disability percentage of 40% or more.",
                "Enrolled in 1st year or 2nd year (lateral entry) in AICTE approved technical institution.",
                "Total annual family income must not exceed ₹8.00 Lakh."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Unique Disability ID (UDID) Card / Medical Board Disability Certificate (>=40%)",
            "Class 10 and 12 marksheet",
            "Course admission allotment letter and fee receipt",
            "Family Income Certificate",
            "Bank Passbook"
        ],
        "application_process": "1. Submit application on National Scholarship Portal. 2. College verification of technical course admission. 3. AICTE verification and DBT sanction.",
        "official_url": "https://www.aicte-india.org",
        "verification_date": "2026-10-20",
        "source": "AICTE Official Portal & National Scholarship Portal",
        "tags": "saksham, differently abled, divyang, disability, engineering, aicte, technical education"
    },
    {
        "code": "BEGUM-HAZRAT",
        "name": "Begum Hazrat Mahal National Scholarship for Minority Girls",
        "name_hindi": "बेगम हज़रत महल राष्ट्रीय छात्रवृत्ति योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Minority Affairs",
        "category": "Education & Learning",
        "target_audience": "Meritorious girl students belonging to notified minority communities studying in Class 9 to 12",
        "short_description": "Financial scholarship of ₹5,000 to ₹6,000 per year for minority girl students studying in Classes 9 through 12.",
        "full_description": "Implemented by Maulana Azad Education Foundation / Ministry of Minority Affairs to support meritorious girl students belonging to six notified minority communities (Muslims, Christians, Sikhs, Buddhists, Jains, and Parsis) who cannot continue their education due to financial distress.",
        "benefits": "₹5,000 per year for Class 9 and 10; ₹6,000 per year for Class 11 and 12, transferred via DBT into student's bank account.",
        "max_benefit_amount": 6000,
        "eligibility_criteria": {
            "min_age": 13,
            "max_age": 19,
            "max_annual_income": 200000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["Minority"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Only girl students belonging to six notified minority communities are eligible.",
                "Must have secured minimum 50% aggregate marks in the qualifying previous class.",
                "Total annual parental/guardian income must not exceed ₹2,00,000.",
                "Maximum 2 girls from the same family eligible."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Self-declaration / Certificate of Minority Community",
            "Previous Class Marksheet with minimum 50% marks",
            "Income Certificate issued by Competent Authority",
            "School Verification Certificate signed by Principal",
            "Bank Passbook in student's name"
        ],
        "application_process": "1. Apply online on National Scholarship Portal. 2. Upload minority declaration and income proof. 3. School head verification. 4. DBT payment release.",
        "official_url": "https://scholarships.gov.in",
        "verification_date": "2026-10-20",
        "source": "National Scholarship Portal & Ministry of Minority Affairs",
        "tags": "minority, girl scholarship, begum hazrat mahal, class 9 to 12, education support"
    },
    {
        "code": "PMRF",
        "name": "Prime Minister's Research Fellowship (PMRF)",
        "name_hindi": "प्रधानमंत्री अनुसंधान फेलोशिप",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Education",
        "category": "Education & Learning",
        "target_audience": "High-merit Ph.D. scholars in STEM disciplines at IITs, IISc, IISERs, and central universities",
        "short_description": "Prestige research fellowship of ₹70,000 to ₹80,000 per month plus an annual contingency research grant of ₹2 Lakh.",
        "full_description": "Designed for improving the quality of research in higher educational institutions in the country. Attracts the best talent into research in frontier science and technology areas at premier institutions like IITs, IISc Bangalore, IISERs, and top Central Universities.",
        "benefits": "Monthly fellowship of ₹70,000/month (Year 1 & 2), ₹75,000/month (Year 3), and ₹80,000/month (Year 4 & 5), alongside an annual contingency grant of ₹2,00,000 per fellow for research and conference travel.",
        "max_benefit_amount": 960000,
        "eligibility_criteria": {
            "min_age": 21,
            "max_age": 35,
            "max_annual_income": None,
            "eligible_occupations": ["Student", "Ph.D. Scholar", "Researcher"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be admitted to Ph.D. programme in a PMRF granting institution (Direct Entry or Lateral Entry).",
                "For direct entry: B.Tech/M.Tech with CGPA >= 8.0 or top GATE score.",
                "For lateral entry: Completed 12 to 24 months of Ph.D. with minimum CGPA 8.5 and published research."
            ]
        },
        "required_documents": [
            "Academic transcripts (Undergraduate & Postgraduate)",
            "GATE / CEED / CSIR-NET scorecard (if applicable)",
            "Research Project Proposal / Abstract",
            "Letter of recommendation from Ph.D. guide/department",
            "Institutional nomination document"
        ],
        "application_process": "1. Institution nominates candidate via PMRF National Portal (pmrf.in). 2. National Review Committee evaluates research proposal and publications. 3. Fellowship awarded by National Steering Committee.",
        "official_url": "https://www.pmrf.in",
        "verification_date": "2026-10-20",
        "source": "PMRF National Portal (pmrf.in) & Ministry of Education",
        "tags": "phd, doctoral fellowship, research grant, iit, iisc, science, stem, pmrf"
    },
    {
        "code": "INSPIRE-SHE",
        "name": "INSPIRE Scholarship for Higher Education (SHE)",
        "name_hindi": "इंस्पायर उच्च शिक्षा छात्रवृत्ति योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Science and Technology",
        "category": "Education & Learning",
        "target_audience": "Top 1% Class 12 students pursuing undergraduate and postgraduate education in Natural and Basic Sciences",
        "short_description": "₹80,000 per annum scholarship (₹60,000 cash + ₹20,000 summer mentorship project grant) for 5 years in B.Sc. and M.Sc.",
        "full_description": "Innovation in Science Pursuit for Inspired Research (INSPIRE) is a flagship programme by Department of Science & Technology (DST). The SHE component offers 12,000 scholarships annually to attract youth towards studying basic and natural sciences at university level.",
        "benefits": "Total value of ₹80,000 per annum: ₹60,000 scholarship (₹5,000/month credited annually) plus ₹20,000 mentorship grant for mandatory summer research project under certified scientist.",
        "max_benefit_amount": 80000,
        "eligibility_criteria": {
            "min_age": 17,
            "max_age": 22,
            "max_annual_income": None,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Student must rank within the top 1% cut-off in their Class 12 board examination.",
                "OR qualify within top 10,000 ranks in JEE / NEET and choose B.Sc., B.S., or Integrated M.Sc. in basic sciences.",
                "Eligible disciplines: Physics, Chemistry, Mathematics, Biology, Statistics, Geology, Astrophysics, Botany, Zoology."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Class 12 Board Marksheet & INSPIRE Board Advisory / Cut-off Certificate",
            "Endorsement Certificate signed by College Principal / University Registrar",
            "Aadhaar-linked SBI Bank Passbook"
        ],
        "application_process": "1. Apply online on INSPIRE web portal (online-inspire.gov.in). 2. Upload endorsement certificate and Class 12 marksheets. 3. DST scrutinizes applications and issues conditional offer letter. 4. Release of ₹80,000/year upon passing examinations with 60% marks.",
        "official_url": "https://online-inspire.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Science and Technology (DST) INSPIRE Portal",
        "tags": "inspire, basic sciences, bsc, msc, dst, research scholarship, natural sciences"
    },
    {
        "code": "NAPS",
        "name": "National Apprenticeship Promotion Scheme (NAPS)",
        "name_hindi": "राष्ट्रीय शिक्षुता प्रोत्साहन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Skill Development and Entrepreneurship",
        "category": "Employment & Skill Development",
        "target_audience": "Youth who have completed ITI, Diploma, Graduate, or 10th/12th looking for industrial on-the-job apprenticeship",
        "short_description": "Government pays 25% of prescribed monthly stipend (up to ₹1,500/month) directly via DBT to apprentices undergoing industrial training.",
        "full_description": "NAPS aims to promote apprenticeship training in establishments by providing financial support to both employers and apprentices. Apprentices receive monthly stipends while gaining real-world industry work experience across manufacturing, automotive, IT, and service sectors.",
        "benefits": "Government transfers 25% of the stipend payable up to ₹1,500 per month directly to the apprentice's bank account via DBT, while the employer pays the remaining stipend (minimum total ₹7,000 to ₹10,000/month). Apprenticeship certificate issued by NCVET upon completion.",
        "max_benefit_amount": 18000,
        "eligibility_criteria": {
            "min_age": 14,
            "max_age": 35,
            "max_annual_income": None,
            "eligible_occupations": ["Student", "Job Seeker", "ITI Graduate", "Diploma Holder"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be at least 14 years of age (18 years for designated hazardous trades).",
                "Must meet minimum educational qualifications prescribed for the trade (e.g. 10th pass, ITI, or graduate).",
                "Must not have undergone an apprenticeship training contract previously in the same trade."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Educational Certificates (10th/12th/ITI/Degree/Diploma)",
            "Bank Account Passbook (Aadhaar Seeded for DBT)",
            "Passport Size Photograph"
        ],
        "application_process": "1. Register as a Candidate on Apprenticeship Portal (apprenticeshipindia.gov.in). 2. Complete e-KYC with Aadhaar. 3. Search and apply for apprenticeship vacancies posted by establishments. 4. Sign apprenticeship contract digitally.",
        "official_url": "https://www.apprenticeshipindia.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Skill Development & Entrepreneurship (MSDE)",
        "tags": "apprenticeship, naps, industrial training, stipend, iti, skill development, job training"
    }
]

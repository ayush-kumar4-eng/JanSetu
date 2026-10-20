"""
Flagship State Government Schemes Dataset (Verified Official Data)
Sources: Official State Portals (Rajasthan, Maharashtra, UP, MP, Karnataka, Tamil Nadu, West Bengal, Bihar, Odisha, Delhi, Gujarat).
"""

STATE_SCHEMES = [
    # ------------------- RAJASTHAN -------------------
    {
        "code": "RJ-CHIRANJEEVI",
        "name": "Mukhyamantri Ayushman Arogya Yojana (Formerly Chiranjeevi Health Scheme)",
        "name_hindi": "मुख्यमंत्री आयुष्मान आरोग्य योजना (चिरंजीवी)",
        "level": "State",
        "state": "Rajasthan",
        "ministry": "Medical, Health & Family Welfare Department, Rajasthan",
        "category": "Health & Wellness",
        "target_audience": "All permanent resident families of Rajasthan with Jan Aadhaar Card",
        "short_description": "Universal cashless healthcare cover of up to ₹25 Lakh per family per year in empaneled public and private hospitals.",
        "full_description": "Rajasthan's flagship universal healthcare assurance scheme providing cashless hospital treatment. Eligible categories (NFSA, SECC, small/marginal farmers, contractual workers, destitute) receive 100% free premium from the state, while other families can enroll by paying a nominal premium of ₹850 per year.",
        "benefits": "Cashless hospitalization treatment up to ₹25,00,000 per family per year covering complex tertiary surgeries (organ transplants, cancer therapy, cardiovascular surgery). Additional accidental insurance cover up to ₹10,00,000.",
        "max_benefit_amount": 2500000,
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
                "Must be a bonafide resident of Rajasthan possessing a Jan Aadhaar Card / Jan Aadhaar Enrolment Slip.",
                "Free coverage for NFSA, BPL, small/marginal farmers, Covid-19 ex-gratia recipients, and contractual government workers.",
                "All other resident families can avail benefits by paying ₹850/year premium."
            ]
        },
        "required_documents": [
            "Jan Aadhaar Card / Jan Aadhaar Registration Slip",
            "Aadhaar Card",
            "Category Proof (Ration card / farmer certificate for free category)"
        ],
        "application_process": "1. Visit chiranjeevi.rajasthan.gov.in or nearest E-Mitra kiosk. 2. Authenticate using Jan Aadhaar ID. 3. Free for eligible categories or pay ₹850 premium. 4. Avail cashless admission at any empaneled hospital using Jan Aadhaar.",
        "official_url": "https://chiranjeevi.rajasthan.gov.in",
        "verification_date": "2026-10-20",
        "source": "State Health Agency, Govt. of Rajasthan (chiranjeevi.rajasthan.gov.in)",
        "tags": "chiranjeevi, rajasthan health, ayushman arogya, 25 lakh health cover, jan aadhaar, emitra"
    },
    {
        "code": "RJ-PALANHAR",
        "name": "Palanhar Yojana Rajasthan",
        "name_hindi": "पालनहार योजना राजस्थान",
        "level": "State",
        "state": "Rajasthan",
        "ministry": "Social Justice and Empowerment Department, Rajasthan",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Foster parents and caretakers nurturing orphan children, children of destitute/disabled parents, or life prisoners",
        "short_description": "Monthly financial assistance of ₹1,500 (age 0-6) and ₹2,500 (age 6-18) plus an annual clothing grant of ₹2,000 per child.",
        "full_description": "Palanhar Yojana aims to ensure that orphan children, children of widowed mothers, divorcee women, leprosy patients, and life convict prisoners are nurtured within a family environment rather than being sent to orphanages. The caregiver (Palanhar) receives regular monthly financial aid directly via DBT.",
        "benefits": "Monthly grant of ₹1,500 per child for children aged 0 to 6 years attending Anganwadi; and ₹2,500 per child per month for school-going children aged 6 to 18 years. Additional annual lump-sum grant of ₹2,000 per child for uniforms, textbooks, and shoes.",
        "max_benefit_amount": 32000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 18,
            "max_annual_income": 120000,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Caregiver and child must be bonafide residents of Rajasthan.",
                "Annual family income of the Palanhar family must not exceed ₹1.20 Lakh (waived for pure orphans).",
                "Mandatory enrollment: Child aged 2-6 years must attend Anganwadi; child aged 6-18 must be enrolled in a recognized school."
            ]
        },
        "required_documents": [
            "Jan Aadhaar Card",
            "Death Certificate of parents (for orphans) / Disability Certificate / Imprisonment order",
            "School / Anganwadi attendance bonafide certificate",
            "Income Certificate of Palanhar caregiver",
            "Bank Account Passbook (Aadhaar linked)"
        ],
        "application_process": "1. Apply via SSO Rajasthan (sso.rajasthan.gov.in) or E-Mitra kiosk. 2. Upload supporting category proof and school certificate. 3. Verification by Block Development Officer / Social Welfare Officer. 4. Monthly DBT to Palanhar bank account.",
        "official_url": "https://sje.rajasthan.gov.in/Schemes_Palanhar.aspx",
        "verification_date": "2026-10-20",
        "source": "Social Justice and Empowerment Department, Govt. of Rajasthan",
        "tags": "palanhar, orphan support, foster care, child allowance, rajasthan welfare, jan aadhaar"
    },
    {
        "code": "RJ-ANNAPURNA",
        "name": "Shri Annapurna Rasoi Yojana (Formerly Indira Rasoi)",
        "name_hindi": "श्री अन्नपूर्णा रसोई योजना",
        "level": "State",
        "state": "Rajasthan",
        "ministry": "Local Self Government Department, Rajasthan",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Any citizen, daily wage laborer, student, or patient attendant in urban and semi-urban Rajasthan",
        "short_description": "Wholesome, hygienic, freshly prepared hot meal of 600 grams for just ₹8 per plate.",
        "full_description": "Operated with the vision 'Koi Bhukha Na Soye' (No one should sleep hungry), Annapurna Rasois provide fresh, nutritious meals at subsidized rates through permanent dining centres across municipal corporations, railway stations, and hospital complexes in Rajasthan. State Govt contributes ₹22 subsidy per thali.",
        "benefits": "Full nutritious meal (100g dal, 100g seasonal vegetable, 300g chapatis, and pickle/millets) at an affordable cost of only ₹8 to the citizen.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All", "Daily Wage Earner", "Student", "Labourer", "Driver"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Open to all individuals without any income, residence, or category restrictions.",
                "Service timings: Lunch from 8:30 AM to 3:00 PM; Dinner from 6:00 PM to 9:30 PM."
            ]
        },
        "required_documents": [
            "Aadhaar Card / Jan Aadhaar Card / Any Government ID (for nominal coupon generation)"
        ],
        "application_process": "Walk into any Annapurna Rasoi center across urban Rajasthan. Pay ₹8 cash or UPI at the billing counter and receive meal token.",
        "official_url": "https://indirarasoi.rajasthan.gov.in",
        "verification_date": "2026-10-20",
        "source": "Local Self Government Department, Rajasthan",
        "tags": "annapurna rasoi, indira rasoi, 8 rupee meal, subsidized food, rajasthan, daily wage worker"
    },
    {
        "code": "RJ-YUVA-SAMBAL",
        "name": "Mukhyamantri Yuva Sambal Yojana (MYSY)",
        "name_hindi": "मुख्यमंत्री युवा संबल योजना",
        "level": "State",
        "state": "Rajasthan",
        "ministry": "Department of Skill, Employment and Entrepreneurship, Rajasthan",
        "category": "Employment & Skill Development",
        "target_audience": "Unemployed graduates residing in Rajasthan seeking career transition and internships",
        "short_description": "Unemployment allowance of ₹4,000/month (male) and ₹4,500/month (female/divyang) for up to 2 years with skill internship.",
        "full_description": "Provides financial subsistence to unemployed educated youth in Rajasthan for a maximum duration of two years or until gaining employment. Beneficiaries undergo 3 months of certified skill training and undertake 4 hours daily of government department internship.",
        "benefits": "Monthly allowance of ₹4,000 for male candidates and ₹4,500 for female, transgender, and specially-abled (Divyangjan) candidates for up to 24 months via DBT.",
        "max_benefit_amount": 108000,
        "eligibility_criteria": {
            "min_age": 21,
            "max_age": 30,
            "max_annual_income": 200000,
            "eligible_occupations": ["Unemployed Youth", "Graduate"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a graduate from a recognized university located in Rajasthan (or domicile women married in Rajasthan).",
                "Age limit: 21 to 30 years for General males; up to 35 years for SC, ST, OBC, Women, and Divyangjan.",
                "Total annual family income must not exceed ₹2,00,000.",
                "Mandatory 4-hour daily internship in designated government offices."
            ]
        },
        "required_documents": [
            "Jan Aadhaar Card",
            "Degree Graduation Marksheet / Certificate",
            "Domicile / Bonafide Resident Certificate of Rajasthan",
            "Self-declaration of unemployment",
            "Income Certificate"
        ],
        "application_process": "1. Register on Rajasthan Employment Exchange portal (employment.livelihoods.rajasthan.gov.in). 2. Submit MYSY application with graduation documents. 3. Allocation of internship department. 4. Monthly allowance credited via DBT on monthly attendance verification.",
        "official_url": "https://employment.livelihoods.rajasthan.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Skill, Employment & Entrepreneurship, Govt. of Rajasthan",
        "tags": "yuva sambal, unemployment allowance, rajasthan youth, graduate stipend, berojgari bhatta"
    },
    {
        "code": "RJ-ANUPRITI",
        "name": "Mukhyamantri Anupriti Coaching Yojana",
        "name_hindi": "मुख्यमंत्री अनुप्रति कोचिंग योजना",
        "level": "State",
        "state": "Rajasthan",
        "ministry": "Social Justice and Empowerment Department, Rajasthan",
        "category": "Education & Learning",
        "target_audience": "Meritorious students from SC, ST, OBC, MBC, EWS, and Minority communities preparing for professional entrance exams",
        "short_description": "100% free coaching at premier institutes for UPSC, RAS, NEET, JEE, CLAT, CA, REET + ₹40,000 annual boarding grant.",
        "full_description": "Provides free competitive examination coaching to meritorious students from underprivileged backgrounds for premier exams (UPSC Civil Services, RPSC RAS, NEET, IIT-JEE, CA-FC, CS, CLAT, Bank PO, and Sub-Inspector). 30,000 seats allocated annually across Rajasthan.",
        "benefits": "Full course coaching fee borne directly by the state government to empaneled institutes (Allen, Utkarsh, Drishti IAS, etc.), plus an additional annual boarding and lodging grant of ₹40,000 for students living away from their home town for coaching.",
        "max_benefit_amount": 100000,
        "eligibility_criteria": {
            "min_age": 16,
            "max_age": 28,
            "max_annual_income": 800000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["SC", "ST", "OBC", "MBC", "EWS", "Minority"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be a permanent resident of Rajasthan.",
                "Belonging to SC, ST, OBC, MBC, EWS, or Minority communities.",
                "Total annual family income must not exceed ₹8.00 Lakh (or parents are state govt employees in Pay Matrix Level 11).",
                "Selection based on 10th and 12th board merit percentages."
            ]
        },
        "required_documents": [
            "Jan Aadhaar Card",
            "Caste Certificate (SC/ST/OBC/EWS)",
            "Class 10 and 12 Marksheets",
            "Income Certificate (under ₹8 Lakh)",
            "Domicile Certificate"
        ],
        "application_process": "1. Apply via SSO Rajasthan portal (sso.rajasthan.gov.in) under SJMS application. 2. Select desired examination and preferred coaching institute. 3. Merit list released based on board marks. 4. Admission granted without any out-of-pocket tuition fees.",
        "official_url": "https://sje.rajasthan.gov.in",
        "verification_date": "2026-10-20",
        "source": "Social Justice and Empowerment Department, Rajasthan",
        "tags": "anupriti, free coaching, upsc, iit jee, neet, rajasthan, ras, competitive exams, sje"
    },

    # ------------------- MAHARASHTRA -------------------
    {
        "code": "MH-LADKI-BAHIN",
        "name": "Mukhyamantri Majhi Ladki Bahin Yojana",
        "name_hindi": "मुख्यमंत्री माझी लाड़की बहिन योजना (महाराष्ट्र)",
        "level": "State",
        "state": "Maharashtra",
        "ministry": "Women and Child Development Department, Maharashtra",
        "category": "Women & Child",
        "target_audience": "Women residents of Maharashtra aged 21 to 65 years from low-income families",
        "short_description": "Direct financial assistance of ₹1,500 per month credited directly into the bank accounts of eligible women.",
        "full_description": "Flagship welfare scheme launched by the Government of Maharashtra to empower women economically and socially, enhance health and nutritional well-being, and support their self-reliance. Beneficiaries receive ₹1,500 monthly via Aadhaar-linked DBT.",
        "benefits": "₹1,500 per month (₹18,000 per year) deposited directly into beneficiary's Aadhaar-linked bank account through direct benefit transfer (DBT).",
        "max_benefit_amount": 18000,
        "eligibility_criteria": {
            "min_age": 21,
            "max_age": 65,
            "max_annual_income": 250000,
            "eligible_occupations": ["All", "Homemaker", "Daily Wage Earner", "Self Employed"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a married, widowed, divorced, deserted, or unmarried destitute woman residing in Maharashtra.",
                "Age must be between 21 and 65 years.",
                "Combined family annual income must not exceed ₹2.50 Lakh (Yellow or Orange Ration Card holders exempted from separate income certificate).",
                "Family members should not be regular/permanent government employees or income tax payers."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Maharashtra Domicile Certificate / 15-year old Ration Card / School Leaving Certificate",
            "Yellow or Orange Ration Card / Income Certificate (below ₹2.5 Lakh)",
            "Aadhaar-seeded Bank Account Passbook",
            "Affidavit / Self-declaration"
        ],
        "application_process": "1. Apply online via Nari Shakti Doot App or ladkibahin.maharashtra.gov.in or visit Setu Suvidha Kendra / Anganwadi. 2. Aadhaar e-KYC authentication. 3. Scrutiny by Ward / Taluka Committee. 4. Monthly DBT disbursement.",
        "official_url": "https://ladkibahin.maharashtra.gov.in",
        "verification_date": "2026-10-20",
        "source": "Women & Child Development Department, Govt. of Maharashtra",
        "tags": "ladki bahin, maharashtra, 1500 monthly, women empowerment, dbt, nari shakti"
    },
    {
        "code": "MH-MPJAY",
        "name": "Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY)",
        "name_hindi": "महात्मा ज्योतिराव फुले जन आरोग्य योजना",
        "level": "State",
        "state": "Maharashtra",
        "ministry": "Public Health Department, Maharashtra",
        "category": "Health & Wellness",
        "target_audience": "All citizens and families holding valid ration cards in Maharashtra",
        "short_description": "Cashless health insurance cover up to ₹5,00,000 per family per year for 1,356 medical and surgical procedures.",
        "full_description": "Pioneering state health assurance initiative integrated with Ayushman Bharat. Provides comprehensive cashless hospital coverage of ₹5 Lakh per family per year across empaneled government and private network hospitals for 1,356 serious medical and surgical therapies.",
        "benefits": "Cashless hospital treatment up to ₹5,00,000 per family per year covering surgeries, ICU, consultations, diagnostics, and medicines. Universalized to cover all ration card holders of Maharashtra.",
        "max_benefit_amount": 500000,
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
                "Must be a resident of Maharashtra holding a valid state ration card (Yellow, Orange, or White) or Annapurna card.",
                "Cashless treatment at any network hospital upon Arogyamitra verification."
            ]
        },
        "required_documents": [
            "Valid Maharashtra Ration Card",
            "Aadhaar Card / Voter ID"
        ],
        "application_process": "Approach Arogyamitra desk at any empaneled government or private hospital with ration card and Aadhaar. Hospital initiates pre-authorization and provides cashless treatment.",
        "official_url": "https://www.jeevandayee.gov.in",
        "verification_date": "2026-10-20",
        "source": "State Health Assurance Society, Govt. of Maharashtra",
        "tags": "mjpjay, maharashtra health, jeevandayee, 5 lakh cover, cashless hospital, arogyamitra"
    },
    {
        "code": "MH-SHETKARI-SANMAN",
        "name": "Namo Shetkari Maha Samman Nidhi Yojana",
        "name_hindi": "नमो शेतकरी महा सम्मान निधि योजना",
        "level": "State",
        "state": "Maharashtra",
        "ministry": "Agriculture Department, Maharashtra",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "All landholding farmer families in Maharashtra receiving PM-KISAN benefits",
        "short_description": "Additional ₹6,000 per year from Maharashtra government, taking total farmer income support to ₹12,000 annually.",
        "full_description": "State top-up scheme for landholder farmers in Maharashtra. In addition to the ₹6,000/year disbursed under PM-KISAN, the Government of Maharashtra contributes an additional ₹6,000 per year in three equal installments of ₹2,000, ensuring eligible farmers receive a combined ₹12,000 annually.",
        "benefits": "₹6,000 per year transferred via DBT in three installments of ₹2,000 each into Aadhaar-seeded bank accounts (complementing ₹6,000 from PM-KISAN = ₹12,000 total).",
        "max_benefit_amount": 6000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 85,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Cultivator"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Farmer must be an approved beneficiary on the PM-KISAN portal in Maharashtra.",
                "Must hold cultivable land in state 7/12 land records.",
                "Bank account must have active Aadhaar seeding and completed e-KYC."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "PM-KISAN Registration Number",
            "7/12 Land Extract and 8-A Certificate",
            "Aadhaar-linked Bank Passbook"
        ],
        "application_process": "Automatic integration for all verified PM-KISAN beneficiaries in Maharashtra. Farmers can check payment status on nskmy.maharashtra.gov.in.",
        "official_url": "https://krishi.maharashtra.gov.in",
        "verification_date": "2026-10-20",
        "source": "Agriculture Department, Govt. of Maharashtra",
        "tags": "namo shetkari, maharashtra farmer, kisan dbt, 6000 extra, pm kisan top up, agri income"
    },

    # ------------------- UTTAR PRADESH -------------------
    {
        "code": "UP-KANYA-SUMANGALA",
        "name": "Mukhyamantri Kanya Sumangala Yojana (MKSY)",
        "name_hindi": "मुख्यमंत्री कन्या सुमंगला योजना (उत्तर प्रदेश)",
        "level": "State",
        "state": "Uttar Pradesh",
        "ministry": "Women and Child Development Department, Uttar Pradesh",
        "category": "Women & Child",
        "target_audience": "Girl children in Uttar Pradesh born in families with annual income up to ₹3 Lakh",
        "short_description": "Cash incentive of ₹25,000 disbursed across 6 developmental milestones from birth to undergraduate admission.",
        "full_description": "Conditional cash transfer scheme by the Uttar Pradesh Government to eliminate female feticide, foster positive attitudes towards the girl child, prevent child marriage, and support higher education. Enhanced to provide ₹25,000 in 6 installments as the girl progresses through birth, vaccination, school admissions, and graduation.",
        "benefits": "Total ₹25,000 cash assistance: Stage 1 (Birth) - ₹5,000; Stage 2 (Vaccination) - ₹2,000; Stage 3 (Class 1 admission) - ₹3,000; Stage 4 (Class 6 admission) - ₹3,000; Stage 5 (Class 9 admission) - ₹5,000; Stage 6 (Diploma/Degree admission) - ₹7,000.",
        "max_benefit_amount": 25000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 22,
            "max_annual_income": 300000,
            "eligible_occupations": ["Student", "Child"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Family must be permanent residents of Uttar Pradesh.",
                "Total annual parental income must not exceed ₹3,00,000.",
                "Maximum two daughters per family eligible (third girl eligible in case of twin birth in second delivery)."
            ]
        },
        "required_documents": [
            "Aadhaar Card of girl child and parents",
            "UP Domicile Certificate",
            "Birth Certificate / Hospital discharge slip",
            "Immunization Card / School Admission Certificate",
            "Parental Income Certificate (<= ₹3 Lakh)",
            "Bank Passbook in the name of the girl or joint with mother"
        ],
        "application_process": "1. Apply online on mksy.up.gov.in. 2. Select specific stage / milestone and upload admission/vaccination proof. 3. Scrutiny by Block Development Officer / SDM. 4. DBT credit directly into bank account.",
        "official_url": "https://mksy.up.gov.in",
        "verification_date": "2026-10-20",
        "source": "Women & Child Development Department, Uttar Pradesh",
        "tags": "kanya sumangala, up scheme, girl child, 25000 grant, education, maternity, up govt"
    },
    {
        "code": "UP-ABHYUDAYA",
        "name": "Mukhyamantri Abhyudaya Yojana",
        "name_hindi": "मुख्यमंत्री अभ्युदय योजना",
        "level": "State",
        "state": "Uttar Pradesh",
        "ministry": "Social Welfare Department, Uttar Pradesh",
        "category": "Education & Learning",
        "target_audience": "Talented and aspiring youth of Uttar Pradesh preparing for competitive examinations",
        "short_description": "Free physical and virtual coaching by IAS/IPS/PCS officers and subject experts for UPSC, UPPSC, JEE, NEET, and CDS.",
        "full_description": "Initiative by the UP Government providing comprehensive, high-quality, free competitive exam coaching to students from economically weaker backgrounds. Physical coaching centres run in all divisional headquarters, complemented by virtual classes, free study materials, and free tablet distribution for top performers.",
        "benefits": "Free classroom coaching and mentoring by senior administrative officers and domain specialists. Free study content on Abhyudaya portal, doubt-clearing sessions, and free tablet devices for selected meritorious students.",
        "max_benefit_amount": 15000,
        "eligibility_criteria": {
            "min_age": 16,
            "max_age": 35,
            "max_annual_income": None,
            "eligible_occupations": ["Student", "Aspirant"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a resident of Uttar Pradesh.",
                "Must qualify the state-level Abhyudaya entrance test for physical batch admission.",
                "Virtual live classes accessible to all registered aspirants."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Educational Certificates (10th/12th/Graduation as per exam)",
            "Domicile Certificate of Uttar Pradesh"
        ],
        "application_process": "1. Register on abhyuday.up.gov.in. 2. Select course (UPSC, NEET, JEE, NDA/CDS). 3. Appear in online qualifying examination. 4. Attend physical centre or access digital lectures.",
        "official_url": "https://abhyuday.up.gov.in",
        "verification_date": "2026-10-20",
        "source": "Social Welfare Department, Govt. of Uttar Pradesh",
        "tags": "abhyudaya, free coaching, upsc, neet, jee, uttar pradesh, tablet scheme, civil services"
    },

    # ------------------- MADHYA PRADESH -------------------
    {
        "code": "MP-LADLI-BEHNA",
        "name": "Mukhyamantri Ladli Behna Yojana",
        "name_hindi": "मुख्यमंत्री लाड़ली बहना योजना (मध्य प्रदेश)",
        "level": "State",
        "state": "Madhya Pradesh",
        "ministry": "Women and Child Development Department, Madhya Pradesh",
        "category": "Women & Child",
        "target_audience": "Resident women of Madhya Pradesh aged 21 to 60 years from economically disadvantaged families",
        "short_description": "Monthly direct benefit transfer of ₹1,250 directly into the bank accounts of women on the 10th of every month.",
        "full_description": "Pioneering financial empowerment initiative by Government of Madhya Pradesh to foster economic independence among women, improve health and nutrition of children, and enhance family decision-making. Eligible women receive ₹1,250 every month via Aadhaar-linked DBT.",
        "benefits": "₹1,250 per month (₹15,000 per annum) directly credited into Aadhaar-seeded DBT bank accounts on the 10th of each calendar month.",
        "max_benefit_amount": 15000,
        "eligibility_criteria": {
            "min_age": 21,
            "max_age": 60,
            "max_annual_income": 250000,
            "eligible_occupations": ["All", "Homemaker", "Agricultural Worker", "Self Employed"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": 5.0,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a married, widowed, divorced, or deserted woman resident of MP.",
                "Age between 21 and 60 years.",
                "Total annual family income must be under ₹2.50 Lakh, and combined agricultural landholding less than 5 acres.",
                "No family member should be a government employee or income tax payee."
            ]
        },
        "required_documents": [
            "Samagra Family ID (Samagra Sadasya ID with e-KYC completed)",
            "Aadhaar Card",
            "Bank Account Passbook (Aadhaar linked and DBT active)"
        ],
        "application_process": "1. Complete Samagra e-KYC with Aadhaar. 2. Attend registration camp at Gram Panchayat or Ward Office. 3. Camp operator submits online form with live photograph. 4. DBT credited monthly.",
        "official_url": "https://cmladlibahna.mp.gov.in",
        "verification_date": "2026-10-20",
        "source": "Women & Child Development Department, Govt. of Madhya Pradesh",
        "tags": "ladli behna, madhya pradesh, 1250 monthly, samagra id, women welfare, dbt"
    },
    {
        "code": "MP-LADLI-LAXMI",
        "name": "Ladli Laxmi Yojana 2.0",
        "name_hindi": "लाड़ली लक्ष्मी योजना 2.0 (मध्य प्रदेश)",
        "level": "State",
        "state": "Madhya Pradesh",
        "ministry": "Women and Child Development Department, Madhya Pradesh",
        "category": "Women & Child",
        "target_audience": "Girl children born in Madhya Pradesh to non-income tax paying parents",
        "short_description": "Cumulative financial assurance of ₹1,43,000 from birth till age 21, plus ₹25,000 incentive on college admission.",
        "full_description": "First launched in 2007 and upgraded to Ladli Laxmi 2.0, this scheme aims to lay a firm foundation for the girl child by improving sex ratio, preventing female feticide, promoting female education, and preventing child marriage. The state purchases National Savings Certificates for the girl, assuring lump-sum payouts.",
        "benefits": "Total financial benefit of ₹1,43,000. Periodic educational scholarships: ₹2,000 (Class 6), ₹4,000 (Class 9), ₹6,000 (Class 11 & 12). Incentive of ₹25,000 on taking admission into graduation/professional courses. Final lump-sum payment of ₹1,00,000 on completing 21 years without early marriage.",
        "max_benefit_amount": 143000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 1,
            "max_annual_income": None,
            "eligible_occupations": ["Child", "Student"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Parents must be permanent residents of Madhya Pradesh and non-income tax payers.",
                "Girl child must be registered in an Anganwadi centre within one year of birth.",
                "Family planning adopted after maximum two children.",
                "Marriage must not occur before 18 years of age."
            ]
        },
        "required_documents": [
            "Samagra ID and Family ID",
            "Child Birth Certificate",
            "Aadhaar Card of parents",
            "Family Planning Certificate (after second child)"
        ],
        "application_process": "1. Apply via Anganwadi or MP Online kiosk / ladlilaxmi.mp.gov.in within one year of birth. 2. Project officer verifies details. 3. Ladli Laxmi Certificate issued assuring ₹1.43 Lakh.",
        "official_url": "https://ladlilaxmi.mp.gov.in",
        "verification_date": "2026-10-20",
        "source": "Women & Child Development Department, Madhya Pradesh",
        "tags": "ladli laxmi, girl child, 1.43 lakh, education grant, madhya pradesh, samagra"
    },

    # ------------------- KARNATAKA -------------------
    {
        "code": "KA-GRUHA-LAKSHMI",
        "name": "Gruha Lakshmi Scheme",
        "name_hindi": "गृह लक्ष्मी योजना (कर्नाटक)",
        "level": "State",
        "state": "Karnataka",
        "ministry": "Women and Child Development Department, Karnataka",
        "category": "Women & Child",
        "target_audience": "Woman head of every eligible household holding BPL, Antyodaya, or APL ration cards in Karnataka",
        "short_description": "₹2,000 per month financial assistance deposited directly into the bank accounts of women heads of households.",
        "full_description": "One of the five flagship guarantees of the Government of Karnataka. Provides ₹2,000 per month to the woman head of household designated in the family ration card, supporting domestic financial management and poverty alleviation.",
        "benefits": "Direct benefit transfer of ₹2,000 every month (₹24,000 per year) directly to the woman's bank account linked with Aadhaar.",
        "max_benefit_amount": 24000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 85,
            "max_annual_income": None,
            "eligible_occupations": ["All", "Homemaker"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Woman must be listed as the head of family in BPL, APL, or Antyodaya ration cards.",
                "Only one woman per household eligible.",
                "Women or husbands paying Income Tax or GST are excluded."
            ]
        },
        "required_documents": [
            "Aadhaar Card of woman and husband",
            "Karnataka Ration Card (BPL / APL / AAY)",
            "Aadhaar-seeded Bank Account Passbook",
            "Active mobile number linked to Aadhaar"
        ],
        "application_process": "1. Register at Grama One, Karnataka One, or Bangalore One centres, or via Seva Sindhu portal. 2. SMS appointment sent to avoid queues. 3. Monthly DBT credit via e-Kuber.",
        "official_url": "https://sevasindhu.karnataka.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Women & Child Development, Govt. of Karnataka",
        "tags": "gruha lakshmi, karnataka, 2000 monthly, woman head, sevasindhu, dbt guarantee"
    },
    {
        "code": "KA-SHAKTI",
        "name": "Shakti Scheme Karnataka",
        "name_hindi": "शक्ति योजना (मुफ्त बस यात्रा)",
        "level": "State",
        "state": "Karnataka",
        "ministry": "Transport Department, Karnataka",
        "category": "Women & Child",
        "target_audience": "All women and transgender residents of Karnataka",
        "short_description": "100% free travel for women in state road transport corporation buses (KSRTC, BMTC, NWKRTC, KKRTC).",
        "full_description": "Under the Shakti scheme, all women residents of Karnataka (including students and working women) can travel free of cost in ordinary and express state-run buses across the entire state, expanding workforce participation and educational mobility.",
        "benefits": "Free bus transport across KSRTC, BMTC, NWKRTC, and KKRTC state bus networks within Karnataka. Saves ₹1,000 to ₹3,000 monthly in commuting costs.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a woman or transgender person residing in Karnataka.",
                "Applies to non-AC Ordinary and Express intra-state bus services."
            ]
        },
        "required_documents": [
            "Any Government ID with Karnataka residential address (Aadhaar / Voter ID / Driving License)"
        ],
        "application_process": "Present valid Karnataka residential ID to bus conductor. A 'Zero Fare' paper ticket is issued immediately.",
        "official_url": "https://transport.karnataka.gov.in",
        "verification_date": "2026-10-20",
        "source": "Transport Department, Govt. of Karnataka",
        "tags": "shakti scheme, free bus, karnataka women, ksrtc, bmtc, zero ticket, public transport"
    },
    {
        "code": "KA-YUVA-NIDHI",
        "name": "Yuva Nidhi Scheme",
        "name_hindi": "युवा निधि योजना (कर्नाटक)",
        "level": "State",
        "state": "Karnataka",
        "ministry": "Department of Skill Development, Entrepreneurship and Livelihood, Karnataka",
        "category": "Employment & Skill Development",
        "target_audience": "Unemployed degree and diploma holders in Karnataka who completed studies in recent academic years",
        "short_description": "Monthly unemployment assistance of ₹3,000 for degree holders and ₹1,500 for diploma holders for up to 2 years.",
        "full_description": "Yuva Nidhi is Karnataka's guarantee scheme providing financial sustenance and skill training linkages to unemployed graduates and diploma holders for up to 24 months or until securing employment/self-employment.",
        "benefits": "₹3,000 per month for unemployed graduates and ₹1,500 per month for diploma holders credited directly into Aadhaar-linked bank account via DBT.",
        "max_benefit_amount": 72000,
        "eligibility_criteria": {
            "min_age": 21,
            "max_age": 30,
            "max_annual_income": None,
            "eligible_occupations": ["Graduate", "Diploma Holder", "Unemployed Youth"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must have passed Degree/Diploma from a recognized institution in Karnataka.",
                "Must have remained unemployed for at least 180 days (6 months) after passing.",
                "Must not be enrolled in higher education or receiving apprentice stipends."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Degree / Diploma Certificate and Marks Card",
            "Karnataka Domicile proof (minimum 6 years schooling in Karnataka)",
            "Aadhaar-seeded Bank Account Passbook"
        ],
        "application_process": "1. Apply on Seva Sindhu portal (sevasindhugs.karnataka.gov.in). 2. Submit self-declaration of unemployment. 3. Automatic verification against higher education database. 4. Monthly DBT.",
        "official_url": "https://sevasindhugs.karnataka.gov.in",
        "verification_date": "2026-10-20",
        "source": "Skill Development Department, Govt. of Karnataka",
        "tags": "yuva nidhi, karnataka graduate, 3000 monthly, diploma stipend, unemployment allowance"
    },

    # ------------------- TAMIL NADU -------------------
    {
        "code": "TN-MAGALIR-URIMAI",
        "name": "Kalaignar Magalir Urimai Thittam",
        "name_hindi": "कलैग्नार मगलिर उरिमई तिट्टम (तमिलनाडु)",
        "level": "State",
        "state": "Tamil Nadu",
        "ministry": "Special Programme Implementation Department, Tamil Nadu",
        "category": "Women & Child",
        "target_audience": "Women heads of families in Tamil Nadu with annual household income up to ₹2.5 Lakh",
        "short_description": "Basic income entitlement of ₹1,000 per month transferred directly to women heads of eligible households.",
        "full_description": "Recognizing the unpaid domestic labor of homemakers, this pioneering basic income scheme transfers ₹1,000 monthly to over 1.15 crore eligible women heads of households in Tamil Nadu via direct benefit transfer.",
        "benefits": "₹1,000 per month (₹12,000 per year) deposited directly into beneficiary's bank account on the 15th of every month.",
        "max_benefit_amount": 12000,
        "eligibility_criteria": {
            "min_age": 21,
            "max_age": 75,
            "max_annual_income": 250000,
            "eligible_occupations": ["All", "Homemaker"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": 4.0,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Woman must be listed as head of family in Tamil Nadu Smart Family Card.",
                "Annual family income must be below ₹2.50 Lakh, and domestic electricity consumption below 3,600 units/year.",
                "Landholding must not exceed 5 acres wetland or 10 acres dry land.",
                "Family should not pay income tax or professional tax."
            ]
        },
        "required_documents": [
            "Tamil Nadu Smart Family Card (Ration Card)",
            "Aadhaar Card",
            "Electricity Consumer Number",
            "Bank Account Passbook (Aadhaar linked)"
        ],
        "application_process": "1. Fill application at special ward camps / Fair Price Shops. 2. Biometric e-KYC on e-Sevai handheld device. 3. Field verification. 4. Monthly credit on the 15th of each month.",
        "official_url": "https://kmut.tn.gov.in",
        "verification_date": "2026-10-20",
        "source": "Govt. of Tamil Nadu (kmut.tn.gov.in)",
        "tags": "magalir urimai, tamil nadu, 1000 monthly, women basic income, smart card, dbt"
    },
    {
        "code": "TN-PUDHUMAI-PENN",
        "name": "Pudhumai Penn Scheme (Moovalur Ramamirtham Ammaiyar Higher Education)",
        "name_hindi": "पुधुमै पेन योजना (तमिलनाडु उच्च शिक्षा सहायता)",
        "level": "State",
        "state": "Tamil Nadu",
        "ministry": "Social Welfare and Women Empowerment Department, Tamil Nadu",
        "category": "Education & Learning",
        "target_audience": "Girl students who studied in government schools from Class 6 to 12 pursuing higher education",
        "short_description": "₹1,000 per month financial assistance for girl students until completion of undergraduate degree or diploma.",
        "full_description": "Pudhumai Penn Scheme motivates girl students from government schools to pursue higher education, preventing early child marriages and raising the female higher education gross enrolment ratio in Tamil Nadu.",
        "benefits": "₹1,000 per month credited directly into the student's bank account every month until completion of undergraduate degree, diploma, ITI, or professional course.",
        "max_benefit_amount": 12000,
        "eligibility_criteria": {
            "min_age": 17,
            "max_age": 25,
            "max_annual_income": None,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Candidate must be female.",
                "Must have studied continuously in Government schools from Class 6 to Class 12 in Tamil Nadu.",
                "Enrolled in recognized undergraduate, diploma, or ITI course in Tamil Nadu."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "School Transfer Certificate (proving study in Govt school from Class 6 to 12)",
            "College Bonafide Certificate & Admission Receipt",
            "Bank Account Passbook (Aadhaar linked)"
        ],
        "application_process": "1. Apply online via penkalvi.tn.gov.in. 2. College Nodal Officer verifies school certificates with EMIS data. 3. Direct monthly DBT credit.",
        "official_url": "https://penkalvi.tn.gov.in",
        "verification_date": "2026-10-20",
        "source": "Social Welfare Department, Govt. of Tamil Nadu",
        "tags": "pudhumai penn, tamil nadu, girl student, 1000 monthly, higher education, college, emis"
    },

    # ------------------- WEST BENGAL -------------------
    {
        "code": "WB-LAKSHMIR-BHANDAR",
        "name": "Lakshmir Bhandar Scheme",
        "name_hindi": "लक्ष्मी भंडार योजना (पश्चिम बंगाल)",
        "level": "State",
        "state": "West Bengal",
        "ministry": "Department of Women & Child Development and Social Welfare, West Bengal",
        "category": "Women & Child",
        "target_audience": "Female heads of households aged 25 to 60 years in West Bengal",
        "short_description": "Assured monthly financial support of ₹1,000 (General) and ₹1,200 (SC/ST) directly to women via DBT.",
        "full_description": "Lakshmir Bhandar is West Bengal's flagship financial assistance scheme providing basic monthly support to women family heads, enhancing self-reliance and nutritional security. Enrolment is facilitated during statewide Duare Sarkar camps.",
        "benefits": "Monthly financial aid of ₹1,000 per month for General category women and ₹1,200 per month for SC/ST category women deposited directly into bank accounts via DBT.",
        "max_benefit_amount": 14400,
        "eligibility_criteria": {
            "min_age": 25,
            "max_age": 60,
            "max_annual_income": None,
            "eligible_occupations": ["All", "Homemaker"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Woman resident of West Bengal aged 25 to 60 years.",
                "Must hold a Swasthya Sathi health card.",
                "Government employees and pensioners are excluded."
            ]
        },
        "required_documents": [
            "Swasthya Sathi Card",
            "Aadhaar Card",
            "SC / ST Certificate (for higher ₹1,200 assistance)",
            "Bank Account Passbook (Aadhaar linked)",
            "Passport Size Photograph"
        ],
        "application_process": "1. Collect free application form at Duare Sarkar camp or BDO office. 2. Submit form with Swasthya Sathi and Aadhaar copy. 3. Approval and monthly DBT credit.",
        "official_url": "https://socialwelfare.wb.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Women & Child Development, Govt. of West Bengal",
        "tags": "lakshmir bhandar, west bengal, 1000 monthly, duare sarkar, swasthya sathi, women dbt"
    },
    {
        "code": "WB-KANYASHREE",
        "name": "Kanyashree Prakalpa (K1 & K2)",
        "name_hindi": "कन्याश्री प्रकल्प (पश्चिम बंगाल)",
        "level": "State",
        "state": "West Bengal",
        "ministry": "Department of Women & Child Development and Social Welfare, West Bengal",
        "category": "Education & Learning",
        "target_audience": "Adolescent school and college-going girls aged 13 to 19 years in West Bengal",
        "short_description": "Annual scholarship of ₹1,000 (K1) and one-time lump-sum grant of ₹25,000 (K2) upon reaching 18 years unmarried.",
        "full_description": "UN Public Service Award winning conditional cash transfer scheme aimed at improving the status and well-being of the girl child in West Bengal by incentivizing education and preventing child marriage.",
        "benefits": "K1: Annual scholarship of ₹1,000 per year for girls aged 13-18 studying in Class 8 to 12. K2: One-time grant of ₹25,000 on reaching 18 years of age while continuing education and remaining unmarried.",
        "max_benefit_amount": 25000,
        "eligibility_criteria": {
            "min_age": 13,
            "max_age": 19,
            "max_annual_income": 120000,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Girl must be a resident of West Bengal enrolled in a recognized school/college.",
                "Must be unmarried.",
                "Income ceiling of ₹1.20 Lakh/year (waived for differently-abled girls, orphans, or inmates of home)."
            ]
        },
        "required_documents": [
            "Birth Certificate",
            "Aadhaar Card",
            "Declaration of unmarried status certified by parent",
            "School / College Enrolment Certificate",
            "Bank Passbook in the name of the girl"
        ],
        "application_process": "1. Collect K1/K2 form from school/college. 2. Head of Institution verifies and uploads to Kanyashree Portal (wbkanyashree.gov.in). 3. Direct DBT credit to student's bank account.",
        "official_url": "https://wbkanyashree.gov.in",
        "verification_date": "2026-10-20",
        "source": "Govt. of West Bengal & UNICEF",
        "tags": "kanyashree, west bengal, girl scholarship, 25000 grant, child marriage prevention"
    },

    # ------------------- BIHAR -------------------
    {
        "code": "BR-KANYA-UTTHAN",
        "name": "Mukhyamantri Kanya Utthan Yojana",
        "name_hindi": "मुख्यमंत्री कन्या उत्थान योजना (बिहार)",
        "level": "State",
        "state": "Bihar",
        "ministry": "Education Department & Social Welfare Department, Bihar",
        "category": "Education & Learning",
        "target_audience": "Girl children in Bihar from birth through higher education and graduation",
        "short_description": "Financial assistance of up to ₹54,100 from birth till graduation (including ₹25,000 on 12th pass & ₹50,000 on graduation).",
        "full_description": "Comprehensive girl child empowerment scheme by Government of Bihar to eliminate female feticide, promote complete immunization, eradicate child marriage, and ensure higher education for girls. Disburses financial rewards at birth, vaccination, school uniforms, sanitary napkins, intermediate pass, and degree completion.",
        "benefits": "₹2,000 at birth; ₹1,000 on complete 1-year immunization; annual uniform/napkin grants; ₹25,000 upon passing Class 12 (unmarried); and ₹50,000 upon graduating from a recognized university.",
        "max_benefit_amount": 54100,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 25,
            "max_annual_income": None,
            "eligible_occupations": ["Student", "Child"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a permanent resident of Bihar.",
                "For intermediate incentive (₹25,000): Must pass 12th from Bihar School Examination Board and remain unmarried.",
                "For graduation incentive (₹50,000): Must pass undergraduate degree from a recognized university in Bihar (married or unmarried)."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Bihar Domicile Certificate",
            "Class 12 / Degree Marksheet and Admit Card",
            "Bank Account Passbook (Aadhaar linked in student's name)"
        ],
        "application_process": "1. Apply online via Medhasoft portal (medhasoft.bih.nic.in). 2. System validates registration number and board roll number. 3. College verification. 4. DBT payment release.",
        "official_url": "http://medhasoft.bih.nic.in",
        "verification_date": "2026-10-20",
        "source": "Education Department, Govt. of Bihar",
        "tags": "kanya utthan, bihar, girl education, 50000 graduation grant, 25000 intermediate, medhasoft"
    },
    {
        "code": "BR-STUDENT-CREDIT-CARD",
        "name": "Bihar Student Credit Card Scheme (BSCCS)",
        "name_hindi": "बिहार स्टूडेंट क्रेडिट कार्ड योजना",
        "level": "State",
        "state": "Bihar",
        "ministry": "Education Department, Bihar",
        "category": "Education & Learning",
        "target_audience": "12th pass students from Bihar seeking higher education loans for engineering, medical, MBA, and general degrees",
        "short_description": "Concessional education loan up to ₹4,00,000 at 1% interest for girls/divyang and 4% for boys with government guarantee.",
        "full_description": "Under Bihar's Seven Resolves (Saat Nischay), BSCCS ensures that no student is deprived of higher education due to financial hardship. State government acts as 100% guarantor for bank/corporation loans up to ₹4 Lakh with repayment beginning 1 year after course completion.",
        "benefits": "Education loan up to ₹4,00,000 covering tuition, hostel, books, and laptop. Extremely concessional simple interest of 1% for female, transgender, and disabled students (4% for male students). Zero collateral and government guarantee.",
        "max_benefit_amount": 400000,
        "eligibility_criteria": {
            "min_age": 17,
            "max_age": 25,
            "max_annual_income": None,
            "eligible_occupations": ["Student"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be a permanent resident of Bihar.",
                "Must have passed Class 12 or equivalent.",
                "Enrolled in a recognized institution within Bihar or anywhere in India with NAAC/NBA/NIRF accreditation."
            ]
        },
        "required_documents": [
            "Aadhaar Card of student and co-applicant (parents)",
            "Class 10 and 12 Marksheet & Certificates",
            "Admission confirmation slip and fee structure from institution",
            "Bihar Domicile Certificate",
            "Bank Account Passbook"
        ],
        "application_process": "1. Apply on MNSSBY portal (7nishchay-yuvaupmission.bihar.gov.in). 2. Visit District Registration and Counseling Centre (DRCC) for document verification. 3. Bihar State Education Finance Corporation sanctions loan.",
        "official_url": "https://www.7nishchay-yuvaupmission.bihar.gov.in",
        "verification_date": "2026-10-20",
        "source": "Bihar State Education Finance Corporation & Planning Department",
        "tags": "student credit card, bihar education loan, 4 lakh loan, 1 percent interest, saat nischay, drcc"
    },

    # ------------------- ODISHA -------------------
    {
        "code": "OD-BSKY",
        "name": "Biju Swasthya Kalyan Yojana (BSKY / Gopabandhu Jan Arogya)",
        "name_hindi": "बीजू स्वास्थ्य कल्याण योजना (ओडिशा)",
        "level": "State",
        "state": "Odisha",
        "ministry": "Health & Family Welfare Department, Odisha",
        "category": "Health & Wellness",
        "target_audience": "Economically vulnerable families holding National / State Food Security Act ration cards in Odisha",
        "short_description": "Cashless healthcare assurance of ₹5 Lakh per family and up to ₹10 Lakh for female family members.",
        "full_description": "Universal health coverage initiative in Odisha offering cashless secondary and tertiary hospitalization across empaneled public and private hospitals nationwide. Distinctive benefit provides an enhanced health cover of ₹10 Lakh specifically for female family members.",
        "benefits": "Cashless hospitalization up to ₹5,00,000 per family per year, with an enhanced cover of ₹10,00,000 per year for women members. Free healthcare at all government medical colleges and hospitals universally for all citizens.",
        "max_benefit_amount": 1000000,
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
                "Must hold an NFSA or SFSS Ration Card in Odisha, or have a BSKY Smart Health Card.",
                "Cashless facility available in over 800 empaneled hospitals inside and outside Odisha."
            ]
        },
        "required_documents": [
            "BSKY Smart Health Card / NFSA Ration Card",
            "Aadhaar Card"
        ],
        "application_process": "Automatic entitlement for NFSA ration card holders. Swasthya Mitra at empaneled hospital assists with cashless admission and billing.",
        "official_url": "https://bsky.odisha.gov.in",
        "verification_date": "2026-10-20",
        "source": "Health & Family Welfare Department, Govt. of Odisha",
        "tags": "bsky, odisha health, 10 lakh women health cover, cashless hospitalization, swasthya mitra"
    },
    {
        "code": "OD-KALIA",
        "name": "Krushak Assistance for Livelihood and Income Augmentation (KALIA)",
        "name_hindi": "कालिया योजना (ओडिशा)",
        "level": "State",
        "state": "Odisha",
        "ministry": "Agriculture & Farmers' Empowerment Department, Odisha",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Small and marginal farmers, sharecroppers, and landless agricultural households in Odisha",
        "short_description": "Direct financial assistance of ₹10,000 per family per year for farm inputs and ₹12,500 for landless farm labourers.",
        "full_description": "KALIA is an inclusive agricultural support scheme that covers not just landowning farmers, but also tenant farmers, sharecroppers, and landless agricultural labourers. It provides financial assistance for cultivation, livelihood support for animal husbandry/fisheries, and life/disability insurance.",
        "benefits": "₹10,000 per family per year (₹5,000 for Kharif + ₹5,000 for Rabi) for small and marginal farmers. Landless agricultural households receive ₹12,500 for non-farm activities (goat rearing, duckery, mushroom cultivation). Free life and disability insurance.",
        "max_benefit_amount": 12500,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Sharecropper", "Tenant Farmer", "Landless Labourer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": 2.0,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Small and marginal farmers owning cultivable land up to 2 hectares; or landless agricultural households.",
                "Must be a resident of Odisha.",
                "Government employees and income tax payers are excluded."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Ration Card",
            "Land Record (for cultivators) / MGNREGA Job Card (for landless)",
            "Bank Passbook (Aadhaar seeded)"
        ],
        "application_process": "1. Verify inclusion on kalia.odisha.gov.in. 2. New registrations through Gram Panchayat camp or online portal. 3. Direct DBT transfer via state treasury.",
        "official_url": "https://kalia.odisha.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Agriculture & Farmers' Empowerment, Govt. of Odisha",
        "tags": "kalia, odisha farmer, sharecropper, landless agricultural labourer, crop input, dbt"
    },

    # ------------------- DELHI -------------------
    {
        "code": "DL-LADLI",
        "name": "Delhi Ladli Scheme",
        "name_hindi": "दिल्ली लाड़ली योजना",
        "level": "State",
        "state": "Delhi",
        "ministry": "Department of Women and Child Development, GNCTD",
        "category": "Women & Child",
        "target_audience": "Girl children born in NCT of Delhi whose family income does not exceed ₹1 Lakh per year",
        "short_description": "Financial assistance up to ₹1,00,000 deposited in fixed deposits at birth and upon entering Classes 1, 6, 9, 10, and 12.",
        "full_description": "Promotes the birth, upbringing, and education of girl children in the National Capital Territory of Delhi. Financial assistance is deposited with the State Bank of India in the name of the child at various stages, maturing when the girl reaches 18 years of age and passes Class 10.",
        "benefits": "₹11,000 for institutional birth (₹10,000 for home birth); and ₹5,000 each upon admission to Class 1, Class 6, Class 9, Class 10, and Class 12. Final maturity value with compound interest reaches approximately ₹1,00,000 at age 18.",
        "max_benefit_amount": 100000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 18,
            "max_annual_income": 100000,
            "eligible_occupations": ["Child", "Student"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Urban", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Family must have been residing in Delhi for at least three continuous years preceding application.",
                "Total annual family income must not exceed ₹1,00,000.",
                "Girl must be born in Delhi and enrolled in a recognized school in Delhi.",
                "Benefit limited to two girl children per family."
            ]
        },
        "required_documents": [
            "Proof of 3 years residence in Delhi (Ration Card / Voter ID / Electricity Bill)",
            "Income Certificate (under ₹1 Lakh)",
            "Birth Certificate of girl child issued by MCD / NDMC",
            "Aadhaar Card of girl and parents",
            "School Admission Verification form"
        ],
        "application_process": "1. Apply through the school Principal or at District Women and Child Development Office within 90 days of birth/admission. 2. SBI issues fixed deposit certificate. 3. Maturity claim submitted at age 18.",
        "official_url": "https://wcd.delhi.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Women & Child Development, GNCTD",
        "tags": "delhi ladli, girl child, 1 lakh maturity, delhi government, sbi fixed deposit, education"
    },

    # ------------------- GUJARAT -------------------
    {
        "code": "GJ-MANAV-GARIMA",
        "name": "Manav Garima Yojana Gujarat",
        "name_hindi": "मानव गरिमा योजना (गुजरात)",
        "level": "State",
        "state": "Gujarat",
        "ministry": "Social Justice and Empowerment Department, Gujarat",
        "category": "Employment & Skill Development",
        "target_audience": "Artisans, hawkers, cobblers, tailors, and small self-employed workers belonging to SC and backward classes",
        "short_description": "Free specialized professional toolkits worth up to ₹25,000 across 28 traditional trades for self-employment.",
        "full_description": "Manav Garima Yojana empowers poor artisans, daily wage earners, and backward class youth to earn a dignified livelihood by providing them with free, high-quality toolkits and equipment across 28 trades (Tailoring, Beauty Parlour, Carpentry, Plumbing, Electrician, Barber, Cycle Repair, Cobbler, Food Vending).",
        "benefits": "Free complete professional toolkit worth up to ₹25,000 provided without requiring any cash contribution or bank loan.",
        "max_benefit_amount": 25000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 60,
            "max_annual_income": 120000,
            "eligible_occupations": ["Tailor", "Barber", "Plumber", "Electrician", "Carpenter", "Cobbler", "Mason", "Street Vendor"],
            "eligible_genders": ["All"],
            "eligible_categories": ["SC", "OBC", "General"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be a permanent resident of Gujarat.",
                "Annual family income must not exceed ₹1,20,000 in rural areas and ₹1,50,000 in urban areas.",
                "Must possess experience or certified training in the applied trade."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Caste Certificate",
            "Income Certificate issued by Mamlatdar / Competent Authority",
            "Trade Training Certificate or Experience Certificate",
            "Ration Card"
        ],
        "application_process": "1. Apply on e-Samaj Kalyan portal (esamajkalyan.gujarat.gov.in). 2. Select trade and upload certificates. 3. District Social Welfare Officer verification. 4. Toolkit handed over at district camp.",
        "official_url": "https://esamajkalyan.gujarat.gov.in",
        "verification_date": "2026-10-20",
        "source": "Social Justice and Empowerment Department, Govt. of Gujarat",
        "tags": "manav garima, gujarat, free toolkit, artisan, self employment, esamajkalyan, micro trade"
    }
]

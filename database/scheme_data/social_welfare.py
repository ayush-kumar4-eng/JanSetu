"""
Social Welfare, Pension & Financial Security Schemes Dataset (Verified Official Data)
Sources: PFRDA (pfrda.org.in), Ministry of Labour and Employment (eshram.gov.in, maandhan.in),
Department of Financial Services (financialservices.gov.in), Department of Food and Public Distribution (dfpd.gov.in),
Ministry of Social Justice and Empowerment (socialjustice.gov.in), Ministry of Rural Development (nsap.nic.in).
"""

SOCIAL_WELFARE_SCHEMES = [
    {
        "code": "APY",
        "name": "Atal Pension Yojana (APY)",
        "name_hindi": "अटल पेंशन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Social Welfare & Empowerment",
        "target_audience": "All Indian citizens in the unorganized sector aged between 18 and 40 years",
        "short_description": "Guaranteed monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000, or ₹5,000 after 60 years of age.",
        "full_description": "Administered by the Pension Fund Regulatory and Development Authority (PFRDA), APY is a government-guaranteed pension scheme primarily focused on unorganized sector workers. Subscribers contribute a monthly, quarterly, or half-yearly amount based on entry age and chosen pension tier (₹1,000 to ₹5,000/month). The Government guarantees the defined benefit.",
        "benefits": "Guaranteed lifetime monthly pension of ₹1,000 to ₹5,000 to subscriber from age 60. Upon subscriber's demise, the same pension is paid to spouse for life. After demise of both subscriber and spouse, the entire accumulated pension wealth (up to ₹8.5 Lakh) is returned to the nominee.",
        "max_benefit_amount": 60000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 40,
            "max_annual_income": None,
            "eligible_occupations": ["All", "Daily Wage Earner", "Street Vendor", "Driver", "Domestic Worker", "Informal Worker", "Self Employed"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be an Indian citizen aged between 18 and 40 years at the time of joining.",
                "Must possess an active savings bank account or post office account with auto-debit facility enabled.",
                "Tax-payer exclusion: Any citizen who is or has been an income tax payer under the Income Tax Act is not eligible to join APY."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Savings Bank Account Passbook / Post Office Account details",
            "Aadhaar-linked Mobile Number for SMS updates",
            "Nominee details (Aadhaar and relation)"
        ],
        "application_process": "1. Visit the bank branch or post office where you hold a savings account, or apply online via NetBanking / PFRDA eNPS portal. 2. Select chosen pension tier (₹1,000 to ₹5,000). 3. Sign auto-debit consent form. 4. Permanent Retirement Account Number (PRAN) issued immediately.",
        "official_url": "https://www.npscra.nsdl.co.in/scheme-details.php",
        "verification_date": "2026-10-20",
        "source": "Pension Fund Regulatory and Development Authority (PFRDA) & Department of Financial Services",
        "tags": "pension, atal pension yojana, apy, retirement, old age security, guaranteed pension, pfrda"
    },
    {
        "code": "PM-SYM",
        "name": "Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM)",
        "name_hindi": "प्रधानमंत्री श्रम योगी मानधन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Labour and Employment",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Unorganized workers with monthly income up to ₹15,000 aged 18 to 40 years",
        "short_description": "Voluntary contributory pension scheme guaranteeing ₹3,000 monthly pension from age 60 with 50% central co-contribution.",
        "full_description": "PM-SYM is a central sector scheme to provide old age protection and social security to unorganized workers (home-based workers, street vendors, mid-day meal workers, head loaders, brick kiln workers, cobblers, rag pickers, domestic workers, washermen, rickshaw pullers, landless agricultural workers, construction workers). Subscribers contribute ₹55 to ₹200 monthly, with an equal matching grant from Central Govt.",
        "benefits": "Assured monthly pension of ₹3,000 directly deposited via DBT from 60 years of age. In case of subscriber's demise during receipt of pension, spouse is entitled to 50% family pension (₹1,500/month).",
        "max_benefit_amount": 36000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 40,
            "max_annual_income": 180000,
            "eligible_occupations": ["Unorganized Worker", "Street Vendor", "Domestic Worker", "Rickshaw Puller", "Construction Worker", "Agricultural Worker", "Rag Picker"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be an unorganized worker whose monthly income is ₹15,000 or below.",
                "Entry age between 18 and 40 years.",
                "Must not be engaged in organized sector covered by EPFO / ESIC / NPS (Govt funded).",
                "Must not be an income tax payer."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Savings Bank Account Passbook / Jan Dhan Account with IFSC",
            "e-Shram UAN Card (if registered)",
            "Active Mobile Number"
        ],
        "application_process": "1. Visit nearest Common Service Centre (CSC) or self-enrol on maandhan.in. 2. Provide Aadhaar and bank details for auto-debit mandate. 3. System calculates monthly contribution based on age. 4. PM-SYM Shramik Pension Card printed immediately.",
        "official_url": "https://maandhan.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Labour and Employment (maandhan.in)",
        "tags": "shramik pension, unorganized worker, labour pension, pm-sym, monthly pension, lic, eshram"
    },
    {
        "code": "PMJJBY",
        "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
        "name_hindi": "प्रधानमंत्री जीवन ज्योति बीमा योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "All savings bank/post office account holders aged 18 to 50 years",
        "short_description": "Affordable term life insurance cover of ₹2,00,000 for death due to any cause at a nominal premium of ₹436 per year.",
        "full_description": "PMJJBY is a government-backed life insurance scheme in India. It offers a renewable one-year term life cover of ₹2 Lakh to all account holders aged 18 to 50 years for death due to any reason (natural or accidental). The premium of ₹436 per annum is automatically debited from the subscriber's bank account in May each year.",
        "benefits": "₹2,00,000 sum assured paid to nominee upon the death of the insured subscriber due to any cause (illness, disease, natural death, or accident).",
        "max_benefit_amount": 200000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 50,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Individual must be aged 18 to 50 years with an active savings bank account or post office account.",
                "Must give consent for annual auto-debit of ₹436 premium.",
                "Coverage is valid up to 55 years of age subject to regular annual renewal.",
                "A 30-day initial lien period applies for deaths other than accidental."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Savings Bank Account Passbook",
            "Auto-debit Consent Form with Nominee Details"
        ],
        "application_process": "1. Approach your bank branch or activate through NetBanking / Mobile Banking application. 2. Submit auto-debit mandate for ₹436 annual premium. 3. Bank issues insurance acknowledgement receipt / Certificate of Insurance.",
        "official_url": "https://jansuraksha.gov.in",
        "verification_date": "2026-10-20",
        "source": "Jan Suraksha Portal & Department of Financial Services",
        "tags": "life insurance, term insurance, pmjjby, 2 lakh insurance, death benefit, 436 premium, jansuraksha"
    },
    {
        "code": "PMSBY",
        "name": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
        "name_hindi": "प्रधानमंत्री सुरक्षा बीमा योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "All savings bank/post office account holders aged 18 to 70 years",
        "short_description": "Accidental death and disability insurance cover of ₹2,00,000 for an ultra-low premium of just ₹20 per year.",
        "full_description": "PMSBY is a government-backed accident insurance scheme in India. For a nominal premium of ₹20 per annum auto-debited in May, the scheme provides ₹2 Lakh cover for accidental death and permanent total disability, and ₹1 Lakh for permanent partial disability.",
        "benefits": "₹2,00,000 on accidental death or total permanent disability (loss of both eyes, both hands, or both feet). ₹1,00,000 on permanent partial disability (loss of one eye, one hand, or one foot).",
        "max_benefit_amount": 200000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 70,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Individual must be aged 18 to 70 years with an active bank or post office account.",
                "Consent given for annual auto-debit of ₹20.",
                "Accident must be verified by FIR / Police Panchanama / Hospital treatment record."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Bank Account Passbook",
            "Auto-debit Consent Form with Nominee Details"
        ],
        "application_process": "1. Visit bank branch, post office, or log into NetBanking. 2. Submit PMSBY enrollment form with nominee details. 3. Account debited ₹20 annually. 4. Insurance policy document issued.",
        "official_url": "https://jansuraksha.gov.in",
        "verification_date": "2026-10-20",
        "source": "Jan Suraksha Portal & Department of Financial Services",
        "tags": "accident insurance, pmsby, 20 rupee bima, disability cover, accidental death, jansuraksha"
    },
    {
        "code": "PMGKAY",
        "name": "Pradhan Mantri Garib Kalyan Anna Yojana (PMGKAY)",
        "name_hindi": "प्रधानमंत्री गरीब कल्याण अन्न योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
        "category": "Social Welfare & Empowerment",
        "target_audience": "All 81.35 Crore NFSA beneficiaries including Antyodaya Anna Yojana (AAY) and Priority Household (PHH) card holders",
        "short_description": "100% free food grains (5 kg per person per month for PHH and 35 kg per family for AAY) distributed via Fair Price Shops.",
        "full_description": "Under PMGKAY, the Government of India provides 100% free food grains to over 81.35 crore beneficiaries covered under the National Food Security Act (NFSA). Beneficiaries do not have to pay even the subsidized NFSA prices (₹3/₹2/₹1). Extended for a period of five years starting January 1, 2024.",
        "benefits": "Free food grains (wheat/rice/coarse grains): 5 kg per person per month for Priority Household (PHH) ration card holders; and 35 kg per family per month for Antyodaya Anna Yojana (AAY) households. Zero cost at Fair Price Shops.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All", "Agricultural Labourer", "Daily Wage Earner", "Marginal Farmer", "BPL Family"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All", "BPL", "AAY", "PHH"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": True,
            "key_rules": [
                "Must hold an active Antyodaya Anna Yojana (AAY) or Priority Household (PHH) ration card under NFSA.",
                "Ration cards must be Aadhaar-authenticated at the e-PoS (electronic Point of Sale) device.",
                "Beneficiaries can lift rations from any Fair Price Shop across India under One Nation One Ration Card (ONORC)."
            ]
        },
        "required_documents": [
            "NFSA Ration Card (PHH or AAY)",
            "Aadhaar Card of all family members listed on the ration card"
        ],
        "application_process": "Visit the nearest Fair Price Shop (Ration Dealer). Provide biometric fingerprint or IRIS authentication on the e-PoS machine, or collect ration using OTP on registered mobile number.",
        "official_url": "https://dfpd.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Food & Public Distribution (DFPD) & myScheme Portal",
        "tags": "ration, free grain, pmgkay, food security, wheat, rice, nfsa, aay, phh, fair price shop"
    },
    {
        "code": "IGNOAPS",
        "name": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
        "name_hindi": "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Rural Development",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Senior citizens aged 60 years and above living below the poverty line (BPL)",
        "short_description": "Non-contributory monthly old age social security pension of ₹500 to ₹1,500 per month (combined central + state contribution).",
        "full_description": "Component of the National Social Assistance Programme (NSAP). Central government contributes ₹200/month for persons aged 60-79 years, and ₹500/month for persons aged 80 years and above, with states supplementing an additional ₹300 to ₹1,000+ monthly pension directly through DBT.",
        "benefits": "Monthly pension ranging from ₹500 to ₹1,500+ (depending on state top-up) credited directly into the elderly person's Aadhaar-seeded bank or post office account every month.",
        "max_benefit_amount": 18000,
        "eligibility_criteria": {
            "min_age": 60,
            "max_age": 100,
            "max_annual_income": 100000,
            "eligible_occupations": ["All", "Senior Citizen", "Retired Worker", "Homemaker"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All", "BPL"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": True,
            "key_rules": [
                "Applicant must be 60 years of age or older.",
                "Must belong to a household living below the poverty line according to SECC/BPL census criteria.",
                "Must not be receiving another government social security pension simultaneously."
            ]
        },
        "required_documents": [
            "Aadhaar Card / Voter ID (proof of age >= 60)",
            "Valid BPL Card / BPL Certificate issued by Gram Panchayat / ULB",
            "Bank Account Passbook (Aadhaar linked)",
            "Passport Size Photograph"
        ],
        "application_process": "1. Apply online via nsap.nic.in or submit physical application form at Gram Panchayat / Block Development Office / Municipal Ward Office. 2. Verification of BPL list and age by Social Welfare Inspector. 3. Sanction order issued by Sub-Divisional Magistrate (SDM) / District Collector.",
        "official_url": "https://nsap.nic.in",
        "verification_date": "2026-10-20",
        "source": "National Social Assistance Programme (NSAP) & MoRD",
        "tags": "old age pension, senior citizen, ignoaps, nsap, bpl pension, elderly social security"
    },
    {
        "code": "IGNWPS",
        "name": "Indira Gandhi National Widow Pension Scheme (IGNWPS)",
        "name_hindi": "इंदिरा गांधी राष्ट्रीय विधवा पेंशन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Rural Development",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Widows aged 40 to 79 years living below the poverty line",
        "short_description": "Monthly social security pension of ₹500 to ₹1,500 directly transferred to destitute widows belonging to BPL households.",
        "full_description": "Sub-scheme under the National Social Assistance Programme (NSAP) providing non-contributory monthly pension support to vulnerable widows living below the poverty line, safeguarding them against extreme destitution and poverty.",
        "benefits": "Monthly pension ranging from ₹500 to ₹1,500 (Central Govt component ₹300/month plus State Govt top-up) credited via DBT into bank/post office account.",
        "max_benefit_amount": 18000,
        "eligibility_criteria": {
            "min_age": 40,
            "max_age": 79,
            "max_annual_income": 100000,
            "eligible_occupations": ["All", "Homemaker", "Widow"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All", "BPL"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": True,
            "key_rules": [
                "Applicant must be a widow aged between 40 and 79 years.",
                "Must belong to a household living below the poverty line (BPL).",
                "Upon attaining 80 years of age, the beneficiary is automatically migrated to the higher IGNOAPS pension tier."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Husband's Death Certificate",
            "BPL Ration Card / Income Certificate",
            "Age proof (minimum 40 years)",
            "Bank Account Passbook"
        ],
        "application_process": "1. Submit application on NSAP portal (nsap.nic.in) or to Block Development Officer (BDO) / Municipal Councillor. 2. Field verification of marital status and BPL criteria. 3. Monthly pension credited via PFMS.",
        "official_url": "https://nsap.nic.in",
        "verification_date": "2026-10-20",
        "source": "National Social Assistance Programme (NSAP) & MoRD",
        "tags": "widow pension, ignwps, destitute women, bpl, monthly pension, nsap, social security"
    },
    {
        "code": "IGNDPS",
        "name": "Indira Gandhi National Disability Pension Scheme (IGNDPS)",
        "name_hindi": "इंदिरा गांधी राष्ट्रीय दिव्यांगता पेंशन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Rural Development",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Persons with severe or multiple disabilities (80% and above) aged 18 to 79 years living below the poverty line",
        "short_description": "Monthly financial pension assistance of ₹500 to ₹2,000 for severely differently-abled persons in BPL households.",
        "full_description": "Part of NSAP providing monthly financial support to persons with severe or multiple disabilities who belong to families living below the poverty line, helping them meet basic living and medical maintenance costs.",
        "benefits": "Monthly pension ranging from ₹500 to ₹2,000+ (Central assistance ₹300/month supplemented by state government funds) credited via DBT directly to beneficiary's bank account.",
        "max_benefit_amount": 24000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 79,
            "max_annual_income": 100000,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All", "BPL"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": True,
            "key_rules": [
                "Age of the applicant must be between 18 and 79 years.",
                "Must be a person with severe or multiple disabilities with disability degree of 80% and above.",
                "Household must belong to BPL category."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Disability Certificate issued by Medical Board / UDID Card (showing >=80% disability)",
            "BPL Ration Card / BPL Certificate",
            "Bank Account Passbook"
        ],
        "application_process": "1. Apply via NSAP portal (nsap.nic.in) or at District Social Welfare Office / BDO office. 2. Medical certificate and BPL verification. 3. Sanction and regular monthly DBT pension.",
        "official_url": "https://nsap.nic.in",
        "verification_date": "2026-10-20",
        "source": "National Social Assistance Programme (NSAP) & MoRD",
        "tags": "disability pension, divyang, igndps, severe disability, 80 percent, bpl pension, nsap"
    },
    {
        "code": "ADIP",
        "name": "Assistance to Disabled Persons for Purchase/Fitting of Aids and Appliances (ADIP)",
        "name_hindi": "दिव्यांगजनों के लिए सहायक उपकरण वितरण योजना (एडिप)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Social Justice and Empowerment",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Divyangjan (Persons with Disabilities) needing assistive equipment whose monthly family income is up to ₹30,000",
        "short_description": "Free modern assistive aids and appliances (motorized tricycles, smart canes, hearing aids, wheelchairs, prosthetic limbs).",
        "full_description": "The ADIP Scheme is implemented by ALIMCO (Artificial Limbs Manufacturing Corporation of India) under the Department of Empowerment of Persons with Disabilities (DEPwD). It provides sophisticated, modern, standard aids and appliances to assist persons with disabilities in their physical, social, and economic rehabilitation.",
        "benefits": "Free assistive devices up to ₹15,000 (100% grant for monthly income up to ₹20,000; 50% grant for income ₹20,001 to ₹30,000). For motorized tricycles and wheelchairs, full cost subsidy up to ₹42,000. Cochlear implants for hearing impaired children up to 5 years (₹6.0 Lakh).",
        "max_benefit_amount": 42000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 90,
            "max_annual_income": 360000,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be an Indian citizen with 40% or more disability certified by competent medical authority.",
                "Monthly income from all sources must not exceed ₹30,000 (100% aid for income <= ₹20,000; 50% aid for ₹20,001 to ₹30,000).",
                "Aids provided cannot be replaced within 3 years (1 year for children below 12 years)."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Unique Disability ID (UDID) Card or Medical Disability Certificate (>=40%)",
            "Income Certificate issued by Revenue Authority / MP / MLA / BDO",
            "Passport Size Photograph showing disability"
        ],
        "application_process": "1. Register on ADIP portal (adip.depwd.gov.in) or attend camp organized by ALIMCO / District Social Welfare Officer. 2. Clinical assessment of device suitability. 3. Free device fitted and distributed.",
        "official_url": "https://adip.depwd.gov.in",
        "verification_date": "2026-10-20",
        "source": "DEPwD & ALIMCO (alimco.in)",
        "tags": "adip, assistive devices, wheelchair, motorized tricycle, hearing aid, prosthesis, divyangjan, alimco"
    }
]

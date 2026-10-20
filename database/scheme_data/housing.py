"""
Housing, Water & Rural Infrastructure Schemes Dataset (Verified Official Data)
Sources: Ministry of Rural Development (pmayg.nic.in), Ministry of Housing and Urban Affairs (pmayuclap.gov.in),
Department of Drinking Water and Sanitation (jaljeevanmission.gov.in), Ministry of Panchayati Raj (svamitva.nic.in),
Ministry of New and Renewable Energy (pmsuryaghar.gov.in).
"""

HOUSING_SCHEMES = [
    {
        "code": "PMAY-G",
        "name": "Pradhan Mantri Awas Yojana - Gramin (PMAY-G)",
        "name_hindi": "प्रधानमंत्री आवास योजना - ग्रामीण",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Rural Development",
        "category": "Housing & Shelter",
        "target_audience": "Homeless families and households living in kutcha and dilapidated houses in rural areas",
        "short_description": "Financial assistance of ₹1,20,000 (plain areas) and ₹1,30,000 (hilly/difficult areas) for building a 25 sq.m. pucca house.",
        "full_description": "PMAY-G aims to provide a pucca house with basic amenities to all rural families who are homeless or living in kutcha/dilapidated houses. Beneficiaries are identified using housing deprivation parameters in the SECC 2011 and Awaas+ survey list, verified by the Gram Sabha.",
        "benefits": "Financial grant of ₹1,20,000 in plain areas and ₹1,30,000 in hilly/NE/difficult areas released directly via DBT in 3-4 construction milestones. Convergence with MGNREGA provides 90-95 person-days of unskilled labor wages (approx. ₹20,000+) and ₹12,000 under Swachh Bharat Mission for toilet construction. Free LPG connection under Ujjwala and electricity connection under Saubhagya.",
        "max_benefit_amount": 162000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 85,
            "max_annual_income": 180000,
            "eligible_occupations": ["All", "Agricultural Labourer", "Daily Wage Earner", "Marginal Farmer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All", "SC", "ST", "BPL"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Family must not own a pucca house anywhere in India.",
                "Household must be listed in SECC 2011 permanent waitlist (PWL) or verified Awaas+ survey list.",
                "Houses built must have minimum area of 25 sq.m. including a dedicated hygienic cooking space.",
                "Exclusion criteria: Households possessing motorized 2/3/4-wheelers, mechanized agricultural equipment, or paying income tax are excluded."
            ]
        },
        "required_documents": [
            "Aadhaar Card of all family members",
            "Bank Account Passbook (Aadhaar linked for DBT)",
            "MGNREGA Job Card Number",
            "Consent letter for geo-tagging of existing kutcha house site",
            "Ration Card / SECC Family ID"
        ],
        "application_process": "1. Identification from SECC 2011 / Awaas+ list by Gram Panchayat. 2. Gram Sabha validates priority list. 3. Block Development Officer (BDO) geo-tags kutcha site and sanctions order on AwaasSoft (pmayg.nic.in). 4. Payments released automatically as photos are geo-tagged at foundation, lintel, and roof levels.",
        "official_url": "https://pmayg.nic.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Rural Development (pmayg.nic.in)",
        "tags": "pmay, housing, awas yojana, pucca house, rural housing, home grant, mgnrega convergence"
    },
    {
        "code": "PMAY-U",
        "name": "Pradhan Mantri Awas Yojana - Urban (PMAY-U / BLC)",
        "name_hindi": "प्रधानमंत्री आवास योजना - शहरी",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Housing and Urban Affairs",
        "category": "Housing & Shelter",
        "target_audience": "Economically Weaker Section (EWS) and Low Income Group (LIG) families in statutory towns",
        "short_description": "Central financial assistance of up to ₹1,50,000 for individual house construction / enhancement under Beneficiary-Led Construction (BLC).",
        "full_description": "PMAY-U addresses the housing shortage among urban poor including slum dwellers. Under the Beneficiary-Led individual house Construction/enhancement (BLC) vertical, eligible families belonging to EWS category receive central assistance of ₹1.5 Lakh (supplemented by state government assistance) to build a new pucca house on their own land.",
        "benefits": "Central assistance of ₹1,50,000 per house (combined with state subsidy of ₹50,000 - ₹1,00,000 totaling up to ₹2.5 Lakh). All houses must have toilet, water, electricity, and kitchen. Ownership must be in the name of the female head or joint ownership.",
        "max_benefit_amount": 250000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": 300000,
            "eligible_occupations": ["All", "Street Vendor", "Domestic Worker", "Driver", "Construction Worker"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All", "EWS", "LIG"],
            "max_land_hectares": None,
            "residence_area": ["Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Beneficiary family should not own a pucca house in their name or any family member's name anywhere in India.",
                "Annual household income must be up to ₹3,00,000 for EWS category.",
                "Beneficiary must own clear land title / patta within municipal statutory town limits.",
                "House title must include the adult female head of the family."
            ]
        },
        "required_documents": [
            "Aadhaar Card of all family members",
            "Land Title deed / Registered ownership papers / Urban Patta",
            "Income Certificate issued by Tehsildar / Competent Authority",
            "Bank Account Passbook",
            "Photograph of existing site / kutcha structure"
        ],
        "application_process": "1. Apply online on PMAY-U MIS portal (pmaymis.gov.in) or via municipal corporation / CSC. 2. Urban Local Body conducts biometric and land title verification. 3. Project approved in State Level Sanctioning Committee. 4. Construction funds released in geo-tagged installments.",
        "official_url": "https://pmaymis.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Housing and Urban Affairs & myScheme Portal",
        "tags": "pmay urban, blc, urban housing, house subsidy, ews, slum rehabilitation, municipal corporation"
    },
    {
        "code": "JJM",
        "name": "Jal Jeevan Mission (Har Ghar Jal)",
        "name_hindi": "जल जीवन मिशन (हर घर जल)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Jal Shakti",
        "category": "Housing & Shelter",
        "target_audience": "Every rural household across all villages of India",
        "short_description": "Functional Household Tap Connection (FHTC) providing 55 liters per capita per day of potable drinking water on a long-term basis.",
        "full_description": "Jal Jeevan Mission aims to provide safe and adequate drinking water through individual Functional Household Tap Connections (FHTC) to all rural households in India. Emphasizes community-led water management, greywater treatment, rainwater harvesting, and water quality testing by Village Water & Sanitation Committees (VWSC) / Paani Samitis.",
        "benefits": "Free installation of piped drinking water tap connection directly inside household premises. Supply of tested potable water (minimum 55 liters per person per day) meeting BIS 10500 standards, eliminating water fetching drudgery for women and girls.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Universal coverage: Every rural household located in the village revenue area.",
                "Schools, Anganwadi centres, Gram Panchayat buildings, and health sub-centres also receive free connections."
            ]
        },
        "required_documents": [
            "Aadhaar Card (for household head verification on JJM dashboard)",
            "Gram Panchayat residence proof"
        ],
        "application_process": "Approach Village Water and Sanitation Committee (VWSC) or Gram Panchayat. Piped distribution network and tap metering is implemented community-wide under Village Action Plan (VAP).",
        "official_url": "https://jaljeevanmission.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Drinking Water & Sanitation, Ministry of Jal Shakti",
        "tags": "jal jeevan, drinking water, tap water, har ghar jal, rural water, paani samiti, water connection"
    },
    {
        "code": "SBM-G",
        "name": "Swachh Bharat Mission - Gramin (SBM-G)",
        "name_hindi": "स्वच्छ भारत मिशन - ग्रामीण",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Jal Shakti",
        "category": "Housing & Shelter",
        "target_audience": "BPL households and identified APL vulnerable households lacking individual household latrines",
        "short_description": "Direct financial incentive of ₹12,000 for constructing an Individual Household Latrine (IHHL) with twin-pit safe technology.",
        "full_description": "SBM-G Phase-II focuses on sustaining Open Defecation Free (ODF) status and management of solid and liquid waste (ODF Plus). The scheme provides ₹12,000 financial assistance for the construction of individual household latrines (IHHL) to newly formed households and left-out eligible families in rural villages.",
        "benefits": "Direct cash incentive of ₹12,000 per household credited via DBT into the beneficiary's bank account upon completion and geo-tagging of the toilet structure.",
        "max_benefit_amount": 12000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 85,
            "max_annual_income": 200000,
            "eligible_occupations": ["All", "Agricultural Labourer", "Small Farmer", "Daily Wage Earner"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All", "SC", "ST", "BPL", "Small/Marginal Farmer"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Household must not have an existing functional toilet.",
                "Eligible categories: All BPL households, and APL households belonging to SC/ST, Small & Marginal Farmers, Landless labourers with homestead, Physically handicapped, and Women-headed households.",
                "Toilet must be constructed using twin-pit pour-flush technology."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Bank Account Passbook (Aadhaar linked)",
            "Ration Card / BPL card / Category certificate",
            "Photograph of applicant alongside newly constructed toilet"
        ],
        "application_process": "1. Apply online via sbm.gov.in or submit form to Village Swachhata Dooth / Gram Panchayat. 2. Field verification and geo-tagging of pit digging. 3. Completion inspection and photo upload. 4. DBT credit of ₹12,000 into bank account.",
        "official_url": "https://swachhbharatmission.ddws.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Drinking Water and Sanitation & myScheme Portal",
        "tags": "toilet subsidy, swachh bharat, ihhl, sanitation, rural latrine, 12000 incentive, odf"
    },
    {
        "code": "PM-SURYAGHAR",
        "name": "PM Surya Ghar: Muft Bijli Yojana",
        "name_hindi": "पीएम सूर्य घर: मुफ्त बिजली योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of New and Renewable Energy",
        "category": "Housing & Shelter",
        "target_audience": "Residential households possessing a grid-connected electricity connection and suitable rooftop space",
        "short_description": "Central financial subsidy of up to ₹78,000 for installing residential rooftop solar panels, providing up to 300 units of free power per month.",
        "full_description": "Flagship national rooftop solar initiative aimed at lighting up 1 crore households with free electricity generated from solar power. Provides direct capital subsidy of ₹30,000 for 1 kW systems, ₹60,000 for 2 kW systems, and ₹78,000 for systems of 3 kW or higher, along with concessional collateral-free bank loans at ~7% interest rate.",
        "benefits": "Capital subsidy of ₹30,000 for 1 kW, ₹60,000 for 2 kW, and ₹78,000 for 3 kW+ rooftop solar systems directly credited to bank account via DBT within 30 days of net meter commissioning. Saves up to ₹1,500 - ₹2,500 monthly on electricity bills and allows selling surplus solar power back to DISCOM.",
        "max_benefit_amount": 78000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 80,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be an Indian citizen with a valid residential electricity connection in their name.",
                "Rooftop area must be structurally sound and free from shadow.",
                "Solar panels and inverters must adhere to ALMM (Approved List of Models and Manufacturers) domestic content criteria.",
                "Must install a bi-directional net meter through the local DISCOM."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Latest Residential Electricity Bill (showing Consumer Account Number)",
            "Rooftop Ownership proof / House property tax receipt",
            "Aadhaar-seeded Bank Account Passbook / Cancelled Cheque",
            "Passport Size Photograph"
        ],
        "application_process": "1. Register on National Portal (pmsuryaghar.gov.in) with State, DISCOM name, and Consumer Number. 2. Submit rooftop application. 3. Receive technical feasibility approval from DISCOM. 4. Empaneled vendor installs system. 5. Net meter inspection and commissioning. 6. Subsidy released directly to bank account via DBT within 30 days.",
        "official_url": "https://pmsuryaghar.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of New and Renewable Energy (pmsuryaghar.gov.in)",
        "tags": "solar rooftop, free electricity, muft bijli, surya ghar, solar subsidy, 78000 subsidy, clean energy"
    },
    {
        "code": "SVAMITVA",
        "name": "SVAMITVA Scheme (Survey of Villages and Mapping with Improvised Technology)",
        "name_hindi": "स्वामित्व योजना (संपत्ति कार्ड)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Panchayati Raj",
        "category": "Housing & Shelter",
        "target_audience": "Rural property owners residing in populated (Abadi) areas of villages",
        "short_description": "Legal ownership Property Card (Sampatti Patra) issued using high-resolution drone mapping of rural residential land.",
        "full_description": "Central sector scheme that uses drone surveying technology to map inhabited land parcels in rural areas (Abadi). Provides rural citizens with official, legally validated Property Cards ('Sampatti Patra' / Title Deeds), enabling them to monetize residential assets as collateral for bank loans, resolving boundary disputes, and aiding Gram Panchayat tax planning.",
        "benefits": "Free official Property Card ('Sampatti Patra') providing clear legal title of residential houses in rural abadi land. Enables access to institutional home loans and business credit using village property as formal collateral.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 100,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a bonafide resident and owner of a residential structure in the village Abadi area surveyed by Survey of India.",
                "Boundaries marked (chuna marking) during village ground truthing."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Gram Panchayat Voter ID / Family register extract",
            "Any historical house possession paper or electricity receipt"
        ],
        "application_process": "1. Survey of India conducts drone flights over village Abadi in coordination with Revenue Department. 2. Property owners mark boundaries with lime powder (chuna). 3. Inquiry officer hears objections and finalizes maps. 4. Digital Property Card delivered to mobile phone and physical card distributed by District Collector.",
        "official_url": "https://svamitva.nic.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Panchayati Raj & Survey of India",
        "tags": "svamitva, property card, drone survey, sampatti patra, rural house ownership, land title, abadi"
    }
]

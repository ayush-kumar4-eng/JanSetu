"""
Agriculture & Farmers Welfare Schemes Dataset (Verified Official Data)
Sources: myScheme (myscheme.gov.in), Ministry of Agriculture & Farmers Welfare, Ministry of Fisheries, Animal Husbandry & Dairying.
"""

AGRICULTURE_SCHEMES = [
    {
        "code": "PM-KISAN",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "name_hindi": "प्रधानमंत्री किसान सम्मान निधि",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Small, marginal, and all landholding farmer families across India",
        "short_description": "Direct income support of ₹6,000 per year in three equal installments of ₹2,000 directly into the bank accounts of farmer families.",
        "full_description": "PM-KISAN is a central sector scheme with 100% funding from Government of India. It aims to supplement the financial needs of landholding farmers in procuring various inputs to ensure proper crop health and appropriate yields, commensurate with the anticipated farm income.",
        "benefits": "₹6,000 per annum paid in three 4-monthly installments of ₹2,000 each directly transferred via DBT into Aadhaar-seeded bank accounts.",
        "max_benefit_amount": 6000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 85,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Cultivator", "Agricultural Worker", "Small Landholder"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be a landholder farmer family with cultivable land in their name in state land records.",
                "Institutional landholders, constitutional post holders, serving/retired government officers, and income tax payers in the last assessment year are excluded.",
                "Bank account must be Aadhaar-linked with e-KYC completed."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Holding Documents (Khatauni / RoR / Jamabandi)",
            "Bank Account Passbook (Aadhaar Seeded)",
            "Active Mobile Number for OTP verification"
        ],
        "application_process": "1. Visit PM-KISAN portal (pmkisan.gov.in) or nearest Common Service Centre (CSC). 2. Submit New Farmer Registration with Aadhaar and Land Khatauni details. 3. Complete biometric or OTP-based e-KYC. 4. Verification by State Nodal Officer.",
        "official_url": "https://pmkisan.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & PM-KISAN Portal",
        "tags": "farmer, dbt, direct benefit, agriculture, kisan, income support, crop input"
    },
    {
        "code": "PMFBY",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "name_hindi": "प्रधानमंत्री फसल बीमा योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "All farmers growing notified crops in notified areas including sharecroppers and tenant farmers",
        "short_description": "Comprehensive risk insurance cover against non-preventable natural risks from pre-sowing to post-harvest.",
        "full_description": "PMFBY provides comprehensive crop insurance coverage against losses caused by natural disasters, pests, and diseases. Farmers pay a nominal uniform premium of 2% for Kharif crops, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops, with the balance subsidized by the Government.",
        "benefits": "Full sum insured payout based on threshold yield deficit. Comprehensive cover for localized calamities, prevented sowing, mid-season adversity, and post-harvest losses within 14 days of harvest.",
        "max_benefit_amount": 200000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Sharecropper", "Tenant Farmer", "Cultivator"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be growing notified crops in notified insurance areas during the designated season.",
                "Non-loanee farmers must provide land ownership documents or registered tenancy/sharecropper agreement.",
                "Loss intimation must be submitted within 72 hours of localized disaster (hailstorm, landslide, inundation)."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Records (Khasra/Khatauni/Patta)",
            "Sowing Certificate issued by Patwari / Village Agricultural Officer",
            "Bank Account Passbook",
            "Tenancy Agreement (for tenant farmers)"
        ],
        "application_process": "1. Apply via National Crop Insurance Portal (pmfby.gov.in) or through bank branch / CSC / insurance intermediary. 2. Select crop season, district, and survey number. 3. Pay farmer share of premium. 4. Policy receipt generated immediately.",
        "official_url": "https://pmfby.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & PMFBY National Portal",
        "tags": "crop insurance, disaster relief, fasal bima, drought, flood, hailstorm, farmers"
    },
    {
        "code": "KCC",
        "name": "Kisan Credit Card (KCC) Scheme",
        "name_hindi": "किसान क्रेडिट कार्ड योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Farmers, individual/joint cultivators, tenant farmers, self-help groups, animal husbandry and fisheries farmers",
        "short_description": "Timely access to affordable institutional credit with concessional interest rates for agricultural, animal husbandry, and fisheries operations.",
        "full_description": "Kisan Credit Card facilitates short-term credit requirements for cultivation of crops, post-harvest expenses, consumption requirements of farmer households, working capital for maintenance of farm assets, and activities allied to agriculture. Farmers receive interest subvention of 2% and prompt repayment incentive of 3%, bringing effective interest rate down to 4% p.a. on loans up to ₹3 Lakh.",
        "benefits": "Short-term credit up to ₹3,00,000 at effective subsidized interest rate of 4% per annum upon prompt repayment. Collateral-free loan up to ₹1.60 Lakh (extended to ₹2 Lakh for tie-up). Flexible revolving cash credit.",
        "max_benefit_amount": 300000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Dairy Farmer", "Fisherman", "Poultry Farmer", "Tenant Farmer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Individual or joint borrower farmers who are owner cultivators or legal tenants.",
                "Co-applicant mandatory if applicant age is above 60 years.",
                "Animal husbandry and fisheries farmers are eligible for working capital limit up to ₹2 Lakh within the overall ₹3 Lakh ceiling."
            ]
        },
        "required_documents": [
            "Duly filled KCC Application Form",
            "Aadhaar Card / Voter ID",
            "Land title deeds / revenue records / lease agreement",
            "Passport size photographs",
            "No Dues Certificate (if borrowing beyond collateral limit)"
        ],
        "application_process": "1. Fill 1-page simplified KCC form at commercial bank, RRB, cooperative bank, or online on JanSamarth portal (jansamarth.in). 2. Submit land documents and KYC. 3. Bank sanctions credit limit within 14 days and issues RuPay KCC card.",
        "official_url": "https://myscheme.gov.in/schemes/kcc",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & Department of Financial Services (DFS)",
        "tags": "kcc, credit card, loan, subsidized interest, farm loan, working capital, animal husbandry"
    },
    {
        "code": "PMKSY-PDMC",
        "name": "Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PDMC)",
        "name_hindi": "प्रधानमंत्री कृषि सिंचाई योजना - प्रति बूंद अधिक फसल",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "All farmer categories adopting micro-irrigation (Drip and Sprinkler systems)",
        "short_description": "Financial subsidy of 55% for small/marginal farmers and 45% for other farmers to install precision micro-irrigation systems.",
        "full_description": "PDMC focuses on enhancing water use efficiency at farm level through micro-irrigation technologies like drip and sprinkler irrigation systems. It promotes precision water management, reduces fertilizer wastage via fertigation, and improves crop yields significantly.",
        "benefits": "Financial assistance of 55% of benchmark cost for Small and Marginal farmers, and 45% for other farmers for installing drip and sprinkler irrigation systems.",
        "max_benefit_amount": 100000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Horticulturist", "Floriculturist"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": 5.0,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must possess cultivable agricultural land with assured water source (borewell, open well, canal, or farm pond).",
                "Beneficiary must not have received micro-irrigation subsidy for the same survey number in the preceding 7 years.",
                "Small and marginal farmers receive higher subsidy support (55%)."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Ownership Records (Jamabandi/7-12 extract/Khatauni)",
            "Water Source Proof / Electricity Connection Certificate",
            "Bank Passbook",
            "Soil and Water Test Report (where mandated by state)"
        ],
        "application_process": "1. Register on state horticulture/agriculture portal or micro-irrigation MIS portal. 2. Select empanelled micro-irrigation manufacturer. 3. Field inspection by Agriculture Officer. 4. Subsidy released directly to farmer account or vendor upon installation verification.",
        "official_url": "https://pmksy.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & PMKSY Official Portal",
        "tags": "irrigation, drip irrigation, sprinkler, water saving, subsidy, horticulture, farm efficiency"
    },
    {
        "code": "PM-KMY",
        "name": "Pradhan Mantri Kisan Maandhan Yojana (PM-KMY)",
        "name_hindi": "प्रधानमंत्री किसान मानधन योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Social Welfare & Empowerment",
        "target_audience": "Small and Marginal Farmers (SMFs) owning cultivable land up to 2 hectares aged 18 to 40 years",
        "short_description": "Voluntary and contributory pension scheme providing assured monthly pension of ₹3,000 after reaching 60 years of age.",
        "full_description": "PM-KMY provides social security to small and marginal farmers in their old age. Farmers contribute a monthly amount ranging between ₹55 to ₹200 depending on entry age (18 to 40 years), with an equal matching contribution made by the Central Government. The pension fund is managed by Life Insurance Corporation of India (LIC).",
        "benefits": "Assured monthly pension of ₹3,000 directly deposited into bank account upon reaching 60 years of age. Family pension of 50% (₹1,500/month) to spouse in case of subscriber death.",
        "max_benefit_amount": 36000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 40,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Small Landholder", "Marginal Farmer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": 2.0,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Must be a small or marginal farmer with cultivable landholding up to 2 hectares in state land records.",
                "Must be aged between 18 and 40 years at time of enrolment.",
                "Should not be covered under other statutory social security schemes like NPS, ESIC, EPFO or PM-SYM.",
                "Income tax payees are excluded."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Khasra/Khatauni land record proving landholding up to 2 hectares",
            "Savings Bank Account Passbook / Cheque for auto-debit",
            "Nominee details"
        ],
        "application_process": "1. Visit nearest Common Service Centre (CSC) or self-enrol via maandhan.in. 2. Provide Aadhaar and bank account details. 3. System calculates monthly contribution based on age. 4. Auto-debit mandate signed and Kisan Pension Card issued.",
        "official_url": "https://maandhan.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & Ministry of Agriculture",
        "tags": "pension, small farmer, social security, monthly pension, old age, maandhan, lic"
    },
    {
        "code": "PM-KUSUM",
        "name": "PM-KUSUM (Kisan Urja Suraksha evam Utthaan Mahabhiyan)",
        "name_hindi": "पीएम कुसुम योजना (सोलर कृषि पंप)",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of New and Renewable Energy",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Individual farmers, farmer groups, cooperatives, water user associations, and panchayats",
        "short_description": "Up to 60% subsidy for setting up standalone off-grid solar agriculture pumps and solarization of grid-connected agriculture pumps.",
        "full_description": "PM-KUSUM scheme enables farmers to de-dieselise the agricultural sector and generate income from barren/uncultivable land. Component-B provides 30% Central Financial Assistance and 30% State subsidy for installing standalone solar agriculture pumps up to 7.5 HP, with farmers contributing only 40% (or 10% cash + 30% bank loan).",
        "benefits": "60% subsidy (30% Central Govt + 30% State Govt) on standalone solar water pumps. Farmer pays only 10% upfront, with remaining 30% available as bank loan. Reliable daytime irrigation and zero electricity/diesel bills.",
        "max_benefit_amount": 150000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Cultivator", "Dairy Farmer"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must possess agricultural land with an existing water source (borewell/open well).",
                "For standalone pumps (Component B), area must be non-grid connected or suffering from irregular power.",
                "Beneficiaries must have valid land title or certified tenancy rights."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Ownership Documents (Jamabandi/Khasra/Khatauni)",
            "Bank Account Passbook",
            "Electricity connection certificate (or declaration of no grid connection)",
            "Passport photograph"
        ],
        "application_process": "1. Apply online via state nodal renewable energy agency portal (e.g. RREC in Rajasthan, MEDA in Maharashtra). 2. Submit land documents and pump HP requirement. 3. Pay farmer share (10% to 40%). 4. Certified vendor installs solar pump and tests water discharge.",
        "official_url": "https://pmkusum.mnre.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & MNRE Official Portal",
        "tags": "solar pump, renewable energy, irrigation, kusum, electricity, agriculture, green energy"
    },
    {
        "code": "SMAM",
        "name": "Sub-Mission on Agricultural Mechanization (SMAM)",
        "name_hindi": "कृषि यंत्रीकरण उप-मिशन",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Small, marginal, SC, ST, and women farmers seeking modern farm machinery",
        "short_description": "40% to 50% financial subsidy on procurement of tractors, power tillers, rotavators, harvesters, and establishment of Custom Hiring Centres.",
        "full_description": "SMAM aims to increase the reach of farm mechanization to small and marginal farmers and to regions where availability of farm power is low. It promotes Custom Hiring Centres (CHCs) to offset high cost of purchasing equipment for individual farmers.",
        "benefits": "40% to 50% subsidy on purchase of agricultural machinery (up to ₹1.25 Lakh on small tractors/power tillers, and up to ₹10 Lakh subsidy for establishing Custom Hiring Centres).",
        "max_benefit_amount": 125000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 70,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Agricultural Entrepreneur"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be an active farmer possessing registered agricultural land.",
                "Women, SC, and ST farmers are accorded higher priority and 50% subsidy rate.",
                "Only one tractor/power equipment subsidy permitted per family within a 7-year block."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Record (Khasra/Khatauni)",
            "Bank Passbook copy",
            "Caste Certificate (for SC/ST beneficiaries)",
            "Quotation from authorized implement dealer"
        ],
        "application_process": "1. Register on DBT Agricultural Mechanization portal (agrimachinery.nic.in). 2. Select implement and upload dealer quotation. 3. Approval by District Agriculture Department. 4. Purchase machine and receive DBT subsidy in bank account.",
        "official_url": "https://agrimachinery.nic.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & Department of Agriculture",
        "tags": "tractor subsidy, farm machinery, mechanization, rotavator, power tiller, custom hiring centre"
    },
    {
        "code": "PMMSY",
        "name": "Pradhan Mantri Matsya Sampada Yojana (PMMSY)",
        "name_hindi": "प्रधानमंत्री मत्स्य संपदा योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Fisheries, Animal Husbandry and Dairying",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Fishers, fish farmers, fish workers, SHGs, JLGs, fisheries cooperatives, and entrepreneurs",
        "short_description": "40% to 60% financial assistance for aquaculture pond construction, biofloc, RAS, boats, nets, and cold chain logistics.",
        "full_description": "PMMSY is an umbrella scheme to bring about the Blue Revolution through sustainable development of the fisheries sector in India. It addresses critical gaps in fish production, productivity, quality, technology, post-harvest infrastructure, and modernization of the value chain.",
        "benefits": "Financial grant of 40% of project cost for General category and 60% for SC, ST, and Women beneficiaries across freshwater aquaculture, biofloc, cold storage, and motorization of traditional fishing crafts.",
        "max_benefit_amount": 300000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 70,
            "max_annual_income": None,
            "eligible_occupations": ["Fisherman", "Fish Farmer", "Aquaculturist", "Fish Vendor"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Coastal", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must possess own land or minimum 7-10 years leasehold rights for pond/RAS construction.",
                "Coastal fishers must have registered fishing vessel license with fisheries department.",
                "Women, SC, and ST applicants receive maximum 60% subsidy rate."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Fisherman Identity Card / Biometric ID",
            "Land / Pond ownership or lease agreement",
            "Detailed Project Report (DPR) / Technical estimate",
            "Bank Account Passbook"
        ],
        "application_process": "1. Apply on PMMSY portal (pmmsy.dof.gov.in) or submit proposal to District Fisheries Officer (DFO). 2. Scrutiny by District Level Committee (DLC). 3. Sanction letter issued. 4. Release of phased milestone subsidy via DBT.",
        "official_url": "https://pmmsy.dof.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & Department of Fisheries",
        "tags": "fisheries, aquaculture, fish farming, biofloc, blue revolution, boat subsidy, fisherman"
    },
    {
        "code": "RGM",
        "name": "Rashtriya Gokul Mission (RGM)",
        "name_hindi": "राष्ट्रीय गोकुल मिशन",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Fisheries, Animal Husbandry and Dairying",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Dairy farmers, rural youth, private entrepreneurs, FPOs, and cooperatives",
        "short_description": "Up to 50% capital subsidy (up to ₹2 Crore) for establishing breed multiplication farms and sex-sorted semen facilities.",
        "full_description": "Rashtriya Gokul Mission is implemented for development and conservation of indigenous bovine breeds, genetic upgradation of the bovine population, and enhancement of milk production and productivity. It provides capital subsidies to entrepreneurs for setting up modern dairy breeding farms.",
        "benefits": "50% capital subsidy up to ₹2 Crore for setting up Breed Multiplication Farms (minimum 200 indigenous cows/buffaloes) and 50% subsidy up to ₹25 Lakh for silage making units and high-yielding heifer units.",
        "max_benefit_amount": 2000000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 65,
            "max_annual_income": None,
            "eligible_occupations": ["Dairy Farmer", "Agri-Entrepreneur", "Cattle Breeder"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must possess land (minimum 5 acres for 200 cows) or long-term registered lease.",
                "Must arrange remaining 50% project cost through bank loan or self-financing.",
                "Entrepreneur must have relevant experience or certified training in dairy farming/animal husbandry."
            ]
        },
        "required_documents": [
            "Aadhaar Card and PAN Card",
            "Land title deeds / lease agreement",
            "Bank loan sanction letter (for loan-linked portion)",
            "Detailed Project Report (DPR) approved by veterinary consultant",
            "Dairy training certificate"
        ],
        "application_process": "1. Apply online through National Livestock Mission / RGM portal (nlm.udyamimitra.in). 2. Submit DPR and bank sanction. 3. Appraisal by State Livestock Development Board and approval by Central Monitoring Committee.",
        "official_url": "https://dahd.nic.in/rashtriya-gokul-mission",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & DAHD Portal",
        "tags": "dairy, cattle breeding, indigenous cow, gokul mission, milk production, animal husbandry"
    },
    {
        "code": "PKVY",
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "name_hindi": "परम्परागत कृषि विकास योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "Farmer clusters, SHGs, and traditional farmers transitioning to organic cultivation",
        "short_description": "Financial assistance of ₹50,000 per hectare for 3 years to adopt organic farming and Participatory Guarantee System (PGS) certification.",
        "full_description": "PKVY promotes organic farming through a cluster approach and PGS-India certification. It supports organic input production, on-farm composting, packaging, organic branding, and linkage to domestic and international organic markets.",
        "benefits": "₹50,000 per hectare for 3 years, of which ₹31,000 is given directly via DBT for organic inputs (bio-fertilizers, vermicompost, botanical extracts) and ₹19,000 for cluster formation, PGS certification, and marketing.",
        "max_benefit_amount": 50000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Organic Cultivator"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": 2.0,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Farmers must form a cluster of minimum 20 hectares (or 50 farmers) in contiguous agricultural land.",
                "Individual farmer ceiling for assistance is 2 hectares.",
                "Commitment to discontinue synthetic chemical fertilizers and pesticides."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Ownership Records (Khatauni/Khasra)",
            "Bank Account Passbook",
            "Cluster Member Resolution / Farmer Group Agreement"
        ],
        "application_process": "1. Mobilize farmer cluster and register through District Agriculture Officer / Regional Lead Agency. 2. Register group on PGS-India portal (pgsindia-ncof.gov.in). 3. Periodic peer appraisals and DBT input credit.",
        "official_url": "https://pgsindia-ncof.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & INM Division, MoAFW",
        "tags": "organic farming, biofertilizer, vermicompost, pgs certification, sustainable agriculture, pkvy"
    },
    {
        "code": "AIF",
        "name": "Agriculture Infrastructure Fund (AIF)",
        "name_hindi": "कृषि अवसंरचना कोष",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Farmers, FPOs, PACS, Agri-entrepreneurs, and start-ups building post-harvest infrastructure",
        "short_description": "3% per annum interest subvention on bank loans up to ₹2 Crore for setting up cold storage, warehouses, sorting/grading units, and silos.",
        "full_description": "AIF provides a medium-long term debt financing facility for investment in viable projects for post-harvest management infrastructure and community farming assets. Loans have an interest subvention of 3% p.a. for up to 7 years and credit guarantee coverage under CGTMSE for loans up to ₹2 Crore.",
        "benefits": "3% per annum interest subvention on term loans up to ₹2 Crore for up to 7 years. Credit guarantee fee paid by government under CGTMSE. Repayment moratorium up to 2 years.",
        "max_benefit_amount": 2000000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 70,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Agri-Entrepreneur", "FPO Director", "PACS Secretary"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Semi-Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Project must create post-harvest management infrastructure or community farming assets.",
                "Interest subvention available on maximum loan of ₹2 Crore per project (up to 25 projects across different locations).",
                "Borrower must obtain formal bank loan sanction from participating commercial/cooperative banks."
            ]
        },
        "required_documents": [
            "Aadhaar and PAN Card",
            "Detailed Project Report (DPR) with financial viability",
            "Land ownership / long lease document for facility site",
            "Bank In-principle / Sanction Letter",
            "FPO / Company incorporation papers (if applicable)"
        ],
        "application_process": "1. Register on AIF portal (agriinfra.dac.gov.in). 2. Submit DPR and select preferred lending bank. 3. Ministry scrutiny within 7 days. 4. Bank disburses loan with integrated 3% interest subvention.",
        "official_url": "https://agriinfra.dac.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & Department of Agriculture",
        "tags": "cold storage, warehouse, food processing, agri infrastructure, interest subsidy, loan, post harvest"
    },
    {
        "code": "SHC",
        "name": "Soil Health Card (SHC) Scheme",
        "name_hindi": "मृदा स्वास्थ्य कार्ड योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "category": "Agriculture, Rural & Environment",
        "target_audience": "All farmers cultivating agricultural land across India",
        "short_description": "Free soil nutrient testing and customized fertilizer recommendation card issued to every farmer every 3 years.",
        "full_description": "The Soil Health Card scheme assesses the nutrient status of soil across 12 parameters: N, P, K (macro-nutrients); S (secondary nutrient); Zn, Fe, Cu, Mn, Bo (micro-nutrients); and pH, EC, OC (physical parameters). It provides crop-wise fertilizer dosage recommendations to lower input costs and prevent soil degradation.",
        "benefits": "Free diagnostic report on 12 soil parameters with customized dosage recommendations for urea, DAP, micronutrients, and bio-fertilizers. Helps cut input costs by 15-20% and improve yields by 10-15%.",
        "max_benefit_amount": 0,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 85,
            "max_annual_income": None,
            "eligible_occupations": ["Farmer", "Tenant Farmer", "Sharecropper"],
            "eligible_genders": ["All"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural"],
            "is_bpl_required": False,
            "key_rules": [
                "Farmer must hold agricultural land in the village grid selected for cycle testing.",
                "Soil sample collected by Agriculture Extension Officer in presence of farmer."
            ]
        },
        "required_documents": [
            "Aadhaar Card",
            "Land Record (Khasra Number / Survey Number)",
            "Active Mobile Number"
        ],
        "application_process": "1. Approach local Village Agriculture Assistant / Krishi Vigyan Kendra (KVK). 2. Soil sample taken from field with GPS coordinates. 3. Laboratory testing conducted. 4. Printed Soil Health Card delivered or downloaded via soilhealth.dac.gov.in.",
        "official_url": "https://soilhealth.dac.gov.in",
        "verification_date": "2026-10-20",
        "source": "myScheme Portal (myscheme.gov.in) & Department of Agriculture",
        "tags": "soil health, fertilizer, nutrient management, crop yield, free testing, soil health card"
    }
]

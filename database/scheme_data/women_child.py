"""
Women & Child Welfare Schemes Dataset (Verified Official Data)
Sources: Ministry of Women and Child Development (wcd.nic.in), Department of Financial Services,
Ministry of Petroleum and Natural Gas.
"""

WOMEN_CHILD_SCHEMES = [
    {
        "code": "PMMVY",
        "name": "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
        "name_hindi": "प्रधानमंत्री मातृ वंदना योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Women and Child Development",
        "category": "Women & Child",
        "target_audience": "Pregnant Women and Lactating Mothers (PW&LM) belonging to socially and economically disadvantaged sections",
        "short_description": "Maternity benefit cash incentive of ₹5,000 for the first child and ₹6,000 for the second child (if girl) directly via DBT.",
        "full_description": "Centrally sponsored conditional cash transfer scheme implemented under Mission Shakti (Samarthya). It provides partial compensation for wage loss in terms of cash incentive so that the woman can take adequate rest before and after delivery of the first child, and promotes healthy nutrition practices and institutional delivery.",
        "benefits": "₹5,000 in two installments (₹3,000 upon early ANC registration and ₹2,000 after child birth and first cycle of immunization) for the first child. For the second child, ₹6,000 in a single installment if the newborn is a girl child.",
        "max_benefit_amount": 6000,
        "eligibility_criteria": {
            "min_age": 19,
            "max_age": 45,
            "max_annual_income": 800000,
            "eligible_occupations": ["All"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All", "SC", "ST", "BPL", "EWS"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Pregnant women and lactating mothers for first living child; or for second child if newborn is a girl.",
                "Must belong to eligible categories: SC/ST, Divyangjan, E-shram card holders, BPL ration card holders, PMJAY card holders, or net family income less than ₹8 Lakh.",
                "Women in regular employment with Central/State Govt or PSUs are excluded (as they receive paid maternity leave)."
            ]
        },
        "required_documents": [
            "Mother's and Father's Aadhaar Card",
            "Mother and Child Protection (MCP) Card",
            "Eligibility proof (E-shram card, SC/ST certificate, Ration Card, or Income proof)",
            "Mother's Aadhaar-linked Bank Account Passbook",
            "Child Birth Certificate (for second installment / second child)"
        ],
        "application_process": "1. Apply online via PMMVY Portal (pmmvy.wcd.gov.in) or submit Form 1A/1B at local Anganwadi Centre / ASHA worker. 2. Verification by Anganwadi Worker (AWW) and Child Development Project Officer (CDPO). 3. Direct DBT credit via PFMS.",
        "official_url": "https://pmmvy.wcd.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Women and Child Development & myScheme Portal",
        "tags": "maternity benefit, pmmvy, pregnancy, cash incentive, mother, newborn girl, nutrition, dbt"
    },
    {
        "code": "SSY",
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "name_hindi": "सुकन्या समृद्धि योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Parents or legal guardians of a girl child below 10 years of age",
        "short_description": "High-interest (8.2% p.a.) small savings government scheme with Section 80C tax exemption and tax-free maturity for girl's education/marriage.",
        "full_description": "Launched under the Beti Bachao Beti Padhao campaign, SSY is a dedicated government-backed savings initiative for girl children. It offers one of the highest sovereign interest rates among small savings schemes (8.2% p.a. compounded annually) and complete EEE (Exempt-Exempt-Exempt) tax benefits under the Income Tax Act.",
        "benefits": "Attractive sovereign interest rate of 8.2% p.a. Minimum deposit of only ₹250/year up to maximum ₹1,50,000/year. Deposits can be made for 15 years, with account maturing after 21 years. Partial withdrawal up to 50% allowed after age 18 for higher education.",
        "max_benefit_amount": 150000,
        "eligibility_criteria": {
            "min_age": 0,
            "max_age": 10,
            "max_annual_income": None,
            "eligible_occupations": ["All"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Account can be opened by natural or legal guardian in the name of a girl child from her birth till she attains 10 years of age.",
                "Maximum of two accounts permitted per family (one for each girl child; exception for twins/triplets).",
                "Account operates till the girl reaches 21 years of age or upon marriage after age 18."
            ]
        },
        "required_documents": [
            "Birth Certificate of the girl child",
            "Aadhaar Card and PAN of parent/guardian",
            "Address proof of parent/guardian",
            "Passport size photos of child and guardian"
        ],
        "application_process": "1. Visit any Post Office branch or authorized commercial bank (SBI, PNB, BoB, etc.). 2. Fill SSY account opening form. 3. Deposit initial minimum amount of ₹250. 4. SSY passbook issued.",
        "official_url": "https://www.indiapost.gov.in/Financial/pages/content/sukanya-samriddhi-account.aspx",
        "verification_date": "2026-10-20",
        "source": "India Post & Department of Economic Affairs, Ministry of Finance",
        "tags": "sukanya samriddhi, ssy, girl child, high interest, savings, tax exemption 80c, beti bachao"
    },
    {
        "code": "PMUY",
        "name": "Pradhan Mantri Ujjwala Yojana 2.0 (PMUY)",
        "name_hindi": "प्रधानमंत्री उज्ज्वला योजना 2.0",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Petroleum and Natural Gas",
        "category": "Women & Child",
        "target_audience": "Adult women belonging to poor households without existing LPG connection",
        "short_description": "Deposit-free LPG connection, free first cylinder refill, free hotplate stove, and ₹300 per cylinder targeted subsidy.",
        "full_description": "PMUY was launched to safeguard the health of women and children by providing them with a clean cooking fuel (LPG). Under Ujjwala 2.0, beneficiaries receive a deposit-free LPG connection, along with a free first cylinder refill and a free hotplate stove, requiring minimal documentation for migrants through self-declaration.",
        "benefits": "Free deposit-free LPG gas connection (security deposit for cylinder and pressure regulator borne by Central Govt). Free first 14.2 kg LPG refill and free gas stove. Ongoing targeted subsidy of ₹300 per cylinder for up to 12 refills per year directly into bank account.",
        "max_benefit_amount": 4500,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 75,
            "max_annual_income": 250000,
            "eligible_occupations": ["All", "Homemaker", "Daily Wage Earner", "Agricultural Worker"],
            "eligible_genders": ["Female"],
            "eligible_categories": ["All", "SC", "ST", "BPL", "OBC", "General"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Applicant must be an adult woman aged 18 years or older.",
                "There must not be any other active LPG connection in the same household.",
                "Must belong to poor categories: SC/ST, PMAY-Gramin beneficiaries, Antyodaya Anna Yojana (AAY), Most Backward Classes, Forest Dwellers, Tea Garden Tribes, or 14-point declaration of poor household."
            ]
        },
        "required_documents": [
            "Aadhaar Card of applicant and adult family members",
            "Ration Card issued by State Govt / Family Composition Certificate",
            "Bank Account Passbook (Aadhaar linked)",
            "Self-declaration for migrant address proof (if residing away from home)"
        ],
        "application_process": "1. Apply online via pmuy.gov.in or visit nearest LPG distributor (Indane, Bharatgas, HP Gas). 2. Submit e-KYC with Aadhaar. 3. Oil Marketing Company verifies de-duplication. 4. Free cylinder, regulator, pipe, and stove delivered to home.",
        "official_url": "https://www.pmuy.gov.in",
        "verification_date": "2026-10-20",
        "source": "Ministry of Petroleum and Natural Gas & myScheme Portal",
        "tags": "ujjwala, lpg connection, gas cylinder, clean cooking fuel, free stove, women health, subsidy"
    },
    {
        "code": "STANDUP-INDIA",
        "name": "Stand-Up India Scheme for Women and SC/ST Entrepreneurs",
        "name_hindi": "स्टैंड-अप इंडिया योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Women and SC/ST entrepreneurs setting up a greenfield enterprise in manufacturing, services, or trading",
        "short_description": "Composite bank loans between ₹10 Lakh and ₹1 Crore to at least one Woman and one SC/ST borrower per bank branch.",
        "full_description": "Stand-Up India facilitates bank loans between ₹10 Lakh and ₹1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise. The enterprise may be in manufacturing, services, agri-allied activities, or trading sector.",
        "benefits": "Composite loan (term loan and working capital) between ₹10,00,000 and ₹1,00,00,000 repayable in up to 7 years with maximum moratorium period of 18 months. Margin money requirement reduced to 15%. Credit guarantee cover via NCGTC.",
        "max_benefit_amount": 10000000,
        "eligibility_criteria": {
            "min_age": 18,
            "max_age": 70,
            "max_annual_income": None,
            "eligible_occupations": ["Entrepreneur", "Business Owner", "Self Employed"],
            "eligible_genders": ["Female", "All"],
            "eligible_categories": ["SC", "ST", "General", "OBC"],
            "max_land_hectares": None,
            "residence_area": ["Rural", "Urban"],
            "is_bpl_required": False,
            "key_rules": [
                "Borrower must be a Woman OR belong to SC/ST category.",
                "Enterprise must be greenfield (first-time venture of the beneficiary).",
                "In case of non-individual enterprises, 51% of shareholding and controlling stake must be held by SC/ST or woman entrepreneur.",
                "Borrower should not be in default to any bank or financial institution."
            ]
        },
        "required_documents": [
            "Aadhaar Card and PAN Card",
            "Caste Certificate (for SC/ST borrowers)",
            "Detailed Project Report (DPR) and business plan",
            "Proof of business address and lease/ownership of business premises",
            "Bank statements for last 6 months"
        ],
        "application_process": "1. Register on Stand-Up India portal (standupmitra.in). 2. Submit business proposal and loan application. 3. Application routed to designated commercial bank branch. 4. Bank conducts appraisal and sanctions credit.",
        "official_url": "https://www.standupmitra.in",
        "verification_date": "2026-10-20",
        "source": "SIDBI & Department of Financial Services, Ministry of Finance",
        "tags": "standup india, women entrepreneur, sc st loan, business loan, 10 lakh to 1 crore, greenfield"
    },
    {
        "code": "MSSC",
        "name": "Mahila Samman Savings Certificate (MSSC)",
        "name_hindi": "महिला सम्मान बचत प्रमाणपत्र",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Finance",
        "category": "Banking, Financial Services & Insurance",
        "target_audience": "Women or girls (or legal guardian on behalf of a minor girl)",
        "short_description": "High-interest (7.5% fixed p.a.) 2-year term deposit scheme offering secure government returns for women.",
        "full_description": "Introduced by the Ministry of Finance to commemorate Azadi Ka Amrit Mahotsav, MSSC is a dedicated small savings scheme for women. It offers an attractive fixed interest rate of 7.5% per annum compounded quarterly for a 2-year tenure, with partial withdrawal facility up to 40% after one year.",
        "benefits": "Fixed interest rate of 7.5% per annum compounded quarterly. Minimum investment of ₹1,000 and maximum of ₹2,00,000 for a flexible 2-year tenure. Up to 40% partial withdrawal allowed after 1 year.",
        "max_benefit_amount": 200000,
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
                "Account can be opened by a woman for herself, or by a guardian on behalf of a minor girl.",
                "Maximum deposit limit of ₹2 Lakh per individual across all MSSC accounts.",
                "A time gap of minimum 3 months between opening two MSSC accounts by the same individual."
            ]
        },
        "required_documents": [
            "Aadhaar Card of the woman/girl",
            "PAN Card (for deposits exceeding ₹50,000)",
            "KYC documents and passport size photograph",
            "Birth certificate (in case of minor girl)"
        ],
        "application_process": "1. Visit any Department of Posts (Post Office) branch or authorized commercial bank. 2. Submit MSSC Account Opening Form with KYC documents. 3. Deposit money via cash/cheque/transfer. 4. Certificate passbook issued.",
        "official_url": "https://www.indiapost.gov.in",
        "verification_date": "2026-10-20",
        "source": "Department of Economic Affairs & India Post",
        "tags": "mahila samman, mssc, fixed deposit, high interest, savings, women finance, postal scheme"
    },
    {
        "code": "SAKHI-OSC",
        "name": "One Stop Centre (OSC / Sakhi) Scheme",
        "name_hindi": "वन स्टॉप सेंटर (सखी) योजना",
        "level": "Central",
        "state": "All India",
        "ministry": "Ministry of Women and Child Development",
        "category": "Women & Child",
        "target_audience": "Women affected by violence in private or public spaces, irrespective of age, marital status, or background",
        "short_description": "Integrated 24x7 emergency shelter, medical aid, police assistance, psycho-social counseling, and legal support under one roof.",
        "full_description": "Formulated under the Nirbhaya Fund framework, Sakhi One Stop Centres facilitate access to an integrated range of services including medical aid, police assistance, psycho-social counseling, legal aid, and temporary shelter (up to 5 days) for women affected by domestic violence, harassment, sexual assault, and trafficking.",
        "benefits": "Free 24x7 emergency response and rescue. Immediate medical examination, free legal aid through District Legal Services Authority (DLSA), trauma counseling, shelter, food, and clothing. Linked directly with Women Helpline 181.",
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
                "Any woman or girl facing violence, harassment, threat, or exploitation in domestic, workplace, or public sphere.",
                "Girls below 18 years are linked with POCSO Act and Child Welfare Committees (CWC).",
                "Completely free of charge with guaranteed confidentiality."
            ]
        },
        "required_documents": [
            "None required for emergency admission. ID proof can be provided later."
        ],
        "application_process": "Dial 181 (Women Helpline) or 112 (Emergency Response Support System), or walk into the nearest Sakhi One Stop Centre located in district headquarters / hospital campuses.",
        "official_url": "https://wcd.nic.in/schemes/one-stop-centre-scheme-1",
        "verification_date": "2026-10-20",
        "source": "Ministry of Women and Child Development",
        "tags": "sakhi, one stop centre, women helpline 181, domestic violence, legal aid, shelter, nirbhaya"
    }
]

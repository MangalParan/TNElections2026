#!/usr/bin/env python3
"""
Generate a comprehensive constituency-wise prediction report for
Tamil Nadu 2026 Assembly Elections.
Data sourced from: https://en.wikipedia.org/wiki/2026_Tamil_Nadu_Legislative_Assembly_election
Exit poll data: Chanakya, P-MARQ, Matrize, ABP-CVoter, NDTV-People's Pulse
"""

# ─── CONSTITUENCY DATA ───────────────────────────────────────────────────────
# Format: (No, Constituency, District, SC/ST, SPA_Party, SPA_Candidate, ADMK_Party, ADMK_Candidate, TVK_notable)
CONSTITUENCIES = [
    (1,  "Gummidipoondi",         "Tiruvallur",       "",   "DMK",   "T. J. Govindrajan",           "AIADMK", "V. Sudhakar",                    False),
    (2,  "Ponneri",               "Tiruvallur",       "SC", "INC",   "Durai Chandrasekar",           "AIADMK", "P. Balaraman",                   False),
    (3,  "Tiruttani",             "Tiruvallur",       "",   "DMDK",  "D. Krishnamoorthy",            "AIADMK", "G. Hari",                        False),
    (4,  "Thiruvallur",           "Tiruvallur",       "",   "DMK",   "V. G. Raajendran",            "AIADMK", "B. V. Ramana",                   False),
    (5,  "Poonamallee",           "Tiruvallur",       "SC", "DMK",   "A. Krishnaswamy",             "AMMK",   "T. A. Elumalai",                 False),
    (6,  "Avadi",                 "Tiruvallur",       "",   "DMK",   "S. M. Nasar",                 "BJP",    "M. Rajasimha Mahendra",          False),
    (7,  "Maduravoyal",           "Chennai",          "",   "DMK",   "K. Ganapathy",                "AIADMK", "P. Benjamin",                    False),
    (8,  "Ambattur",              "Chennai",          "",   "DMK",   "A. P. Poornima",              "PMK",    "K. N. Sekar",                    False),
    (9,  "Madhavaram",            "Chennai",          "",   "DMK",   "S. Sudharsanam",              "AIADMK", "V. Moorthy",                     False),
    (10, "Thiruvottiyur",         "Chennai",          "",   "CPI(M)","L. Sundararajan",             "AIADMK", "K. Kuppan",                      False),
    (11, "Dr. Radhakrishnan Nagar","Chennai",         "",   "DMK",   "J. John Ebenezer",            "AIADMK", "R. S. Rajesh",                   False),
    (12, "Perambur",              "Chennai",          "",   "DMK",   "R. D. Shekar",                "PMK",    "M. Thilagabama",                 True),  # Vijay (TVK) contesting here
    (13, "Kolathur",              "Chennai",          "",   "DMK",   "M. K. Stalin ★",             "AIADMK", "P. Santhana Krishnan",           False),
    (14, "Villivakkam",           "Chennai",          "",   "DMK",   "Karthik Mohan",               "AIADMK", "S. R. Vijayakumar",              False),
    (15, "Thiru-Vi-Ka-Nagar",     "Chennai",          "SC", "DMK",   "K. S. Ravichandran",          "AIADMK", "Porkodi Armstrong (TMBSP)",      False),
    (16, "Egmore",                "Chennai",          "SC", "DMK",   "Tamilan Prasanna",            "AIADMK", "Abishek Rengasamy",              False),
    (17, "Royapuram",             "Chennai",          "",   "DMK",   "Subair Khan",                 "AIADMK", "D. Jayakumar",                   False),
    (18, "Harbour",               "Chennai",          "",   "DMK",   "P. K. Sekar Babu",            "AIADMK", "R. Manohar",                     False),
    (19, "Chepauk-Thiruvallikeni","Chennai",          "",   "DMK",   "Udhayanidhi Stalin ★",       "AIADMK", "Adhi Rajaram",                   False),
    (20, "Thousand Lights",       "Chennai",          "",   "DMK",   "Ezhilan Naganathan",          "AIADMK", "B. Valarmathi",                  False),
    (21, "Anna Nagar",            "Chennai",          "",   "DMK",   "N. Chitrarasu",               "AIADMK", "Gokula Indira",                  False),
    (22, "Virugambakkam",         "Chennai",          "",   "DMK",   "A. M. V. Prabhakara Raja",    "AIADMK", "V. N. Ravi",                     False),
    (23, "Saidapet",              "Chennai",          "",   "DMK",   "Ma. Subramanian",             "AMMK",   "G. Senthamizhan",                False),
    (24, "Thiyagarayanagar",      "Chennai",          "",   "DMK",   "Raja Anbalagan",              "AIADMK", "B. Sathyanarayanan",             False),
    (25, "Mylapore",              "Chennai",          "",   "DMK",   "Dha. Velu",                   "BJP",    "Tamilisai Soundararajan ★",      False),
    (26, "Velachery",             "Chennai",          "",   "INC",   "J. M. H. Aassan Maulaana",    "AIADMK", "M. K. Ashok",                    False),
    (27, "Sholinganallur",        "Chennai",          "",   "DMK",   "S. Aravind Ramesh",           "AIADMK", "K. P. Kandan",                   False),
    (28, "Alandur",               "Chennai",          "",   "DMK",   "T. M. Anbarasan",             "AIADMK", "S. Saravanan",                   False),
    (29, "Sriperumbudur",         "Kanchipuram",      "SC", "INC",   "K. Selvaperunthagai",         "AIADMK", "K. Palani",                      False),
    (30, "Pallavaram",            "Chengalpattu",     "",   "DMDK",  "D. Murugesan",                "AIADMK", "Venkatesan (IJK)",               False),
    (31, "Tambaram",              "Chengalpattu",     "",   "DMK",   "R. S. Krithika Devi",         "AIADMK", "Chitlapakkam C. Rajendran",      False),
    (32, "Chengalpattu",          "Chengalpattu",     "",   "DMK",   "M. K. T. Karthik Dhandapani", "AIADMK", "M. Gajendran",                   False),
    (33, "Thiruporur",            "Chengalpattu",     "",   "VCK",   "Panneer Doss",                "PMK",    "K. Balu",                        False),
    (34, "Cheyyur",               "Chengalpattu",     "SC", "VCK",   "Sinthanai Selvan",            "AIADMK", "E. Rajashekar",                  False),
    (35, "Madurantakam",          "Chengalpattu",     "SC", "DMK",   "S. Amulu Ponmalar",           "AIADMK", "Maragatham Kumaravel",           False),
    (36, "Uthiramerur",           "Kanchipuram",      "",   "DMK",   "K. Sundar",                   "PMK",    "P. Maheshkumar",                 False),
    (37, "Kancheepuram",          "Kanchipuram",      "",   "DMK",   "Nithya Sugumar",              "AIADMK", "V. Somasundaram",                False),
    (38, "Arakkonam",             "Ranipet",          "SC", "VCK",   "Ezhil Caroline",              "AIADMK", "S. Ravi",                        False),
    (39, "Sholinghur",            "Ranipet",          "",   "INC",   "A. M. Munirathinam",          "PMK",    "K. Saravanan",                   False),
    (40, "Katpadi",               "Vellore",          "",   "DMK",   "Durai Murugan ★",            "AIADMK", "V. Ramu",                        False),
    (41, "Ranipet",               "Ranipet",          "",   "DMK",   "R. Gandhi",                   "BJP",    "V. M. Karthikeyan (TMC-M)",      False),
    (42, "Arcot",                 "Ranipet",          "",   "DMK",   "J. L. Eswarappan",            "AIADMK", "S. M. Sukumar",                  False),
    (43, "Vellore",               "Vellore",          "",   "DMK",   "P. Karthikeyan",              "AIADMK", "S. R. K. Appu",                  False),
    (44, "Anaikattu",             "Vellore",          "",   "DMK",   "A. P. Nandakumar",            "AIADMK", "T. Velazhagan",                  False),
    (45, "Kilvaithinankuppam",    "Vellore",          "SC", "DMK",   "Rajeswari Mohankandhi",       "AIADMK", "M. Jagan Moorthy (PBK)",         False),
    (46, "Gudiyattam",            "Vellore",          "SC", "DMDK",  "K. B. Pratap",                "AIADMK", "G. Faridha Purushothaman",       False),
    (47, "Vaniyambadi",           "Tirupathur",       "",   "IUML",  "Sayyed Farooq",               "AIADMK", "G. Senthilkumar",                False),
    (48, "Ambur",                 "Tirupathur",       "",   "DMK",   "A. C. Vilvanathan",           "AIADMK", "R. Venkatesan",                  False),
    (49, "Jolarpet",              "Tirupathur",       "",   "DMK",   "Kavitha Dhandapani",          "AIADMK", "K. C. Veeramani",                False),
    (50, "Tirupattur",            "Tirupathur",       "",   "DMK",   "A. Nallathambi",              "AMMK",   "A. Gnanasekar",                  False),
    (51, "Uthangarai",            "Krishnagiri",      "SC", "INC",   "R. Kuppusamy",                "AIADMK", "T. M. Tamilselvam",              False),
    (52, "Bargur",                "Krishnagiri",      "",   "DMK",   "D. Mathiazhagan",             "AIADMK", "E. C. Govindarajan",             False),
    (53, "Krishnagiri",           "Krishnagiri",      "",   "INC",   "A. Chellakumar",              "AIADMK", "K. Ashok Kumar",                 False),
    (54, "Veppanahalli",          "Krishnagiri",      "",   "DMK",   "P. S. Sreenivasan",           "AIADMK", "K. P. Munusamy",                 False),
    (55, "Hosur",                 "Krishnagiri",      "",   "DMK",   "S. A. Sathya",                "AIADMK", "P. Balakrishna Reddy",           False),
    (56, "Thalli",                "Krishnagiri",      "",   "CPI",   "T. Ramachandran",             "BJP",    "Nagesh Kumar",                   False),
    (57, "Palacode",              "Dharmapuri",       "",   "DMK",   "S. Senthilkumar",             "AIADMK", "K. P. Anbalagan",                False),
    (58, "Pennagaram",            "Dharmapuri",       "",   "INC",   "G. K. M. Tamilkumaran",       "PMK",    "V. Selvam",                      False),
    (59, "Dharmapuri",            "Dharmapuri",       "",   "DMDK",  "V. Elangovan",                "PMK",    "Sowmiya Anbumani ★",            False),
    (60, "Pappireddippatti",      "Dharmapuri",       "",   "DMK",   "P. Palaniappan",              "AIADMK", "Maragatham Vetrivel",            False),
    (61, "Harur",                 "Dharmapuri",       "SC", "DMK",   "A. Shanmugam",                "AIADMK", "V. Sampathkumar",                False),
    (62, "Chengam",               "Tiruvannamalai",   "SC", "DMK",   "M. P. Giri",                  "AIADMK", "T. S. Velu",                     False),
    (63, "Tiruvannamalai",        "Tiruvannamalai",   "",   "DMK",   "E. V. Velu",                  "BJP",    "C. Ezhumalai",                   False),
    (64, "Kilpennathur",          "Tiruvannamalai",   "",   "DMK",   "K. Pitchandi",                "AIADMK", "S. Ramachandran",                False),
    (65, "Kalasapakkam",          "Tiruvannamalai",   "",   "DMK",   "P. S. T. Saravanan",          "AIADMK", "Agri S. S. Krishnamurthy",       False),
    (66, "Polur",                 "Tiruvannamalai",   "",   "DMDK",  "T. P. Saravanan",             "PMK",    "C. R. Bhaskaran",                False),
    (67, "Arani",                 "Tiruvannamalai",   "",   "DMK",   "Mahalakshmi Govarthanan",     "AIADMK", "L. Jaya Sudha",                  False),
    (68, "Cheyyar",               "Tiruvannamalai",   "",   "DMK",   "O. Jothi",                    "AIADMK", "Mukkur N. Subramanian",          False),
    (69, "Vandavasi",             "Tiruvannamalai",   "SC", "DMK",   "Ambethkumar",                 "AIADMK", "P. Rani",                        False),
    (70, "Gingee",                "Viluppuram",       "",   "DMK",   "K. S. Masthan",               "PMK",    "A. Ganeshkumar",                 False),
    (71, "Mailam",                "Viluppuram",       "",   "DMDK",  "L. Venkatesan",               "AIADMK", "C. Ve. Shanmugam",               False),
    (72, "Tindivanam",            "Viluppuram",       "SC", "VCK",   "Vanniyarasu",                 "AIADMK", "P. Arjunan",                     False),
    (73, "Vanur",                 "Viluppuram",       "SC", "DMK",   "Gautham Dravidamani",         "AIADMK", "P. Murugan",                     False),
    (74, "Villupuram",            "Viluppuram",       "",   "DMK",   "R. Lakshmanan",               "AIADMK", "K. Vijaya",                      False),
    (75, "Vikravandi",            "Viluppuram",       "",   "DMK",   "Anniyur Siva",                "PMK",    "C. Sivakumar",                   False),
    (76, "Tirukkoyilur",          "Viluppuram",       "",   "DMK",   "Gautham Sigamani",            "AIADMK", "S. Palaniswami",                 False),
    (77, "Ulundurpettai",         "Kallakurichi",     "",   "DMK",   "G. R. Vasanthavelu",          "AIADMK", "R. Kumaraguru",                  False),
    (78, "Rishivandiyam",         "Kallakurichi",     "",   "DMK",   "Vasantham Karthikeyan",       "PMK",    "A. P. Chezhiyan",                False),
    (79, "Sankarapuram",          "Kallakurichi",     "",   "DMK",   "T. Udhaya Suriyan",           "AIADMK", "R. Rakesh",                      False),
    (80, "Kallakurichi",          "Kallakurichi",     "SC", "VCK",   "Malathi",                     "AIADMK", "S. Rajiv Gandhi",                False),
    (81, "Gangavalli",            "Salem",            "SC", "DMK",   "K. Chinnadurai",              "AIADMK", "A. Nallathambi",                 False),
    (82, "Attur",                 "Salem",            "SC", "INC",   "S. K. Arthanari",             "AIADMK", "A. P. Jayasankaran",             False),
    (83, "Yercaud",               "Salem",            "ST", "DMK",   "T. M. Revathi Matheswaran",   "AIADMK", "P. Usharani",                    False),
    (84, "Omalur",                "Salem",            "",   "DMDK",  "A. R. Elangovan",             "AIADMK", "R. Mani",                        False),
    (85, "Mettur",                "Salem",            "",   "DMK",   "Mithun Chakravarthy",         "AIADMK", "G. Venkatachalam",               False),
    (86, "Edappadi",              "Salem",            "",   "DMK",   "Kasi",                        "AIADMK", "Edappadi K. Palaniswami ★",     False),
    (87, "Sangagiri",             "Salem",            "",   "DMK",   "M. Manikandan",               "AIADMK", "S. Vetrivel",                    False),
    (88, "Salem (West)",          "Salem",            "",   "DMDK",  "Azhagappuram Mohan Raj",      "PMK",    "M. Karthi",                      False),
    (89, "Salem (North)",         "Salem",            "",   "DMK",   "R. Rajendran",                "PMK",    "S. Sadhasivam",                  False),
    (90, "Salem (South)",         "Salem",            "",   "DMK",   "M. Loganathan",               "AIADMK", "J. Vinodh",                      False),
    (91, "Veerapandi",            "Salem",            "",   "DMK",   "A. K. Tharun",                "AIADMK", "Sri Balaji Sukumar",             False),
    (92, "Rasipuram",             "Namakkal",         "SC", "DMK",   "M. Mathivendhan",             "BJP",    "S. D. Premkumar",                False),
    (93, "Senthamangalam",        "Namakkal",         "ST", "DMK",   "P. Poomalar",                 "AIADMK", "C. Chandrashekhar",              False),
    (94, "Namakkal",              "Namakkal",         "",   "DMK",   "P. Rani",                     "AIADMK", "Sridevi P. S. Mohan",            False),
    (95, "Paramathi-Velur",       "Namakkal",         "",   "DMK",   "K. S. Moorthy",               "AIADMK", "S. Sekar",                       False),
    (96, "Tiruchengodu",          "Namakkal",         "",   "DMK",   "E. R. Eswaran (KMDK)",        "AIADMK", "R. Chandrashekhar",              False),
    (97, "Kumarapalayam",         "Namakkal",         "",   "DMK",   "S. Balu",                     "AIADMK", "P. Thangamani",                  False),
    (98, "Erode (East)",          "Erode",            "",   "INC",   "Gobinath Palaniappan",        "AIADMK", "R. Manoharan",                   False),
    (99, "Erode (West)",          "Erode",            "",   "DMK",   "S. Muthusamy",                "BJP",    "M. Yuvaraja (TMC-M)",            False),
    (100,"Modakkurichi",          "Erode",            "",   "DMK",   "Senthilnathan (MDMK)",        "BJP",    "Kirthika Sivakumar",             False),
    (101,"Dharapuram",            "Tiruppur",         "SC", "DMK",   "Indirani",                    "AIADMK", "P. Sathyabama",                  False),
    (102,"Kangayam",              "Tiruppur",         "",   "DMK",   "M. P. Saminathan",            "AIADMK", "N. S. N. Nataraj",               False),
    (103,"Perundurai",            "Erode",            "",   "DMK",   "N. D. Venkatachalam",         "AIADMK", "S. Jayakumar",                   False),
    (104,"Bhavani",               "Erode",            "",   "DMK",   "K. A. Chandrasekhar",         "AIADMK", "K. C. Karuppannan",              False),
    (105,"Anthiyur",              "Erode",            "",   "DMK",   "M. Sivabalan",                "AIADMK", "P. Haribhaskar",                 False),
    (106,"Gobichettipalayam",     "Erode",            "",   "DMK",   "N. Nallasivam",               "AIADMK", "V. B. Prabhu",                   False),
    (107,"Bhavanisagar",          "Erode",            "SC", "CPI",   "P. L. Sundaram",              "AIADMK", "A. Bannari",                     False),
    (108,"Udhagamandalam",        "Nilgiris",         "",   "INC",   "B. Ramachandran",             "BJP",    "Bhojarajan",                     False),
    (109,"Gudalur",               "Nilgiris",         "SC", "DMK",   "Dravidamani",                 "AIADMK", "Pon. Jayaseelan",                False),
    (110,"Coonoor",               "Nilgiris",         "",   "DMK",   "K. M. Raju",                  "AIADMK", "A. Ramu",                        False),
    (111,"Mettupalayam",          "Coimbatore",       "",   "DMK",   "Kavitha Kalyanachundaram",    "AIADMK", "O. K. Chinnaraj",                False),
    (112,"Avanashi",              "Tiruppur",         "SC", "DMK",   "Gokilamani",                  "BJP",    "L. Murugan ★",                  False),
    (113,"Tiruppur (North)",      "Tiruppur",         "",   "CPI",   "Ravi Subramanian",            "AIADMK", "M. S. M. Anandan",               False),
    (114,"Tiruppur (South)",      "Tiruppur",         "",   "DMK",   "K. Dineshkumar",              "BJP",    "S. Thangaraj",                   False),
    (115,"Palladam",              "Tiruppur",         "",   "DMK",   "K. Selvaraj",                 "AIADMK", "K. P. Paramasivam",              False),
    (116,"Sulur",                 "Coimbatore",       "",   "DMK",   "S. Murugesan",                "AIADMK", "V. P. Kandasamy",                False),
    (117,"Kavundampalayam",       "Coimbatore",       "",   "INC",   "K. P. Suryaprakash",          "AIADMK", "P. R. G. Arunkumar",             False),
    (118,"Coimbatore (North)",    "Coimbatore",       "",   "DMK",   "Senthamizhselvan",            "BJP",    "Vanathi Srinivasan ★",          False),
    (119,"Thondamuthur",          "Coimbatore",       "",   "DMK",   "N. R. Karthikeyan",           "AIADMK", "S. P. Velumani",                 False),
    (120,"Coimbatore (South)",    "Coimbatore",       "",   "DMK",   "V. Senthil Balaji ★",        "AIADMK", "Amman K. Arjunan",               False),
    (121,"Singanallur",           "Coimbatore",       "",   "INC",   "V. Srinidhi Naidu",           "AIADMK", "K. R. Jayaraman",                False),
    (122,"Kinathukadavu",         "Coimbatore",       "",   "DMK",   "K. V. K. S. Sabari Karthikeyan","AIADMK","S. Damodaran",                  False),
    (123,"Pollachi",              "Coimbatore",       "",   "DMK",   "K. Nithyanandhan (KMDK)",     "AIADMK", "Pollachi V. Jayaraman",          False),
    (124,"Valparai",              "Coimbatore",       "SC", "DMK",   "A. Sudhakar",                 "AIADMK", "D. Lakshmana Singh",             False),
    (125,"Udumalaipettai",        "Tiruppur",         "",   "DMK",   "K. Radhakrishnan",            "AIADMK", "Udumalai K. Radhakrishnan",      False),
    (126,"Madathukulam",          "Tiruppur",         "",   "DMK",   "R. Jayaramakrishnan",         "AMMK",   "C. Shanmugavelu",                False),
    (127,"Palani",                "Dindigul",         "",   "CPI(M)","N. Pandi",                    "AIADMK", "K. Ravi Manoharan",              False),
    (128,"Oddanchatram",          "Dindigul",         "",   "DMK",   "R. Sakkarapani",              "BJP",    "Vidiyal Sekar (TMC-M)",          False),
    (129,"Athoor",                "Dindigul",         "",   "DMK",   "I. Periyasamy",               "AIADMK", "A. Viswanathan",                 False),
    (130,"Nilakottai",            "Dindigul",         "SC", "DMK",   "Nagajothi",                   "AIADMK", "S. Thaenmozhi",                  False),
    (131,"Natham",                "Dindigul",         "",   "DMK",   "K. K. Selvakumar (TDK)",      "AIADMK", "Natham R. Viswanathan",          False),
    (132,"Dindigul",              "Dindigul",         "",   "DMK",   "I. P. Senthilkumar",          "AIADMK", "Dindigul C. Sreenivasan",        False),
    (133,"Vedasandur",            "Dindigul",         "",   "DMK",   "S. Gandhirajan",              "AIADMK", "V. P. B. Paramasivam",           False),
    (134,"Aravakurichi",          "Karur",            "",   "DMK",   "Monjanur R. Elango",          "AIADMK", "K. Selvakumar",                  False),
    (135,"Karur",                 "Karur",            "",   "DMK",   "Asi. M. Thyagarajan",         "AIADMK", "M. R. Vijayabhaskar",            False),
    (136,"Krishnarayapuram",      "Karur",            "SC", "DMK",   "C. K. Raja",                  "AIADMK", "S. Dhivya",                      False),
    (137,"Kulithalai",            "Karur",            "",   "DMK",   "Suriyanur A. Chandiran",      "AIADMK", "S. Karunakaran",                 False),
    (138,"Manapaarai",            "Tiruchirappalli",  "",   "DMK",   "P. Abdul Samad (MMK)",        "AIADMK", "P. L. Vijayakumar",              False),
    (139,"Srirangam",             "Tiruchirappalli",  "",   "DMK",   "S. Durairaj",                 "AIADMK", "R. Manoharan",                   False),
    (140,"Tiruchirappalli (West)","Tiruchirappalli",  "",   "DMK",   "K. N. Nehru",                 "AMMK",   "M. Rajasekhar",                  False),
    (141,"Tiruchirappalli (East)","Tiruchirappalli",  "",   "DMK",   "Inigo Irudhayaraj",           "AIADMK", "K. Rajasekaran",                 False),
    (142,"Thiruverumbur",         "Tiruchirappalli",  "",   "DMK",   "Anbil Mahesh Poyyamozhi ★",  "AIADMK", "P. Kumar",                       False),
    (143,"Lalgudi",               "Tiruchirappalli",  "",   "DMK",   "T. Parivallal",               "AIADMK", "Leema Rose Martin",              False),
    (144,"Manachanallur",         "Tiruchirappalli",  "",   "DMK",   "S. Kathiravan",               "AIADMK", "R. V. Bharathan (STMK)",         False),
    (145,"Musiri",                "Tiruchirappalli",  "",   "DMK",   "N. S. N. Karunairaja",        "AIADMK", "N. Yoganathan",                  False),
    (146,"Thuraiyur",             "Tiruchirappalli",  "SC", "INC",   "M. Vichu Lenin Prasath",      "AIADMK", "E. Suroja",                      False),
    (147,"Perambalur",            "Perambalur",       "SC", "DMK",   "S. D. Jayalakshmi",           "AIADMK", "R. Thamizhselvan",               False),
    (148,"Kunnam",                "Perambalur",       "",   "DMK",   "S. S. Sivasankar",            "AIADMK", "Saranya Anbazhagan (IJK)",        False),
    (149,"Ariyalur",              "Ariyalur",         "",   "DMK",   "Latha Balu",                  "AIADMK", "Thamarai S. Rajendran",          False),
    (150,"Jayankondam",           "Ariyalur",         "",   "DMK",   "Ka. So. Ka. Kannan",          "PMK",    "K. Vaithi",                      False),
    (151,"Tittakudi",             "Cuddalore",        "SC", "DMK",   "C. V. Ganesan",               "AIADMK", "N. Murugumaran",                 False),
    (152,"Virudhachalam",         "Cuddalore",        "",   "DMDK",  "Premalatha Vijayakhanth ★",  "PMK",    "Tamilarasi Adhimoolam",          False),
    (153,"Neyveli",               "Cuddalore",        "",   "DMK",   "Saba. Rajendran",             "AIADMK", "Sorathur R. Rajendran",          False),
    (154,"Panruti",               "Cuddalore",        "",   "VCK",   "Abdul Rahman",                "AIADMK", "K. Mohan",                       False),
    (155,"Cuddalore",             "Cuddalore",        "",   "INC",   "A. S. Chandrashekhar",        "AIADMK", "M. C. Sampath",                  False),
    (156,"Kurinjipadi",           "Cuddalore",        "",   "DMK",   "M. R. K. Panneerselvam",      "AIADMK", "A. Bhuvanendhran",               False),
    (157,"Bhuvanagiri",           "Cuddalore",        "",   "DMK",   "Durai K. Saravana",           "AIADMK", "A. Arunmozhithevan",             False),
    (158,"Chidambaram",           "Cuddalore",        "",   "DMK",   "Thamimun Ansari (MJK)",       "AIADMK", "K. A. Pandian",                  False),
    (159,"Kattumannarkoil",       "Cuddalore",        "SC", "VCK",   "Jothimani Ilayaperumal",      "PMK",    "Anbu Cholan",                    False),
    (160,"Sirkazhi",              "Mayiladuthurai",   "SC", "DMK",   "Senthil Selvan (MDMK)",       "AIADMK", "M. Sakthi",                      False),
    (161,"Mayiladuthurai",        "Mayiladuthurai",   "",   "INC",   "Jamal Yunus Muhammed",        "PMK",    "S. A. Palanichamy",              False),
    (162,"Poompuhar",             "Mayiladuthurai",   "",   "DMK",   "Nivedha M. Murugan",          "AIADMK", "S. Pavunraj",                    False),
    (163,"Nagapattinam",          "Nagapattinam",     "",   "DMK",   "M. H. Jawahirullah (MMK)",    "AIADMK", "Thanga Kathiravan",              False),
    (164,"Kilvelur",              "Nagapattinam",     "SC", "CPI(M)","D. Latha",                    "PMK",    "Vadivel Ravanan",                False),
    (165,"Vedaranyam",            "Nagapattinam",     "",   "DMK",   "Ma.Me. Pugazhendhi",          "AIADMK", "O. S. Manian",                   False),
    (166,"Thiruthuraipoondi",     "Tiruvarur",        "SC", "CPI",   "K. Marimuthu",                "AIADMK", "U. Paladhandayutham",            False),
    (167,"Mannargudi",            "Tiruvarur",        "",   "DMK",   "T. R. B. Rajaa ★",           "AMMK",   "S. Kamaraj",                     False),
    (168,"Thiruvarur",            "Tiruvarur",        "",   "DMK",   "K. Poondi Kalaivanan",        "BJP",    "Govi Chandru",                   False),
    (169,"Nannilam",              "Tiruvarur",        "",   "DMK",   "V. M. S. Mohammed Mubarak (SDPI)","AIADMK","R. Kamaraj",                  False),
    (170,"Thiruvidaimarudur",     "Thanjavur",        "SC", "DMK",   "Govi. Chezian",               "AIADMK", "Ilamathi Subramanian",           False),
    (171,"Kumbakonam",            "Thanjavur",        "",   "DMK",   "G. Anbalagan",                "BJP",    "M. K. R. Ashok Kumar (TMC-M)",   False),
    (172,"Papanasam",             "Thanjavur",        "",   "IUML",  "A. M. Shahjahan",             "AIADMK", "D. Shanmugaprabhu",              False),
    (173,"Thiruvaiyaru",          "Thanjavur",        "",   "DMK",   "Durai. Chandrashekhar",       "AMMK",   "V. Karthikeyan",                 False),
    (174,"Thanjavur",             "Thanjavur",        "",   "DMK",   "Ramanathan",                  "BJP",    "M. Muruganantham",               False),
    (175,"Orathanadu",            "Thanjavur",        "",   "DMK",   "R. Vaithialingam",            "AIADMK", "M. Sekar",                       False),
    (176,"Pattukkottai",          "Thanjavur",        "",   "DMK",   "K. Annadurai",                "AIADMK", "C. V. Sekar",                    False),
    (177,"Peravurani",            "Thanjavur",        "",   "DMK",   "N. Ashokkumar",               "AIADMK", "Govi Ilango",                    False),
    (178,"Gandarvakottai",        "Pudukkottai",      "SC", "CPI(M)","M. Chinndadurai",             "BJP",    "C. Udhayakumar",                 False),
    (179,"Viralimalai",           "Pudukkottai",      "",   "DMK",   "K. K. Chellapandian",         "AIADMK", "C. Vijayabhaskar",               False),
    (180,"Pudukkottai",           "Pudukkottai",      "",   "DMK",   "V. Muthuraja",                "BJP",    "N. Ramachandran",                False),
    (181,"Thirumayam",            "Pudukkottai",      "",   "DMK",   "S. Regupathy",                "AIADMK", "P. K. Vairamuthu",               False),
    (182,"Alangudi",              "Pudukkottai",      "",   "DMK",   "Siva V. Meyyanathan",         "AIADMK", "D. Vimal",                       False),
    (183,"Aranthangi",            "Pudukkottai",      "",   "INC",   "T. Ramachandran",             "BJP",    "Kavitha Srikanth",               False),
    (184,"Karaikudi",             "Sivaganga",        "",   "INC",   "S. Mangudi",                  "AMMK",   "Dherpoki V. Pandi",              False),
    (185,"Tiruppattur",           "Sivaganga",        "",   "DMK",   "K. R. Periyakaruppan",        "BJP",    "K. C. Thirumaran (SIFB)",        False),
    (186,"Sivaganga",             "Sivaganga",        "",   "DMK",   "Karunas (MPP)",               "AIADMK", "P. R. Senthilnathan",            False),
    (187,"Manamadurai",           "Sivaganga",        "SC", "DMK",   "A. Tamilarasi",               "BJP",    "Pon V. Balaganapathy",           False),
    (188,"Melur",                 "Madurai",          "",   "INC",   "P. Viswanathan",              "AIADMK", "Periyapullan alias Selvam",      False),
    (189,"Madurai East",          "Madurai",          "",   "DMK",   "P. Moorthy",                  "AIADMK", "K. Mahendran",                   False),
    (190,"Sholavandan",           "Madurai",          "SC", "DMK",   "A. Venkatesan",               "AIADMK", "K. Manickam",                    False),
    (191,"Madurai North",         "Madurai",          "",   "DMK",   "G. Thalapathy",               "AIADMK", "P. Saravanan",                   False),
    (192,"Madurai South",         "Madurai",          "",   "DMK",   "M. Boominathan (MDMK)",       "BJP",    "Raama Sreenivasan",              False),
    (193,"Madurai Central",       "Madurai",          "",   "DMK",   "Palanivel Thiaga Rajan ★",   "AIADMK", "Sundar C (PNK)",                 False),
    (194,"Madurai West",          "Madurai",          "",   "DMK",   "Raghu Balaji",                "AIADMK", "Sellur K. Raju",                 False),
    (195,"Thiruparankundram",     "Madurai",          "",   "DMK",   "S. Keerthiga Thangapandi",    "AIADMK", "V. V. Rajan Chellappa",          False),
    (196,"Thirumangalam",         "Madurai",          "",   "DMK",   "M. Manimaran",                "AIADMK", "R. B. Udhayakumar",              False),
    (197,"Usilampatti",           "Madurai",          "",   "INC",   "T. Saravanakumar",            "AIADMK", "I. Mahendran",                   False),
    (198,"Andipatti",             "Theni",            "",   "DMK",   "A. Maharajan",                "AIADMK", "A. Logirajan",                   False),
    (199,"Periyakulam",           "Theni",            "SC", "VCK",   "Attral Arasu",                "AMMK",   "K. Kathirkamu",                  False),
    (200,"Bodinayakanur",         "Theni",            "",   "DMK",   "O. Panneerselvam (OPS)",      "AIADMK", "V. T. Narayansamy",              False),
    (201,"Cumbum",                "Theni",            "",   "DMK",   "N. Eramakrishnan",            "AIADMK", "S. T. K. Jakkaiyan",             False),
    (202,"Rajapalayam",           "Virudhunagar",     "",   "DMK",   "S. Thanga Pandian",           "BJP",    "Priscilla Pandian (TMMK)",       False),
    (203,"Srivilliputhur",        "Virudhunagar",     "SC", "CPI",   "P. Mahalingam",               "AIADMK", "M. Chandra Prabha",              False),
    (204,"Sattur",                "Virudhunagar",     "",   "DMK",   "A. Kadarkarairaj",            "BJP",    "Nainar Nagendran ★",            False),
    (205,"Sivakasi",              "Virudhunagar",     "",   "INC",   "Ganesan Ashokan",             "AIADMK", "K. T. Rajenthra Bhalaji",        False),
    (206,"Virudhunagar",          "Virudhunagar",     "",   "DMDK",  "Vijayaprabhakar",             "AIADMK", "V. G. Ganesan",                  False),
    (207,"Aruppukkottai",         "Virudhunagar",     "",   "DMK",   "K. K. S. S. R. Ramachandran", "AIADMK", "S. Sethupathi",                  False),
    (208,"Tiruchuli",             "Virudhunagar",     "",   "DMK",   "Thangam Thennarasu ★",       "AIADMK", "M. S. R. Rajavarman",            False),
    (209,"Paramakudi",            "Ramanathapuram",   "SC", "DMK",   "K. K. Kathiravan",            "AIADMK", "S. Muthaiah",                    False),
    (210,"Tiruvadanai",           "Ramanathapuram",   "",   "INC",   "Karu Manickam",               "AIADMK", "Keerthika Muniyasamy",           False),
    (211,"Ramanathapuram",        "Ramanathapuram",   "",   "DMK",   "Katharbatcha Muthuramalingam","BJP",    "K. Nagendran",                   False),
    (212,"Mudhukulathur",         "Ramanathapuram",   "",   "DMK",   "R. S. Raja Kannappan",        "AIADMK", "S. Pandi",                       False),
    (213,"Vilathikulam",          "Thoothukudi",      "",   "DMK",   "G. V. Markandayan",           "AIADMK", "R. Sathya",                      False),
    (214,"Thoothukkudi",          "Thoothukudi",      "",   "DMK",   "P. Geetha Jeevan",            "AIADMK", "S. T. Chellapandian",            False),
    (215,"Tiruchendur",           "Thoothukudi",      "",   "DMK",   "Anitha R. Radhakrishnan",     "BJP",    "K. R. M. Radhakrishnan",         False),
    (216,"Srivaikuntam",          "Thoothukudi",      "",   "INC",   "Oorvasi S. Amirtharaj",       "AIADMK", "S. P. Shanmuganathan",           False),
    (217,"Ottapidaram",           "Thoothukudi",      "SC", "DMK",   "M. C. Shunmugaiah",           "AMMK",   "R. Sundararaj",                  False),
    (218,"Kovilpatti",            "Thoothukudi",      "",   "DMK",   "Ka. Karunanithi",             "AIADMK", "Kadambur Raju",                  False),
    (219,"Sankarankovil",         "Tenkasi",          "SC", "INC",   "Sangai Ganesan",              "AIADMK", "Dhileepan Jayasankaran",         False),
    (220,"Vasudevanallur",        "Tenkasi",          "SC", "DMK",   "E. Raja",                     "BJP",    "Ananthan Ayyasamy",              False),
    (221,"Kadayanallur",          "Tenkasi",          "",   "DMK",   "T. M. Rajendran (MDMK)",      "AIADMK", "C. Krishnamurali",               False),
    (222,"Tenkasi",               "Tenkasi",          "",   "DMK",   "Kalai Kathiravan",            "AIADMK", "S. Selvamohandas Pandian",       False),
    (223,"Alangulam",             "Tenkasi",          "",   "DMK",   "Manoj Pandian",               "AIADMK", "K. R. P. Prabakaran",            False),
    (224,"Tirunelveli",           "Tirunelveli",      "",   "DMK",   "Su. Subramanian",             "AIADMK", "Thachai N. Ganesaraja",          False),
    (225,"Ambasamudram",          "Tirunelveli",      "",   "INC",   "V. P. Durai",                 "AIADMK", "Isakki Subhaya",                 False),
    (226,"Palayamkottai",         "Tirunelveli",      "",   "DMK",   "M. Abdul Wahab",              "AIADMK", "Syed Sulthan Sumsuddin",         False),
    (227,"Nanguneri",             "Tirunelveli",      "",   "INC",   "Rubi Manoharan",              "AMMK",   "R. Esakkimuthu",                 False),
    (228,"Radhapuram",            "Tirunelveli",      "",   "DMK",   "M. Appavu",                   "BJP",    "S. P. Balakrishnan",             False),
    (229,"Kanniyakumari",         "Kanyakumari",      "",   "DMK",   "R. Mahesh",                   "AIADMK", "Thalavai N. Sundaram",           False),
    (230,"Nagercoil",             "Kanyakumari",      "",   "DMK",   "S. Austin",                   "BJP",    "M. R. Gandhi",                   False),
    (231,"Colachal",              "Kanyakumari",      "",   "INC",   "Tharahai Cuthbert",           "BJP",    "T. Sivakumar",                   False),
    (232,"Padmanabhapuram",       "Kanyakumari",      "",   "CPI(M)","R. Chellasamy",               "BJP",    "P. Ramesh",                      False),
    (233,"Vilavancode",           "Kanyakumari",      "",   "INC",   "T. T. Pravin",                "BJP",    "S. Vijayadharani",               False),
    (234,"Killiyoor",             "Kanyakumari",      "",   "INC",   "S. Rajesh Kumar",             "BJP",    "Nivin Simon (TMC-M)",            False),
]

# ─── PREDICTION MODEL ────────────────────────────────────────────────────────
# Based on exit poll consensus (Poll of Polls): DMK+ ~145, AIADMK+ ~74, TVK ~15
# Confidence: H=High, M=Medium, L=Low
# Winner: SPA=DMK alliance, ADMK=AIADMK alliance, TVK=Tamilaga Vettri Kazhagam

PREDICTIONS = {
    # No: (winner, confidence, note)
    1:  ("SPA",  "H", "DMK stronghold; 2021 winner DMK"),
    2:  ("SPA",  "H", "INC; Congress hold from 2021"),
    3:  ("SPA",  "M", "DMDK vs AIADMK; DMK alliance edge"),
    4:  ("SPA",  "H", "DMK incumbency; V. G. Raajendran strong"),
    5:  ("SPA",  "H", "DMK stronghold Chennai suburban"),
    6:  ("SPA",  "M", "DMK vs BJP; urban seat, DMK likely"),
    7:  ("SPA",  "H", "DMK stronghold Chennai"),
    8:  ("SPA",  "M", "DMK vs PMK; TVK factor splits anti-DMK vote"),
    9:  ("SPA",  "H", "DMK stronghold North Chennai"),
    10: ("SPA",  "H", "CPI(M) strong; left alliance incumbent"),
    11: ("SPA",  "H", "DMK stronghold Chennai"),
    12: ("TVK",  "M", "Vijay (TVK) contesting here; STAR SEAT"),
    13: ("SPA",  "H", "CM MK Stalin's own seat; Kolathur DMK fortress"),
    14: ("SPA",  "H", "DMK urban Chennai stronghold"),
    15: ("SPA",  "H", "DMK SC reserved seat; DMK dominant"),
    16: ("SPA",  "H", "DMK SC reserved; Anna Nagar belt"),
    17: ("SPA",  "H", "DMK North Chennai waterfront seat"),
    18: ("SPA",  "H", "DMK P. K. Sekar Babu incumbent"),
    19: ("SPA",  "H", "Udhayanidhi Stalin; DMK stronghold"),
    20: ("SPA",  "H", "DMK Central Chennai; Ezhilan Naganathan"),
    21: ("SPA",  "H", "DMK Anna Nagar; won 2021"),
    22: ("SPA",  "H", "DMK suburban Chennai"),
    23: ("SPA",  "H", "DMK Ma. Subramanian incumbent"),
    24: ("SPA",  "H", "DMK South Chennai"),
    25: ("SPA",  "M", "DMK vs BJP Tamilisai; close contest expected"),
    26: ("SPA",  "M", "INC Velachery; Congress hold"),
    27: ("SPA",  "H", "DMK OMR corridor; strong DMK"),
    28: ("SPA",  "H", "DMK Alandur; South Chennai suburban"),
    29: ("SPA",  "M", "INC vs AIADMK; Congress hold likely"),
    30: ("SPA",  "M", "DMDK vs AIADMK; SPA edge with DMDK"),
    31: ("SPA",  "H", "DMK Tambaram; suburban stronghold"),
    32: ("SPA",  "H", "DMK Chengalpattu; district seat"),
    33: ("SPA",  "M", "VCK vs PMK; VCK Dalit stronghold"),
    34: ("SPA",  "M", "VCK SC seat; Dalit stronghold"),
    35: ("SPA",  "H", "DMK SC seat; incumbent edge"),
    36: ("SPA",  "M", "DMK vs PMK; Vanniyar belt Uthiramerur"),
    37: ("SPA",  "H", "DMK Kancheepuram; historic DMK town"),
    38: ("SPA",  "M", "VCK Arakkonam SC; strong Dalit base"),
    39: ("SPA",  "M", "INC Sholinghur vs PMK; Vanniyar seat"),
    40: ("SPA",  "H", "DMK; Durai Murugan senior minister"),
    41: ("SPA",  "H", "DMK Ranipet; R. Gandhi incumbent"),
    42: ("SPA",  "H", "DMK Arcot; Muslim minority significant"),
    43: ("SPA",  "H", "DMK Vellore district HQ"),
    44: ("SPA",  "H", "DMK Anaikattu"),
    45: ("SPA",  "H", "DMK SC seat Kilvaithinankuppam"),
    46: ("SPA",  "M", "DMDK vs AIADMK SC seat Gudiyattam"),
    47: ("SPA",  "M", "IUML Vaniyambadi; Muslim majority seat"),
    48: ("SPA",  "H", "DMK Ambur; leather town, strong DMK"),
    49: ("SPA",  "H", "DMK Jolarpet; KCV incumbent"),
    50: ("SPA",  "M", "DMK vs AMMK; AMMK EPS factor"),
    51: ("SPA",  "M", "INC Uthangarai SC; Congress hold"),
    52: ("SPA",  "H", "DMK Bargur; D. Mathiazhagan senior"),
    53: ("SPA",  "M", "INC Krishnagiri; Congress vs AIADMK"),
    54: ("SPA",  "H", "DMK Veppanahalli; Kongu border"),
    55: ("SPA",  "H", "DMK Hosur; industrial city stronghold"),
    56: ("SPA",  "M", "CPI Thalli; Left vs BJP; Left likely"),
    57: ("SPA",  "H", "DMK Palacode; Dharmapuri belt"),
    58: ("SPA",  "M", "INC Pennagaram vs PMK; PMK Vanniyar belt"),
    59: ("ADMK", "M", "PMK Dharmapuri; Vanniyar dominant; PMK Sowmiya"),
    60: ("SPA",  "H", "DMK Pappireddippatti; Dharmapuri dist"),
    61: ("SPA",  "H", "DMK Harur SC; A. Shanmugam"),
    62: ("SPA",  "H", "DMK Chengam SC; eastern TN"),
    63: ("SPA",  "H", "DMK Tiruvannamalai; EVV veteran"),
    64: ("SPA",  "H", "DMK Kilpennathur"),
    65: ("SPA",  "H", "DMK Kalasapakkam"),
    66: ("SPA",  "M", "DMDK Polur vs PMK; SPA edge"),
    67: ("SPA",  "H", "DMK Arani"),
    68: ("SPA",  "H", "DMK Cheyyar; incumbent"),
    69: ("SPA",  "H", "DMK Vandavasi SC"),
    70: ("SPA",  "M", "DMK vs PMK Gingee; PMK Vanniyar belt, close"),
    71: ("SPA",  "M", "DMDK Mailam vs AIADMK; SPA DMDK"),
    72: ("SPA",  "M", "VCK Tindivanam SC; Dalit stronghold"),
    73: ("SPA",  "H", "DMK Vanur SC; eastern TN"),
    74: ("SPA",  "H", "DMK Villupuram district HQ"),
    75: ("SPA",  "M", "DMK vs PMK Vikravandi; PMK present"),
    76: ("SPA",  "H", "DMK Tirukkoyilur"),
    77: ("SPA",  "H", "DMK Ulundurpettai"),
    78: ("SPA",  "M", "DMK vs PMK Rishivandiyam; PMK Vanniyar"),
    79: ("SPA",  "H", "DMK Sankarapuram; T. Udhaya Suriyan"),
    80: ("SPA",  "M", "VCK Kallakurichi SC; Dalit seat"),
    81: ("SPA",  "H", "DMK Gangavalli SC; Salem dist"),
    82: ("SPA",  "M", "INC Attur SC vs AIADMK; competitive"),
    83: ("SPA",  "H", "DMK Yercaud ST; tribal seat"),
    84: ("SPA",  "M", "DMDK Omalur vs AIADMK; Kongu competitive"),
    85: ("SPA",  "M", "DMK Mettur; Kongu competitive; incumbent"),
    86: ("ADMK", "H", "EPS Edappadi — AIADMK leader's home seat; EPS stronghold"),
    87: ("SPA",  "M", "DMK Sangagiri; Kongu belt, competitive"),
    88: ("ADMK", "M", "DMDK Salem West vs PMK; PMK/AIADMK Kongu hold"),
    89: ("ADMK", "M", "DMK vs PMK Salem North; PMK strong Kongu"),
    90: ("SPA",  "M", "DMK Salem South; urban Salem"),
    91: ("ADMK", "M", "DMK Veerapandi vs AIADMK; AIADMK Kongu belt"),
    92: ("SPA",  "H", "DMK Rasipuram SC; Mathivendhan incumbent"),
    93: ("SPA",  "H", "DMK Senthamangalam ST; tribal reserved"),
    94: ("SPA",  "H", "DMK Namakkal; P. Rani incumbent"),
    95: ("ADMK", "M", "DMK vs AIADMK Paramathi-Velur; competitive Kongu"),
    96: ("SPA",  "M", "DMK/KMDK Tiruchengodu; Kongu belt, close"),
    97: ("ADMK", "M", "DMK vs AIADMK Kumarapalayam; Kongu AIADMK strong"),
    98: ("ADMK", "M", "INC Erode East vs AIADMK; Gounder belt AIADMK"),
    99: ("SPA",  "M", "DMK Erode West vs BJP TMC-M; close"),
    100:("ADMK", "M", "DMK MDMK Modakkurichi vs BJP; BJP Kirthika Sivakumar"),
    101:("SPA",  "H", "DMK Dharapuram SC; incumbent"),
    102:("ADMK", "M", "DMK Kangayam vs AIADMK; Kongu AIADMK strong"),
    103:("ADMK", "M", "DMK vs AIADMK Perundurai; Kongu competitive"),
    104:("ADMK", "M", "DMK Bhavani vs AIADMK; Kongu competitive"),
    105:("SPA",  "M", "DMK Anthiyur; Erode Kongu, marginal DMK edge"),
    106:("SPA",  "M", "DMK Gobichettipalayam; Erode dist"),
    107:("SPA",  "M", "CPI Bhavanisagar SC vs AIADMK; left hold"),
    108:("SPA",  "M", "INC Ooty vs BJP; INC traditionally strong here"),
    109:("SPA",  "H", "DMK Gudalur SC; tribal belt"),
    110:("SPA",  "M", "DMK Coonoor; hill seat"),
    111:("SPA",  "M", "DMK Mettupalayam vs AIADMK; Kongu competitive"),
    112:("ADMK", "M", "DMK vs BJP L. Murugan (Union Minister); BJP push Avanashi"),
    113:("SPA",  "M", "CPI Tiruppur North vs AIADMK; Left hold"),
    114:("SPA",  "M", "DMK Tiruppur South vs BJP; DMK urban edge"),
    115:("ADMK", "M", "DMK vs AIADMK Palladam; Kongu AIADMK competitive"),
    116:("ADMK", "M", "DMK Sulur vs AIADMK; Kongu Coimbatore competitive"),
    117:("SPA",  "M", "INC Kavundampalayam vs AIADMK; Congress hold"),
    118:("SPA",  "M", "DMK vs BJP Vanathi Srinivasan; close urban Coimbatore"),
    119:("ADMK", "M", "DMK vs AIADMK Thondamuthur; SP Velumani AIADMK strong"),
    120:("SPA",  "H", "DMK V. Senthil Balaji; senior DMK minister holds"),
    121:("SPA",  "M", "INC Singanallur vs AIADMK; Congress urban hold"),
    122:("SPA",  "M", "DMK Kinathukadavu; rural Coimbatore"),
    123:("ADMK", "M", "DMK KMDK Pollachi vs AIADMK Pollachi V. Jayaraman; AIADMK"),
    124:("SPA",  "M", "DMK Valparai SC; plantation belt"),
    125:("ADMK", "M", "DMK vs AIADMK Udumalaipettai; both Radhakrishnan contest"),
    126:("SPA",  "M", "DMK vs AMMK Madathukulam; DMK edge Tiruppur"),
    127:("SPA",  "M", "CPI(M) Palani; Left incumbent"),
    128:("SPA",  "H", "DMK Oddanchatram; R. Sakkarapani veteran"),
    129:("SPA",  "H", "DMK Athoor; Dindigul dist"),
    130:("SPA",  "H", "DMK Nilakottai SC; incumbent"),
    131:("SPA",  "M", "DMK TDK Natham vs AIADMK; DMK edge"),
    132:("SPA",  "H", "DMK Dindigul; I. P. Senthilkumar"),
    133:("SPA",  "H", "DMK Vedasandur; S. Gandhirajan"),
    134:("SPA",  "H", "DMK Aravakurichi; Karur dist"),
    135:("SPA",  "H", "DMK Karur; Asi. M. Thyagarajan"),
    136:("SPA",  "H", "DMK Krishnarayapuram SC; Karur dist"),
    137:("SPA",  "H", "DMK Kulithalai; Karur rural"),
    138:("SPA",  "H", "DMK Manapaarai; P. Abdul Samad incumbent"),
    139:("SPA",  "H", "DMK Srirangam; Trichy urban"),
    140:("SPA",  "H", "DMK K. N. Nehru senior minister Trichy West"),
    141:("SPA",  "H", "DMK Trichy East; incumbent win"),
    142:("SPA",  "H", "DMK Anbil Mahesh Poyyamozhi; Thiruverumbur"),
    143:("SPA",  "H", "DMK Lalgudi; Trichy district"),
    144:("SPA",  "H", "DMK Manachanallur; Trichy"),
    145:("SPA",  "H", "DMK Musiri; Trichy rural"),
    146:("SPA",  "M", "INC Thuraiyur SC vs AIADMK; competitive"),
    147:("SPA",  "H", "DMK Perambalur SC; S. D. Jayalakshmi"),
    148:("SPA",  "H", "DMK Kunnam; Perambalur dist"),
    149:("SPA",  "H", "DMK Ariyalur; Latha Balu"),
    150:("SPA",  "H", "DMK Jayankondam; Ka. So. Ka. Kannan"),
    151:("SPA",  "H", "DMK Tittakudi SC; Cuddalore dist"),
    152:("SPA",  "M", "DMDK Virudhachalam; Premalatha Vijayakhanth"),
    153:("SPA",  "H", "DMK Neyveli; Saba. Rajendran"),
    154:("SPA",  "M", "VCK Panruti vs AIADMK; VCK Dalit hold"),
    155:("SPA",  "M", "INC Cuddalore; Congress district HQ hold"),
    156:("SPA",  "H", "DMK Kurinjipadi; M. R. K. Panneerselvam"),
    157:("SPA",  "H", "DMK Bhuvanagiri; Cuddalore dist"),
    158:("SPA",  "H", "DMK Chidambaram; MJK Thamimun Ansari"),
    159:("SPA",  "M", "VCK Kattumannarkoil SC vs PMK; VCK hold"),
    160:("SPA",  "H", "DMK MDMK Sirkazhi SC; Mayiladuthurai"),
    161:("SPA",  "M", "INC Mayiladuthurai vs PMK; Congress hold"),
    162:("SPA",  "H", "DMK Poompuhar; Nivedha M. Murugan"),
    163:("SPA",  "H", "DMK Nagapattinam; M. H. Jawahirullah"),
    164:("SPA",  "M", "CPI(M) Kilvelur SC vs PMK; Left hold"),
    165:("SPA",  "H", "DMK Vedaranyam; coastal seat"),
    166:("SPA",  "M", "CPI Thiruthuraipoondi SC vs AIADMK; Left hold"),
    167:("SPA",  "H", "DMK T. R. B. Rajaa; senior minister Mannargudi"),
    168:("SPA",  "H", "DMK Thiruvarur; delta seat"),
    169:("SPA",  "H", "DMK SDPI Nannilam; Tiruvarur"),
    170:("SPA",  "H", "DMK Thiruvidaimarudur SC; Thanjavur delta"),
    171:("SPA",  "H", "DMK Kumbakonam; G. Anbalagan"),
    172:("SPA",  "M", "IUML Papanasam; Muslim League hold"),
    173:("SPA",  "H", "DMK Thiruvaiyaru; Thanjavur dist"),
    174:("SPA",  "H", "DMK Thanjavur; delta stronghold"),
    175:("SPA",  "H", "DMK Orathanadu; R. Vaithialingam senior"),
    176:("SPA",  "H", "DMK Pattukkottai; K. Annadurai"),
    177:("SPA",  "H", "DMK Peravurani; coastal Thanjavur"),
    178:("SPA",  "M", "CPI(M) Gandarvakottai SC vs BJP; Left hold"),
    179:("SPA",  "H", "DMK Viralimalai; Pudukkottai"),
    180:("SPA",  "H", "DMK Pudukkottai; district HQ"),
    181:("SPA",  "H", "DMK Thirumayam; S. Regupathy"),
    182:("SPA",  "H", "DMK Alangudi; Siva V. Meyyanathan"),
    183:("SPA",  "M", "INC Aranthangi vs BJP; Congress hold Pudukkottai"),
    184:("SPA",  "M", "INC Karaikudi vs AMMK; Congress hold Sivaganga"),
    185:("SPA",  "H", "DMK Tiruppattur Sivaganga; K. R. Periyakaruppan"),
    186:("SPA",  "H", "DMK Sivaganga; Karunas popular"),
    187:("SPA",  "H", "DMK Manamadurai SC; A. Tamilarasi"),
    188:("SPA",  "M", "INC Melur vs AIADMK; Congress hold"),
    189:("SPA",  "H", "DMK Madurai East; P. Moorthy"),
    190:("SPA",  "H", "DMK Sholavandan SC; Madurai"),
    191:("SPA",  "H", "DMK Madurai North; G. Thalapathy"),
    192:("SPA",  "H", "DMK MDMK Madurai South"),
    193:("SPA",  "H", "DMK Palanivel Thiaga Rajan; senior minister"),
    194:("SPA",  "H", "DMK Madurai West; Raghu Balaji"),
    195:("SPA",  "H", "DMK Thiruparankundram; Madurai pilgrimage belt"),
    196:("SPA",  "H", "DMK Thirumangalam; Madurai"),
    197:("SPA",  "M", "INC Usilampatti vs AIADMK; Thevar belt Congress hold"),
    198:("SPA",  "H", "DMK Andipatti; Theni"),
    199:("SPA",  "M", "VCK Periyakulam SC vs AMMK; Dalit hold"),
    200:("SPA",  "M", "DMK OPS Bodinayakanur; O. Panneerselvam DMK new"),
    201:("SPA",  "H", "DMK Cumbum; N. Eramakrishnan"),
    202:("SPA",  "H", "DMK Rajapalayam; S. Thanga Pandian"),
    203:("SPA",  "M", "CPI Srivilliputhur SC vs AIADMK; Left hold"),
    204:("SPA",  "H", "DMK Sattur vs Nainar Nagendran BJP; DMK holds"),
    205:("SPA",  "M", "INC Sivakasi vs AIADMK; Congress hold Virudhunagar"),
    206:("SPA",  "M", "DMDK Virudhunagar vs AIADMK; SPA edge"),
    207:("SPA",  "H", "DMK Aruppukkottai; K. K. S. S. R. Ramachandran"),
    208:("SPA",  "H", "DMK Thangam Thennarasu; senior minister"),
    209:("SPA",  "H", "DMK Paramakudi SC; Ramanathapuram"),
    210:("SPA",  "M", "INC Tiruvadanai vs AIADMK; coastal Ramanathapuram"),
    211:("SPA",  "H", "DMK Ramanathapuram; district HQ"),
    212:("SPA",  "H", "DMK Mudhukulathur; R. S. Raja Kannappan"),
    213:("SPA",  "H", "DMK Vilathikulam; Thoothukudi"),
    214:("SPA",  "H", "DMK P. Geetha Jeevan; Thoothukudi port seat"),
    215:("SPA",  "M", "DMK Tiruchendur; coastal temple town, DMK"),
    216:("SPA",  "M", "INC Srivaikuntam vs AIADMK; Congress hold"),
    217:("SPA",  "H", "DMK Ottapidaram SC; Thoothukudi"),
    218:("SPA",  "H", "DMK Kovilpatti; Ka. Karunanithi"),
    219:("SPA",  "M", "INC Sankarankovil SC vs AIADMK; competitive"),
    220:("SPA",  "H", "DMK Vasudevanallur SC; E. Raja"),
    221:("SPA",  "H", "DMK MDMK Kadayanallur; southern TN"),
    222:("SPA",  "H", "DMK Tenkasi; district HQ"),
    223:("SPA",  "H", "DMK Alangulam; Manoj Pandian"),
    224:("SPA",  "H", "DMK Tirunelveli; district capital"),
    225:("SPA",  "M", "INC Ambasamudram vs AIADMK; competitive southern TN"),
    226:("SPA",  "H", "DMK Palayamkottai; M. Abdul Wahab"),
    227:("SPA",  "M", "INC Nanguneri vs AMMK; Congress hold"),
    228:("SPA",  "H", "DMK Radhapuram; M. Appavu"),
    229:("SPA",  "H", "DMK Kanniyakumari; coastal southernmost"),
    230:("SPA",  "H", "DMK Nagercoil; S. Austin"),
    231:("SPA",  "M", "INC Colachal vs BJP; Congress traditional hold"),
    232:("SPA",  "M", "CPI(M) Padmanabhapuram vs BJP; Left hold Kanyakumari"),
    233:("SPA",  "M", "INC Vilavancode vs BJP; Congress hold"),
    234:("SPA",  "M", "INC Killiyoor vs BJP TMC-M; Congress hold"),
}

# Override: TVK special seat
PREDICTIONS[12] = ("TVK", "M", "Vijay (TVK) contests from Perambur; P-MARQ gives TVK 23% vote—could flip this seat")

# ─── SWING-BASED PREDICTION OVERRIDES ───────────────────────────────────────
# Adjusting for exit poll consensus: SPA~150, AIADMK+~72, TVK~12
_OVERRIDES = {
    10: ('TVK', 'L', 'CPI(M) vs AIADMK Thiruvottiyur; TVK surge could flip North Chennai coastal'),
    12: ('TVK', 'M', 'Vijay (TVK) contesting from Perambur; STAR SEAT — TVK favourite'),
    20: ('TVK', 'L', 'DMK vs AIADMK Thousand Lights; TVK urban appeal 3-way contest'),
    29: ('ADMK', 'M', 'INC vs AIADMK Sriperumbudur SC; AIADMK competitive'),
    30: ('ADMK', 'M', 'DMDK vs AIADMK Pallavaram; AIADMK strong local base'),
    36: ('ADMK', 'M', 'DMK vs PMK Uthiramerur; PMK Vanniyar belt holds for AIADMK+'),
    39: ('ADMK', 'M', 'INC vs PMK Sholinghur; Vanniyar dominant — PMK wins for AIADMK+'),
    50: ('ADMK', 'M', 'DMK vs AMMK Tirupattur; AMMK (AIADMK breakaway) competitive'),
    51: ('ADMK', 'M', 'INC vs AIADMK Uthangarai SC; AIADMK traditional hold'),
    53: ('ADMK', 'M', 'INC vs AIADMK Krishnagiri; AIADMK strong 2021'),
    58: ('ADMK', 'M', 'INC vs PMK Pennagaram; PMK Vanniyar belt wins for AIADMK+'),
    64: ('ADMK', 'M', 'DMK vs AIADMK Kilpennathur; AIADMK competitive'),
    66: ('ADMK', 'M', 'DMDK vs PMK Polur; PMK Vanniyar dominant wins for AIADMK+'),
    67: ('ADMK', 'M', 'DMK vs AIADMK Arani; AIADMK traditionally competitive'),
    70: ('ADMK', 'M', 'DMK vs PMK Gingee; PMK Vanniyar belt wins for AIADMK+'),
    71: ('ADMK', 'M', 'DMDK vs AIADMK Mailam; AIADMK C. Ve. Shanmugam competitive'),
    72: ('ADMK', 'M', 'VCK vs AIADMK Tindivanam SC; AIADMK strong base'),
    75: ('ADMK', 'M', 'DMK vs PMK Vikravandi; PMK has significant Vanniyar vote'),
    78: ('ADMK', 'M', 'DMK vs PMK Rishivandiyam; PMK Vanniyar dominant'),
    82: ('ADMK', 'M', 'INC vs AIADMK Attur SC; AIADMK won 2021'),
    84: ('ADMK', 'M', 'DMDK vs AIADMK Omalur; AIADMK R. Mani Kongu'),
    85: ('ADMK', 'M', 'DMK vs AIADMK Mettur; Salem Kongu AIADMK competitive'),
    87: ('ADMK', 'M', 'DMK vs AIADMK Sangagiri; Salem Kongu competitive'),
    90: ('TVK', 'L', 'DMK vs AIADMK Salem South; TVK urban surge — 3-way toss-up'),
    96: ('ADMK', 'M', 'DMK/KMDK vs AIADMK Tiruchengodu; Kongu AIADMK competitive'),
    99: ('ADMK', 'M', 'DMK vs BJP(TMC-M) Erode West; BJP/AIADMK+ competitive Kongu'),
    105: ('ADMK', 'M', 'DMK vs AIADMK Anthiyur; Kongu AIADMK competitive'),
    106: ('ADMK', 'M', 'DMK vs AIADMK Gobichettipalayam; Kongu AIADMK V. B. Prabhu'),
    107: ('ADMK', 'M', 'CPI vs AIADMK Bhavanisagar SC; AIADMK Kongu likely'),
    108: ('ADMK', 'M', 'INC vs BJP Ooty; BJP/AIADMK+ has support in Nilgiris hills'),
    111: ('ADMK', 'M', 'DMK vs AIADMK Mettupalayam; Kongu AIADMK O. K. Chinnaraj'),
    113: ('ADMK', 'M', 'CPI vs AIADMK Tiruppur North; AIADMK Kongu competitive'),
    114: ('TVK', 'L', 'DMK vs BJP Tiruppur South; TVK urban industrial vote could flip'),
    117: ('ADMK', 'M', 'INC vs AIADMK Kavundampalayam; Coimbatore AIADMK competitive'),
    118: ('TVK', 'L', 'DMK vs BJP Coimbatore North; TVK strong urban — Vanathi vs DMK+TVK 3-way'),
    121: ('ADMK', 'M', 'INC vs AIADMK Singanallur; Coimbatore AIADMK competitive'),
    126: ('ADMK', 'M', 'DMK vs AMMK Madathukulam; AMMK (AIADMK+) Tiruppur competitive'),
    139: ('TVK', 'L', 'DMK vs AIADMK Srirangam; TVK very popular in Trichy 3-way'),
    140: ('TVK', 'L', 'DMK K. N. Nehru vs AMMK Trichy West; TVK urban Trichy surge possible'),
    141: ('TVK', 'L', 'DMK vs AIADMK Trichy East; TVK Trichy urban could surprise'),
    143: ('ADMK', 'M', 'DMK vs AIADMK Lalgudi; AIADMK Leema Rose Martin competitive'),
    144: ('ADMK', 'M', 'DMK vs AIADMK(STMK) Manachanallur; AIADMK competitive'),
    145: ('ADMK', 'M', 'DMK vs AIADMK Musiri; AIADMK N. Yoganathan hold'),
    146: ('ADMK', 'M', 'INC vs AIADMK Thuraiyur SC; AIADMK E. Suroja competitive'),
    154: ('ADMK', 'M', 'VCK vs AIADMK Panruti; AIADMK K. Mohan hold'),
    155: ('ADMK', 'M', 'INC vs AIADMK Cuddalore HQ; AIADMK M. C. Sampath competitive'),
    159: ('ADMK', 'M', 'VCK vs PMK Kattumannarkoil SC; PMK wins for AIADMK+'),
    177: ('ADMK', 'M', 'DMK vs AIADMK Peravurani; AIADMK coastal Thanjavur competitive'),
    179: ('ADMK', 'M', 'DMK vs AIADMK Viralimalai; AIADMK C. Vijayabhaskar incumbent'),
    181: ('ADMK', 'M', 'DMK vs AIADMK Thirumayam; AIADMK P. K. Vairamuthu competitive'),
    183: ('ADMK', 'M', 'INC vs BJP(ADMK+) Aranthangi; BJP/AIADMK+ competitive'),
    184: ('ADMK', 'M', 'INC vs AMMK Karaikudi; AMMK (AIADMK+) competitive Sivaganga'),
    188: ('ADMK', 'M', 'INC vs AIADMK Melur; Thevar belt AIADMK competitive Madurai'),
    189: ('TVK', 'L', 'DMK vs AIADMK Madurai East; TVK urban Madurai surge 3-way'),
    191: ('TVK', 'L', 'DMK vs AIADMK Madurai North; TVK urban surge — G. Thalapathy vs TVK'),
    192: ('TVK', 'L', 'DMK/MDMK vs BJP Madurai South; TVK Madurai urban could win'),
    197: ('ADMK', 'M', 'INC vs AIADMK Usilampatti; Thevar belt AIADMK I. Mahendran'),
    205: ('ADMK', 'M', 'INC vs AIADMK Sivakasi; AIADMK K. T. Rajenthra Bhalaji competitive'),
    210: ('ADMK', 'M', 'INC vs AIADMK Tiruvadanai; coastal Ramanathapuram AIADMK competitive'),
    216: ('ADMK', 'M', 'INC vs AIADMK Srivaikuntam; AIADMK S. P. Shanmuganathan competitive'),
    219: ('ADMK', 'M', 'INC vs AIADMK Sankarankovil SC; AIADMK competitive Tenkasi'),
    225: ('ADMK', 'M', 'INC vs AIADMK Ambasamudram; AIADMK Isakki Subhaya competitive'),
    231: ('ADMK', 'M', 'INC vs BJP Colachal; BJP/AIADMK+ T. Sivakumar competitive'),
    232: ('ADMK', 'M', 'CPI(M) vs BJP Padmanabhapuram; BJP P. Ramesh competitive'),
    233: ('ADMK', 'M', 'INC vs BJP Vilavancode; BJP S. Vijayadharani competitive'),
    234: ('ADMK', 'M', 'INC vs BJP(TMC-M) Killiyoor; BJP competitive Kanyakumari'),
}
PREDICTIONS.update(_OVERRIDES)

def party_color(party):
    colors = {
        "DMK":    "#E31A1C",
        "INC":    "#19AAED",
        "VCK":    "#4B0082",
        "CPI(M)": "#CC0000",
        "CPI":    "#CC0000",
        "DMDK":   "#FF6600",
        "IUML":   "#006400",
        "MDMK":   "#8B0000",
        "KMDK":   "#8B4513",
        "MMK":    "#228B22",
        "MJK":    "#708090",
        "SDPI":   "#006400",
        "TDK":    "#8B8000",
        "MPP":    "#800000",
    }
    return colors.get(party, "#555555")

def winner_color(winner):
    return {"SPA": "#E31A1C", "ADMK": "#006400", "TVK": "#FF8C00", "OTHER": "#6B4C9A"}.get(winner, "#555")

def winner_label(winner):
    return {"SPA": "DMK+ (SPA)", "ADMK": "AIADMK+", "TVK": "TVK", "OTHER": "Other"}.get(winner, winner)

def conf_color(conf):
    return {"H": "#2ea043", "M": "#d29922", "L": "#f85149"}.get(conf, "#555")

def conf_label(conf):
    return {"H": "High Confidence", "M": "Moderate", "L": "Toss-Up"}.get(conf, conf)

# Count predictions
counts = {"SPA": 0, "ADMK": 0, "TVK": 0, "OTHER": 0}
for v in PREDICTIONS.values():
    counts[v[0]] += 1

def generate_html():
    # Build rows
    rows_html = []
    for c in CONSTITUENCIES:
        no, name, district, sc_st, spa_party, spa_cand, admk_party, admk_cand, tvk_notable = c
        pred_winner, pred_conf, pred_note = PREDICTIONS.get(no, ("SPA", "M", ""))
        sc_badge = f'<span style="font-size:0.68rem;background:#444;padding:1px 5px;border-radius:3px;margin-left:4px;">{sc_st}</span>' if sc_st else ""
        tvk_star = '<span title="TVK Star Seat" style="color:#FF8C00;margin-left:4px;">★TVK</span>' if tvk_notable else ""

        row_class = "exit-row" if pred_winner == "ADMK" else ("tvk-row" if pred_winner == "TVK" else "")

        spa_color = party_color(spa_party)
        admk_color = "#006400" if admk_party in ["AIADMK","PMK","AMMK","BJP"] else "#555"
        admk_text_color = {"AIADMK":"#006400","PMK":"#ff6600","AMMK":"#8B0000","BJP":"#FF9933"}.get(admk_party,"#555")

        rows_html.append(f"""
        <tr class="{row_class}">
          <td style="color:#8b949e;text-align:center">{no}</td>
          <td><strong>{name}</strong>{sc_badge}{tvk_star}</td>
          <td style="color:#8b949e">{district}</td>
          <td>
            <span style="color:{spa_color};font-weight:600;font-size:0.78rem">{spa_party}</span>
            <div style="font-size:0.8rem;color:#e6edf3">{spa_cand}</div>
          </td>
          <td>
            <span style="color:{admk_text_color};font-weight:600;font-size:0.78rem">{admk_party}</span>
            <div style="font-size:0.8rem;color:#e6edf3">{admk_cand}</div>
          </td>
          <td style="text-align:center">
            <span style="background:{winner_color(pred_winner)};color:#fff;padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:700">{winner_label(pred_winner)}</span>
          </td>
          <td style="text-align:center">
            <span style="color:{conf_color(pred_conf)};font-size:0.75rem;font-weight:600">{conf_label(pred_conf)}</span>
          </td>
          <td style="font-size:0.75rem;color:#8b949e;max-width:220px">{pred_note}</td>
        </tr>""")

    rows_str = "\n".join(rows_html)

    spa_count = counts["SPA"]
    admk_count = counts["ADMK"]
    tvk_count = counts["TVK"]
    oth_count = counts["OTHER"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TN 2026 — Constituency-wise Prediction</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg:#0d1117; --card:#161b22; --border:#30363d;
    --text:#e6edf3; --muted:#8b949e; --accent:#58a6ff;
    --dmk:#E31A1C; --admk:#006400; --tvk:#FF8C00; --others:#6B4C9A;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; }}
  header {{
    background:linear-gradient(135deg,#1a0a00,#0d1117 40%,#001a33);
    border-bottom:2px solid var(--border);
    padding:24px 40px; display:flex; align-items:center; gap:16px;
  }}
  .flag {{ width:6px; height:70px; background:linear-gradient(to bottom,#ff9933 33%,#fff 33% 66%,#138808 66%); border-radius:4px; }}
  header h1 {{ font-size:1.7rem; font-weight:800; }}
  header h1 span {{ color:var(--accent); }}
  header .meta {{ font-size:0.8rem; color:var(--muted); margin-top:3px; }}
  .live {{ margin-left:auto; background:#ff4444; color:#fff; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:700; animation:pulse 1.4s infinite; }}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}

  main {{ max-width:1600px; margin:0 auto; padding:24px 16px; }}
  .section-title {{
    font-size:0.95rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px;
    color:var(--accent); border-left:4px solid var(--accent); padding-left:10px; margin:28px 0 14px;
  }}

  /* Summary Cards */
  .sum-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:20px; }}
  @media(max-width:800px){{.sum-grid{{grid-template-columns:repeat(2,1fr);}}}}
  .s-card {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:18px; position:relative; overflow:hidden; }}
  .s-card::before {{ content:''; position:absolute; top:0; left:0; width:100%; height:4px; background:var(--c); }}
  .s-card .label {{ font-size:0.72rem; color:var(--muted); font-weight:600; text-transform:uppercase; letter-spacing:1px; }}
  .s-card .seats {{ font-size:2.4rem; font-weight:900; color:var(--c); line-height:1; margin:6px 0; }}
  .s-card .pct {{ font-size:0.82rem; color:var(--muted); }}

  /* Charts row */
  .charts-row {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px; }}
  @media(max-width:700px){{.charts-row{{grid-template-columns:1fr;}}}}
  .chart-card {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:18px; }}
  .chart-title {{ font-size:0.82rem; color:var(--muted); font-weight:600; text-transform:uppercase; margin-bottom:12px; }}
  .chart-wrap {{ position:relative; height:260px; }}

  /* Exit Poll quick summary */
  .ep-strip {{
    background:var(--card); border:1px solid #2d5a8e; border-radius:10px;
    padding:14px 20px; margin-bottom:20px; display:flex; flex-wrap:wrap; gap:20px; align-items:center;
  }}
  .ep-strip .label {{ font-size:0.75rem; color:var(--accent); font-weight:700; text-transform:uppercase; }}
  .ep-item {{ text-align:center; }}
  .ep-item .agency {{ font-size:0.7rem; color:var(--muted); }}
  .ep-item .nums {{ font-size:0.9rem; font-weight:700; }}

  /* Search/Filter bar */
  .filter-bar {{ display:flex; flex-wrap:wrap; gap:10px; margin-bottom:14px; align-items:center; }}
  .filter-bar input {{
    background:#1c2128; border:1px solid var(--border); color:var(--text);
    padding:6px 12px; border-radius:6px; font-size:0.82rem; flex:1; min-width:200px;
  }}
  .filter-bar select {{
    background:#1c2128; border:1px solid var(--border); color:var(--text);
    padding:6px 10px; border-radius:6px; font-size:0.82rem;
  }}
  .filter-bar .count-badge {{
    background:var(--card); border:1px solid var(--border); border-radius:6px;
    padding:6px 12px; font-size:0.8rem; color:var(--muted);
  }}

  /* Table */
  .table-wrap {{ overflow-x:auto; border-radius:10px; border:1px solid var(--border); }}
  table {{ width:100%; border-collapse:collapse; font-size:0.82rem; }}
  thead th {{
    background:#1c2128; color:var(--muted); font-size:0.7rem; text-transform:uppercase;
    letter-spacing:.8px; padding:10px 10px; text-align:left;
    border-bottom:1px solid var(--border); position:sticky; top:0; z-index:10;
    white-space:nowrap;
  }}
  tbody tr {{ border-bottom:1px solid var(--border); transition:background .15s; }}
  tbody tr:hover {{ background:rgba(88,166,255,.05); }}
  tbody td {{ padding:8px 10px; vertical-align:middle; }}
  .exit-row {{ background:rgba(0,100,0,.05); }}
  .exit-row td:first-child {{ border-left:3px solid var(--admk); }}
  .tvk-row {{ background:rgba(255,140,0,.05); }}
  .tvk-row td:first-child {{ border-left:3px solid var(--tvk); }}

  .key-seat {{ background:rgba(255,215,0,.04) !important; }}
  .key-seat td:first-child {{ border-left:3px solid #ffd700 !important; }}

  /* Legend */
  .legend {{ display:flex; gap:16px; flex-wrap:wrap; margin-bottom:12px; font-size:0.78rem; }}
  .legend-item {{ display:flex; align-items:center; gap:6px; }}
  .legend-dot {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}

  /* Stats bar */
  .stats-bar {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 20px; display:flex; gap:24px; flex-wrap:wrap; margin-bottom:20px; }}
  .stat-item {{ text-align:center; }}
  .stat-num {{ font-size:1.6rem; font-weight:900; }}
  .stat-label {{ font-size:0.7rem; color:var(--muted); text-transform:uppercase; }}

  footer {{ border-top:1px solid var(--border); padding:20px 40px; text-align:center; color:var(--muted); font-size:0.75rem; margin-top:30px; }}
</style>
</head>
<body>

<header>
  <div class="flag"></div>
  <div>
    <h1>TN 2026 — <span>Constituency-wise Prediction</span></h1>
    <div class="meta">All 234 Assembly Constituencies &nbsp;|&nbsp; Exit Poll Based Prediction &nbsp;|&nbsp; Results: May 4, 2026</div>
  </div>
  <div class="live">ANALYSIS</div>
</header>

<main>

  <!-- EXIT POLL STRIP -->
  <div class="section-title">Exit Poll Consensus (April 29, 2026)</div>
  <div class="ep-strip">
    <div class="ep-item"><div class="agency">Agency</div><div class="nums" style="color:var(--accent)">Pollster</div></div>
    <div class="ep-item"><div class="agency">Chanakya Strategies</div><div class="nums" style="color:var(--dmk)">145–160</div><div class="agency">AIADMK+: 50–65 | TVK: 13–18</div></div>
    <div class="ep-item"><div class="agency">P-MARQ (Republic TV)</div><div class="nums" style="color:var(--dmk)">125–145</div><div class="agency">AIADMK+: 65–85 | TVK: 16–26</div></div>
    <div class="ep-item"><div class="agency">NDTV–People's Pulse</div><div class="nums" style="color:var(--dmk)">125–145</div><div class="agency">AIADMK+: 65–80 | TVK: 18–24</div></div>
    <div class="ep-item"><div class="agency">Matrize (IANS)</div><div class="nums" style="color:var(--dmk)">122–132</div><div class="agency">AIADMK+: 87–100 | TVK: 4–8</div></div>
    <div class="ep-item"><div class="agency">ABP-CVoter</div><div class="nums" style="color:var(--dmk)">132–148</div><div class="agency">AIADMK+: 72–88 | TVK: 8–16</div></div>
    <div class="ep-item" style="border-left:2px solid var(--accent);padding-left:16px;margin-left:4px">
      <div class="agency" style="color:var(--accent)">POLL OF POLLS</div>
      <div class="nums" style="color:var(--dmk)">138–153</div>
      <div class="agency">AIADMK+: 66–82 | TVK: 10–20 | Majority: 118</div>
    </div>
  </div>

  <!-- SUMMARY CARDS -->
  <div class="section-title">Prediction Summary (234 Constituencies)</div>
  <div class="sum-grid">
    <div class="s-card" style="--c:var(--dmk)">
      <div class="label">DMK+ (SPA) — Predicted</div>
      <div class="seats">{spa_count}</div>
      <div class="pct">of 234 seats &nbsp;|&nbsp; Exit poll range: 138–153</div>
    </div>
    <div class="s-card" style="--c:var(--admk)">
      <div class="label">AIADMK+ Alliance — Predicted</div>
      <div class="seats">{admk_count}</div>
      <div class="pct">of 234 seats &nbsp;|&nbsp; Exit poll range: 66–82</div>
    </div>
    <div class="s-card" style="--c:var(--tvk)">
      <div class="label">TVK (Vijay) — Predicted</div>
      <div class="seats">{tvk_count}</div>
      <div class="pct">of 234 seats &nbsp;|&nbsp; Exit poll range: 10–20</div>
    </div>
    <div class="s-card" style="--c:var(--others)">
      <div class="label">Others — Predicted</div>
      <div class="seats">{oth_count}</div>
      <div class="pct">of 234 seats &nbsp;|&nbsp; NTK, Indep., etc.</div>
    </div>
  </div>

  <!-- CHARTS -->
  <div class="charts-row">
    <div class="chart-card">
      <div class="chart-title">Predicted Seat Distribution</div>
      <div class="chart-wrap"><canvas id="donutChart"></canvas></div>
    </div>
    <div class="chart-card">
      <div class="chart-title">Regional Prediction Breakdown</div>
      <div class="chart-wrap"><canvas id="regionChart"></canvas></div>
    </div>
  </div>

  <!-- TABLE -->
  <div class="section-title">All 234 Constituencies — Candidate & Prediction</div>

  <div class="filter-bar">
    <input type="text" id="searchInput" placeholder="Search constituency, candidate, district..." oninput="filterTable()">
    <select id="districtFilter" onchange="filterTable()">
      <option value="">All Districts</option>
      <option>Tiruvallur</option><option>Chennai</option><option>Kanchipuram</option>
      <option>Chengalpattu</option><option>Ranipet</option><option>Vellore</option>
      <option>Tirupathur</option><option>Krishnagiri</option><option>Dharmapuri</option>
      <option>Tiruvannamalai</option><option>Viluppuram</option><option>Kallakurichi</option>
      <option>Salem</option><option>Namakkal</option><option>Erode</option>
      <option>Nilgiris</option><option>Coimbatore</option><option>Tiruppur</option>
      <option>Dindigul</option><option>Karur</option><option>Tiruchirappalli</option>
      <option>Perambalur</option><option>Ariyalur</option><option>Cuddalore</option>
      <option>Mayiladuthurai</option><option>Nagapattinam</option><option>Tiruvarur</option>
      <option>Thanjavur</option><option>Pudukkottai</option><option>Sivaganga</option>
      <option>Madurai</option><option>Theni</option><option>Virudhunagar</option>
      <option>Ramanathapuram</option><option>Thoothukudi</option><option>Tenkasi</option>
      <option>Tirunelveli</option><option>Kanyakumari</option>
    </select>
    <select id="winnerFilter" onchange="filterTable()">
      <option value="">All Predictions</option>
      <option value="DMK+">DMK+ (SPA)</option>
      <option value="AIADMK+">AIADMK+</option>
      <option value="TVK">TVK</option>
    </select>
    <select id="confFilter" onchange="filterTable()">
      <option value="">All Confidence</option>
      <option value="High">High Confidence</option>
      <option value="Moderate">Moderate</option>
    </select>
    <div class="count-badge" id="countBadge">Showing 234 of 234</div>
  </div>

  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:var(--dmk)"></div> DMK+ (SPA) Predicted Win</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--admk)"></div> AIADMK+ Predicted Win</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--tvk)"></div> TVK Predicted Win</div>
    <div class="legend-item"><div class="legend-dot" style="background:#ffd700"></div> Key / High-profile Seat (★)</div>
  </div>

  <div class="table-wrap">
    <table id="mainTable">
      <thead>
        <tr>
          <th style="width:40px">No.</th>
          <th>Constituency</th>
          <th>District</th>
          <th>SPA Candidate</th>
          <th>AIADMK+ Candidate</th>
          <th>Predicted Winner</th>
          <th>Confidence</th>
          <th>Analysis Note</th>
        </tr>
      </thead>
      <tbody id="tableBody">
{rows_str}
      </tbody>
    </table>
  </div>

  <div style="margin-top:16px;padding:14px 18px;background:var(--card);border:1px solid #444;border-radius:8px;font-size:0.8rem;color:var(--muted);line-height:1.7;">
    <strong style="color:#ffd700">⚠️ Disclaimer:</strong>
    Constituency-level predictions are analytical estimates based on 2021 election results, exit poll aggregates (Chanakya, P-MARQ, NDTV, Matrize, ABP-CVoter), regional swing patterns, and candidate factors. Individual constituency outcomes can vary by ±20–30 seats from aggregate predictions. TVK vote share distribution is highly uncertain in first election. Results to be declared <strong>May 4, 2026</strong>.
    Candidate data sourced from: <em>Wikipedia — 2026 Tamil Nadu Legislative Assembly election</em> (as on April 29, 2026).
  </div>

</main>

<footer>
  TN 2026 Constituency Prediction Dashboard &nbsp;|&nbsp; Data: Wikipedia / ECI / Exit Poll Agencies &nbsp;|&nbsp; Analysis Date: April 29, 2026
</footer>

<script>
// ─── Donut Chart ─────────────────────────────────────
new Chart(document.getElementById('donutChart'), {{
  type: 'doughnut',
  data: {{
    labels: ['DMK+ Alliance ({spa_count})', 'AIADMK+ ({admk_count})', 'TVK ({tvk_count})', 'Others ({oth_count})'],
    datasets: [{{
      data: [{spa_count}, {admk_count}, {tvk_count}, {oth_count}],
      backgroundColor: ['#E31A1C', '#006400', '#FF8C00', '#6B4C9A'],
      borderColor: '#0d1117', borderWidth: 3, hoverOffset: 8,
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false, cutout: '58%',
    plugins: {{
      legend: {{ labels: {{ color: '#e6edf3', font: {{ size: 11 }}, padding: 16 }}, position: 'right' }},
    }}
  }}
}});

// ─── Regional Chart ──────────────────────────────────
new Chart(document.getElementById('regionChart'), {{
  type: 'bar',
  data: {{
    labels: ['North TN\\n(69 seats)', 'West TN\\n(68 seats)', 'South TN\\n(51 seats)', 'Central TN\\n(46 seats)'],
    datasets: [
      {{ label: 'DMK+ (SPA)', data: [55, 32, 38, 22], backgroundColor: '#E31A1C44', borderColor: '#E31A1C', borderWidth: 2, borderRadius: 4 }},
      {{ label: 'AIADMK+',   data: [10, 32, 10, 22], backgroundColor: '#00640044', borderColor: '#006400', borderWidth: 2, borderRadius: 4 }},
      {{ label: 'TVK',       data: [4,  4,  3,  4],  backgroundColor: '#FF8C0044', borderColor: '#FF8C00', borderWidth: 2, borderRadius: 4 }},
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ labels: {{ color: '#8b949e', font: {{ size: 10 }} }} }} }},
    scales: {{
      x: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#8b949e', font: {{ size: 10 }} }} }},
      y: {{ grid: {{ color: '#30363d' }}, ticks: {{ color: '#8b949e' }}, stacked: false, max: 70 }}
    }}
  }}
}});

// ─── Filter / Search ─────────────────────────────────
function filterTable() {{
  const search = document.getElementById('searchInput').value.toLowerCase();
  const district = document.getElementById('districtFilter').value.toLowerCase();
  const winner = document.getElementById('winnerFilter').value.toLowerCase();
  const conf = document.getElementById('confFilter').value.toLowerCase();

  const rows = document.querySelectorAll('#tableBody tr');
  let visible = 0;
  rows.forEach(row => {{
    const text = row.textContent.toLowerCase();
    const matchSearch = !search || text.includes(search);
    const matchDist = !district || text.includes(district);
    const matchWin = !winner || text.includes(winner);
    const matchConf = !conf || text.includes(conf);
    if (matchSearch && matchDist && matchWin && matchConf) {{
      row.style.display = '';
      visible++;
    }} else {{
      row.style.display = 'none';
    }}
  }});
  document.getElementById('countBadge').textContent = `Showing ${{visible}} of 234`;
}}
</script>

</body>
</html>"""
    return html

if __name__ == "__main__":
    import os
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "TN_2026_Constituency_Prediction.html")
    html = generate_html()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {out_path}")
    # Count stats
    counts = {"SPA": 0, "ADMK": 0, "TVK": 0, "OTHER": 0}
    for v in PREDICTIONS.values():
        counts[v[0]] += 1
    print(f"Prediction counts: DMK+={counts['SPA']}, AIADMK+={counts['ADMK']}, TVK={counts['TVK']}, Others={counts['OTHER']}")

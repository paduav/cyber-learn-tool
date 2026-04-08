# database/seed_data.py


import sqlite3

DB_PATH = "activities.db"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    activities = [
        (
            "NOVA Cybersecurity Lab",
            "Network Security, Privacy, Passwords, Social Engineering",
            "Students will be able to explain how to engage in positive, safe, legal and ethical behavior when using technology, including social interactions online or when using networked devices.",
            "Integrate quantitative or technical information expressed in words in a text with a version of that information expressed visually,",
            "Computer/laptop or mobile device, internet connection",
            75,
            None,
            "Intermediate",
            "Online, Individual game",
            "network, security, privacy, passwords, social engineering, lab, online, game, individual, intermediate",
            "https://thinktv.pbslearningmedia.org/resource/nvcy-sci-cyberlab/nova-cybersecurity-lab/nova-premium-collection/"
        ),
        (
            "Space Shelter",
            "Passwords, Authentication, Phishing, Social Engineering",
            "Students will be able to: create a strong, complex password, identify the different methods of 2-factor authentication, identify phishing emails/messages.",
            "Digital Citizenship, K-12 Cybersecurity Standards, ISTE Standards",
            "Computer/laptop or mobile device, internet connection",
            30,
            45,
            "Beginner",
            "Online, Individual, Guided game",
            "password, authentication, phishing, social engineering, beginner, online, game, individual",
            "https://games.gamindo.com/videogames/google/1/?https://games.gamindo.com/videogames/google/"
        ),
        (
            "Gandalf AI",
            "AI security, Prompt Injection, LLM Vulnerabilities",
            "Students will be able to define prompt injection and explain why it is a cybersecurity risk in AI systems.",
            "UNESCO, CSTA, K-12 3B-NI-04, ISTE Standards",
            "Computer/laptop, Internet connection",
            60,
            None,
            "Advanced",
            "Online, individual game",
            "advanced, ai, artificial intelligence, prompt, injection, llm, vulnerability, online, game, individual",
            "https://gandalf.lakera.ai/intro"
        ),
        (
            "CryptoHack",
            "Cryptography",
            "Students will be able to apply foundational cryptography concepts, use Python to manipulate data.",
            "NIST, AES",
            "Computer/laptop, CryptoHack account, Python environment, Internet connection",
            60,
            None,
            "Advanced",
            "Online, Individual CTF challenge platform",
            "advanced, cryptography, hack, python, ctf, capture the flag, online, individual",
            "https://cryptohack.org/"
        ),
        (
            "Interland",
            "Online Safety, Digital Citizenship, Privacy, Phishing, Social Engineering, Passwords",
            "Students will be able to Identify phishing scams and unsafe downloadss, demonstrate strategies for protecting personal information online, recognize characteristics of strong passwords, apply responsible digital citizenship behaviors.",
            "CSTA, NICE",
            "Computer/laptop, Internet connection",
            30,
            45,
            "Beginner",
            "Online, Individual game",
            "beginner, safety, digital citizenship, privacy, phishing, social engineering, passwords, online, individual",
            "https://beinternetawesome.withgoogle.com/en_us/interland/"
        ),
        (
            "Impersonation & Identity Theft",
            "Privacy",
            "Students will be able to define impersonation and identity theft, reflect on the potential impacts of someone else using your identity, review strategies for securing information online.",
            "ISTE, K-12 Cybersecurity Standards",
            "Lesson slides, Unsecured accounts handout",
            30,
            None,
            "Intermediate",
            "Collaborative discussion, Lesson plan",
            "intermediate, privacy, impersonation, identity theft, collaborative, discussion, lesson, slides",
            "https://www.commonsense.org/education/digital-citizenship/lesson/impersonation-and-identity-theft"
        ),
        (
            "Being Aware of What You Share",
            "Online Safety, Digital Citizenship, Privacy",
            "Students will be able to reflect on the concept of privacy, analyze different ways that advertisers collect information to send users targeted ads, identify strategies for protecting their privacy, like opting out of specific features and analyzing app policies.",
            "Common Core ELA, ISTE, CASEL, AASL",
            "Lesson slides, Ad detective handout, Lesson quiz",
            50,
            None,
            "Beginner, Intermediate",
            "Collaborative discussion, Lesson plan with individual quiz",
            "beginner, intermediate, online, safety, digital citizenship, privacy, handout, discussion, collaborative, lesson, quiz, slides",
            "https://www.commonsense.org/education/digital-citizenship/lesson/being-aware-of-what-you-share"
        ),
        (
            "Guess the Object: Thinking Like AI",
            "Artificial Intelligence, Computer Vision",
            "Students will be able to understand how computer vision systems identify objects based on physical characteristics rather than function, practice computational thinking skills such as abstraction and decomposition, recognize differences between human reasoning and AI-based object recognition",
            "ISTE, K-12 Cybersecurity Standards",
            "Object cards, Open space for group play.",
            60,
            90,
            "Beginner",
            "Interactive group card game",
            "beginner, ai, artificial intelligence, computer vision, object, recognition, group, card, game",
            "https://pa-gov.libguides.com/ld.php?content_id=76709554"
        ),
        (
            "Facing Off With Facial Recognition",
            "Digital Citizenship, Artificial Intelligence, Privacy",
            "Students will be able to understand what facial recognition is, consider the benefits and risks of facial recognition.",
            "ISTE, K-12 Cybersecurity Standards",
            "Lesson slides and handout",
            20,
            None,
            "Beginner, Intermediate",
            "Collaborative discussion, Lesson plan",
            "beginner, intermediate, facial recognition, digital citizenship, ai, artificial intelligence, privacy, slides, handout, collaborative, discussion",
            "https://www.commonsense.org/education/digital-citizenship/lesson/facing-off-with-facial-recognition"
        ),
        (
            "Hack-A-Cat: Your Cybersecurity Adventure",
            "Digital Citizenship, Phishing, Social Engineering",
            "Students will be able to recognize phishing attempts, define and identify Ransomware and VPNs.",
            "ISTE, K-12 Cybersecurity Standards",
            "Computer/laptop, Internet connection",
            30,
            None,
            "Beginner, Intermediate",
            "Online, Individual game",
            "beginner, intermediate, digital citizenship, phishing, social engineering, ransomware, vpn, game, online, individual",
            "https://training.knowbe4.com/modstore/view/4be6a93b-b380-4e5a-934a-27b12674d841"
        ),
        (
            "AI Safety for Students",
            "AI safety",
            "Students will be able to explain what Artificial Intelligence (AI) is, navigate the digital world safely while benefiting from AI capabilities",
            "ISTE, K-12 Cybersecurity Standards",
            "Computer/laptop, Internet connection",
            30,
            None,
            "Beginner, Intermediate",
            "Online, Individual game",
            "beginner, intermediate, ai, safety, online, individual, game",
            "https://training.knowbe4.com/modstore/view/faf8def0-1248-4f50-a171-634fa207f1ac"
        ),
        (
            "Building a Cypher Disk",
            "Cryptography",
            "Students will be able to understand the basic concepts of encryption and decryption by using a substitution cipher, apply problem-solving and pattern recognition skills to decrypt messages made by others, recognize the role of cryptography in cybersecurity",
            "Cryptography (CRY), NICE",
            "Scissors, a brad, markers, pages T50-T51",
            40,
            60,
            "Beginner, Intermediate",
            "Hands-on, Individual and group activity",
            "beginner, intermediate, cryptography, encryption, decryption, cipher, messages, individual, group, activity, hands-on, physical",
            "https://cyber.org/news/classroom-activity-building-cypher-disk"
        ),
        (
            "Denial-of-Service Attack Group Activity",
            "Malware, Cyber threats",
            "Students will be able to execute a denial-of-service attack on a model of a computer network, determine quantitative metrics that can measure impact of a DDoS attack, design and test a solution to prevent a DDoS attack on a model of a computer network",
            "Next Generation Science Standards MS-ETS1-3, MS-ETS1-4",
            "Timer, 9x12 colored construction paper, scissors, server queue handout, processing paper handout, clear tape, boxes to collect cards, permanent marker, pen/pencil per participant",
            60,
            None,
            "Intermediate",
            "Collaborative group activity",
            "intermediate, group, collaborative, ddos, malware, threats, denial of service",
            "https://www.sciencebuddies.org/teacher-resources/lesson-plans/cybersecurity-denial-of-service#summary"
        ),
        (
            "316ctf: CTF",
            "Cryptography, Network Security",
            "Students will be able to apply cybersecurity problem-solving skills to identify vulnerabilities, decode encrypted information, and analyze network data, practice common cybersecurity tools and techniques such as password cracking, cryptographic decoding, and online investigation methods.",
            "K-12 Cybersecurity Standards - CRY, Network Security (NET), NICE",
            "Computer/laptop, Internet connection, 316ctf account, cybersecurity tools like Wireshark, John The Ripper, Linux virtual machine",
            45,
            60,
            "Advanced",
            "Online, Individual, CTF challenge platform",
            "advanced, online, individual, ctf, capture the flag, cryptography, network, security, encrypt, decode, password",
            "https://316ctf.com/"
        ),
        (
            "KC7 Cyber Detective",
            "Malware, Cyber threats, Incident response",
            "Students will be able to use SQL queries to examine how logs work, what attackers do, and where to look for evidence. By practicing this, students will develop judgment skills and pattern recognition.",
            "NICE,NIST",
            "Computer/laptop, Internet connection",
            30,
            60,
            "Beginner, Intermediate, Advanced",
            "Online, Individual game",
            "advanced, beginner, intermediate, online, game, detective, malware, threats, incident response, sql, logs, individual",
            "https://kc7cyber.com/"
        ),
        (
            "Threats to Networks Game Idea",
            "Network Security, Cyber Threats, MITM, Packet Sniffing, DoS",
            "Students will be able to recognize network vulnerabilities and understand how networks transmit data.",
            "CSTA 2-NI-2",
            "Rope or tape lines, envelopes, binder clips, notecards",
            30,
            None,
            "Beginner",
            "Hands-on, Physical, Group activity",
            "beginner, group, threats, network, security, game, mitm, packets, dos, data",
            "https://sites.google.com/view/nifty-assignments/home/2021/unplug-the-internet"
        ),
        (
            "CMD Challenge",
            "Operating Systems, Command Line",
            "Students will be able to navigate a file system using basic command line commands, practice executing commands such as listing files, changing directories, and manipulating files.",
            "K-12 Cybersecurity Standards, Computer Science Standards",
            "Computer/laptop, Internet connection",
            45,
            None,
            "Intermediate",
            "Online, Individual game",
            "intermediate, online, game, command line, operating system, os, cmd ,cli, individual, terminal",
            "https://cmdchallenge.com/"
        ),
        (
            "Amanita Whitehat 1 & 2",
            "Malware, Cyber Threats, Social Engineering",
            "Students will be able to identify common cyber threats such as malware, phishing, and suspicious downloads, respond to potential cybersecurity risks.",
            "K-12 Cybersecurity Standards, NICE",
            "Computer/laptop, Internet connection",
            45,
            None,
            "Beginner, Intermediate",
            "Online, Individual game",
            "intermediate, online, game, beginner, puzzle, malware, threats, social engineering, phishing, download, risk, individual",
            "https://cryptologicfoundation.org/resources/cyber-games/amanita-whitehat-2/"
        ),
        (
            "OverTheWire: Bandit",
            "Operating Systems, Command Line",
            "Students will be able to develop foundational Linux command line skills, learn how to navigate files, read file contents, and search for information, apply problem-solving skills to progress through challenges.",
            "K-12 Cybersecurity Standards, NICE",
            "Computer/laptop, Internet connection, terminal or SSH client",
            45,
            60,
            "Advanced",
            "Online, Individual, CTF platform",
            "advanced, online, individual, ctf, capture the flag, os, operating system, command line, cmd, cli, linux, ssh, terminal",
            "https://overthewire.org/wargames/"
        )
    ]

    cursor.executemany("""
    INSERT INTO activities (
        title, topic, learning_objectives, standards, materials, min_time_minutes, max_time_minutes, difficulty, activity_type, tags, link
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, activities)

    conn.commit()
    conn.close()

    print("\nSample data inserted!\n")

if __name__ == "__main__":
    seed_data()
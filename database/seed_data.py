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
            "advanced, cryptography, hack, python, ctf, capture the flag, online",
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
            "beginner, safety, digital citizenship, privacy, phishing, social engineering, passwords, online",
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

    print("Sample data inserted!")

if __name__ == "__main__":
    seed_data()
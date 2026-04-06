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
            "Computer/laptop or mobile device",
            75,
            None,
            "Intermediate",
            "Online, individual game",
            "network, security, privacy, passwords, social engineering, lab, online, game, individual, intermediate",
            "https://thinktv.pbslearningmedia.org/resource/nvcy-sci-cyberlab/nova-cybersecurity-lab/nova-premium-collection/"

        ),
        (
            "Space Shelter",
            "Passwords, Authentication, Phishing, Social Engineering",
            "Students will be able to: create a strong, complex password, identify the different methods of 2-factor authentication, identify phishing emails/messages.",
            "Computer/laptop or mobile device",
            30,
            45,
            "Beginner",
            "Online, individual, guided game",
            "password, authentication, phishing, social engineering, beginner, online, game, individual",
            "https://games.gamindo.com/videogames/google/1/?https://games.gamindo.com/videogames/google/"

        )
    ]

    cursor.executemany("""
    INSERT INTO activities (
        title, topic, learning_objectives, materials, min_time_minutes, max_time_minutes, difficulty, activity_type, tags, link
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, activities)

    conn.commit()
    conn.close()

    print("Sample data inserted!")

if __name__ == "__main__":
    seed_data()
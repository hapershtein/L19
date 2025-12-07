"""
Message generation functions for different styles
"""


class MessageGenerators:
    """Generate feedback messages in different styles based on grades"""

    @staticmethod
    def generate_trump_message(repo_data):
        """Generate congratulation message in Donald Trump's style (90+)"""
        grade = repo_data['grade']

        messages = [
            f"INCREDIBLE! Absolutely INCREDIBLE! This code is {grade}% modular - that's TREMENDOUS! "
            f"Nobody writes code this good. Nobody. I've seen a lot of code, believe me, and this is "
            f"THE BEST. Beautiful, clean, modular - just perfect. This developer is a WINNER. "
            f"We need more developers like this. The BEST developers. Fantastic job!",

            f"WOW! {grade}% modularity - that's AMAZING! This is what I call WINNING code! "
            f"Very professional, very clean. The files are small, organized - just the way it should be. "
            f"I know quality when I see it, and this is QUALITY. Top tier. First class. "
            f"This developer gets it. They really get it. EXCELLENT work!",

            f"Let me tell you something - this code is SPECTACULAR! {grade}% modular. That's the kind of "
            f"number winners get. BIG LEAGUE coding right here. The structure is perfect, the organization "
            f"is perfect - everything is just PERFECT. This is how you write code. "
            f"Tremendous achievement. Really tremendous. CONGRATULATIONS!",
        ]

        idx = hash(repo_data['id']) % len(messages)
        return messages[idx]

    @staticmethod
    def generate_netanyahu_message(repo_data):
        """Generate positive feedback in Benjamin Netanyahu's style (70-89)"""
        grade = repo_data['grade']

        messages = [
            f"Let me be clear: achieving {grade}% modularity demonstrates solid technical capability. "
            f"The evidence shows a well-structured codebase with thoughtful organization. "
            f"This level of modular design reflects an understanding of best practices and maintainability. "
            f"The data speaks for itself - this is commendable work. With continued focus on these "
            f"principles, even greater achievements lie ahead. Well done.",

            f"Analysis of this codebase reveals {grade}% modularity - a strong result by any measure. "
            f"History teaches us that quality code is built through discipline and attention to structure. "
            f"This developer has demonstrated both. The small file architecture shows strategic thinking "
            f"and commitment to maintainability. This is the foundation upon which robust systems are built. "
            f"Good work. Continue on this path.",

            f"The metrics are clear: {grade}% modularity represents solid engineering. Throughout the "
            f"history of software development, we've learned that modular code leads to sustainable systems. "
            f"This codebase reflects that understanding. The balance between complexity and organization "
            f"is well-managed. This developer has made good choices. The foundation is strong. "
            f"Keep building on this success.",
        ]

        idx = hash(repo_data['id']) % len(messages)
        return messages[idx]

    @staticmethod
    def generate_hason_message(repo_data):
        """Generate improvement message in Shahar Hason's style (50-69)"""
        grade = repo_data['grade']

        messages = [
            f"אז... {grade}% modularity. לא רע, לא רע בכלל! (Not bad at all!) "
            f"But listen, we can do better here, right? It's like going to the gym - "
            f"you're doing good, but maybe add a few more reps? 😊 The code is okay, "
            f"some files are nice and small, but there's room to break things down more. "
            f"Think of it like hummus - better in small containers than one huge bucket! "
            f"You're on the right track, my friend. Just needs a bit more organization. "
            f"Keep going! 💪",

            f"So I looked at this code... {grade}% modular. אחלה התחלה! (Great start!) "
            f"You know what this reminds me of? My closet. Some things are organized, "
            f"some things... not so much. 😄 But that's okay! We all have that one drawer "
            f"that's messy. The important thing is you're trying! Break those big files "
            f"down a bit more, make it easier to find things. You got this! "
            f"I believe in you! ✨",

            f"{grade}% modularity - רגע, רגע (wait, wait)... this is like a falafel that's "
            f"good but could be GREAT with more tehina! 😋 The foundation is there, "
            f"the potential is there, but let's make those files smaller, yeah? "
            f"Break it down like you're explaining to your grandma - small pieces, "
            f"easy to understand. You're doing fine! Just needs some love. "
            f"Come on, you can do better! I'm rooting for you! 🎉",
        ]

        idx = hash(repo_data['id']) % len(messages)
        return messages[idx]

    @staticmethod
    def generate_amsalem_message(repo_data):
        """Generate brutally honest message in Dudi Amsalem's style (<50)"""
        grade = repo_data['grade']

        messages = [
            f"תקשיב טוב (Listen well) - {grade}% modularity?! זה לא מקובל! (This is unacceptable!) "
            f"What is this? Giant files, no organization, everything mixed together like a mess! "
            f"This is exactly the problem - no discipline, no structure! You think this is how "
            f"professionals write code?! די כבר! (Enough already!) Break these files down! "
            f"Small, focused, organized - that's what we need! Not this chaos! "
            f"Fix this immediately. This is not acceptable. We expect MUCH better! 💢",

            f"מה זה?! (What is this?!) {grade}% modular? This is a disaster! "
            f"Big files everywhere, no separation of concerns, no organization! "
            f"האם זה ברצינות?! (Are you serious?!) This is the kind of code that creates problems! "
            f"We need standards! We need quality! Not this mess! עוד פעם נגיד את זה - "
            f"(We'll say it again) - BREAK IT DOWN! Small files! Clear structure! "
            f"This needs MAJOR improvement. Now. לא מחר! (Not tomorrow!) NOW! ⚠️",

            f"אני לא מאמין! (I don't believe it!) {grade}% modularity is UNACCEPTABLE! "
            f"This is sloppy work! Everything in huge files, no thought about maintainability! "
            f"זה בדיוק מה שלא צריך לעשות! (This is exactly what you shouldn't do!) "
            f"You want to be taken seriously? Then write serious code! Organized! Modular! "
            f"Not this חוסר סדר (disorder)! We're not playing games here! "
            f"Fix this code RIGHT NOW! We need to see improvement IMMEDIATELY! 🔥",
        ]

        idx = hash(repo_data['id']) % len(messages)
        return messages[idx]

    @staticmethod
    def generate_message(repo_data):
        """
        Generate appropriate message based on grade

        Args:
            repo_data: Dictionary with repository data

        Returns:
            Generated message string
        """
        grade = repo_data['grade']

        if grade >= 90:
            return MessageGenerators.generate_trump_message(repo_data)
        elif grade >= 70:
            return MessageGenerators.generate_netanyahu_message(repo_data)
        elif grade >= 50:
            return MessageGenerators.generate_hason_message(repo_data)
        else:
            return MessageGenerators.generate_amsalem_message(repo_data)

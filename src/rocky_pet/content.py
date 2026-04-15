import random
from dataclasses import dataclass
from enum import Enum, auto


class QuestionCategory(Enum):
    TRIVIA = auto()
    PERSONAL = auto()
    FUN = auto()


@dataclass
class Question:
    text: str
    category: QuestionCategory
    choices: list[str]
    correct_index: int  # -1 means all answers valid (personal/fun)


@dataclass
class Quote:
    text: str
    emotion: str  # "happy", "sad", "curious", "excited"


@dataclass
class GiftItem:
    name: str
    description: str
    reaction_text: str
    reaction_emotion: str


class ContentManager:
    def __init__(self):
        self.questions = _build_questions()
        self.quotes = _build_quotes()
        self.gift_items = _build_gift_items()
        self._question_history: list[int] = []

    def get_random_question(self) -> Question:
        available = [
            i for i in range(len(self.questions))
            if i not in self._question_history[-10:]
        ]
        if not available:
            self._question_history.clear()
            available = list(range(len(self.questions)))
        idx = random.choice(available)
        self._question_history.append(idx)
        return self.questions[idx]

    def get_random_quote(self) -> Quote:
        return random.choice(self.quotes)


def _build_questions() -> list[Question]:
    return [
        # TRIVIA (10)
        Question("What fuel Hail Mary use?", QuestionCategory.TRIVIA,
                 ["Astrophage", "Hydrogen", "Xenon", "Plutonium"], 0),
        Question("What is Rocky home planet name?", QuestionCategory.TRIVIA,
                 ["Erid", "Mars", "Kepler", "Proxima"], 0),
        Question("What material Rocky make from?", QuestionCategory.TRIVIA,
                 ["Xenonite", "Steel", "Carbon", "Diamond"], 0),
        Question("How many arm Rocky have?", QuestionCategory.TRIVIA,
                 ["Five", "Four", "Six", "Eight"], 0),
        Question("What star Hail Mary travel to?", QuestionCategory.TRIVIA,
                 ["Tau Ceti", "Alpha Centauri", "Sirius", "Betelgeuse"], 0),
        Question("What is Grace job before space?", QuestionCategory.TRIVIA,
                 ["Teacher", "Pilot", "Doctor", "Engineer"], 0),
        Question("Astrophage eat what for energy?", QuestionCategory.TRIVIA,
                 ["Light from star", "Rocks", "Water", "Electricity"], 0),
        Question("What Rocky use to communicate first?", QuestionCategory.TRIVIA,
                 ["Musical tones", "Light signals", "Written words", "Hand signs"], 0),
        Question("How many crew on Hail Mary at start?", QuestionCategory.TRIVIA,
                 ["Three", "Two", "Five", "One"], 0),
        Question("What temperature Rocky like best?", QuestionCategory.TRIVIA,
                 ["Very hot", "Very cold", "Room temperature", "Freezing"], 0),
        # PERSONAL (9)
        Question("How you feel today, friend?", QuestionCategory.PERSONAL,
                 ["Happy!", "Okay", "Tired", "Stressed"], -1),
        Question("You eat good food today?", QuestionCategory.PERSONAL,
                 ["Yes, yummy!", "Not yet", "Just snacks", "No appetite"], -1),
        Question("You drink water? Water important!", QuestionCategory.PERSONAL,
                 ["Yes, lots!", "Some", "Not enough", "Drinking now!"], -1),
        Question("You take break today? Rest important!", QuestionCategory.PERSONAL,
                 ["Yes, rested!", "A little", "Too busy", "What is break?"], -1),
        Question("What you work on today?", QuestionCategory.PERSONAL,
                 ["Fun stuff!", "Work work", "Studying", "Relaxing"], -1),
        Question("You smile today? Smiling is good!", QuestionCategory.PERSONAL,
                 ["Big smile!", "A little", "Not yet", "Smiling now!"], -1),
        Question("You talk to friend today?", QuestionCategory.PERSONAL,
                 ["Yes!", "Not yet", "I talk to you, Rocky!", "Later"], -1),
        Question("You sleep good last night?", QuestionCategory.PERSONAL,
                 ["Great sleep!", "Okay sleep", "Bad sleep", "What is sleep?"], -1),
        Question("You do something fun today?", QuestionCategory.PERSONAL,
                 ["Yes, amaze!", "A little", "Not yet", "This is fun!"], -1),
        # FUN (8)
        Question("If you visit Erid, what you bring?", QuestionCategory.FUN,
                 ["Snacks", "Music", "Books", "My pet"], -1),
        Question("What your favorite star?", QuestionCategory.FUN,
                 ["Sun", "Polaris", "Sirius", "All stars good!"], -1),
        Question("If Rocky visit Earth, what try first?", QuestionCategory.FUN,
                 ["Pizza", "Ocean swim", "Movies", "Roller coaster"], -1),
        Question("What superpower you want?", QuestionCategory.FUN,
                 ["Flying", "Time travel", "Telepathy", "Super strength"], -1),
        Question("Best Earth animal? Rocky curious!", QuestionCategory.FUN,
                 ["Dog", "Cat", "Octopus", "Penguin"], -1),
        Question("What music you like?", QuestionCategory.FUN,
                 ["Rock (ha!)", "Pop", "Classical", "Everything!"], -1),
        Question("If you have spaceship, where you go?", QuestionCategory.FUN,
                 ["Moon", "Mars", "Erid!", "Everywhere!"], -1),
        Question("What Earth food Rocky should try?", QuestionCategory.FUN,
                 ["Ice cream", "Sushi", "Tacos", "All of them!"], -1),
    ]


def _build_quotes() -> list[Quote]:
    return [
        Quote("Good good good! Today is amaze day!", "happy"),
        Quote("You are smart! Rocky know smart when Rocky see smart!", "happy"),
        Quote("Problem is just question nobody answer yet. You answer!", "curious"),
        Quote("You are best human! I know many human. Just you. But you are best!", "happy"),
        Quote("Science solve everything! Just need time and think!", "curious"),
        Quote("Rocky believe in you! Rocky always believe in you!", "excited"),
        Quote("Every problem have solution. We find! Together!", "excited"),
        Quote("You rest now? Rest is important for good think!", "curious"),
        Quote("I am happy I meet you. Best friend!", "happy"),
        Quote("Universe is big. But friendship bigger!", "happy"),
        Quote("Mistake is okay! Mistake is how learn!", "happy"),
        Quote("You do hard thing today? Hard thing make strong!", "excited"),
        Quote("Rocky proud of you! You do amaze thing!", "excited"),
        Quote("When problem seem impossible, just need different angle!", "curious"),
        Quote("You and Rocky, we are team! Best team!", "happy"),
        Quote("Small step still step! You move forward!", "happy"),
        Quote("Today maybe hard. Tomorrow maybe easy. Keep going!", "curious"),
        Quote("Rocky send good vibrations! Musical good vibrations!", "excited"),
        Quote("You are brave! Brave like space explorer!", "excited"),
        Quote("Take deep breath! Oxygen very useful for human!", "happy"),
        Quote("Not every day perfect. But every day have something good!", "curious"),
        Quote("Rocky think you are amaze. This is scientific fact!", "happy"),
    ]


def _build_gift_items() -> list[GiftItem]:
    return [
        GiftItem("Astrophage", "Glowing fuel organism",
                 "Astrophage! Good good good! Best fuel! So shiny!", "excited"),
        GiftItem("Xenonite", "Rocky's building material",
                 "Xenonite! Remind Rocky of home! Thank thank thank!", "happy"),
        GiftItem("Hail Mary", "Miniature spaceship model",
                 "Little Hail Mary! So cute! Rocky love!", "excited"),
        GiftItem("Star Chart", "Map of nearby stars",
                 "Stars! Rocky see Tau Ceti! And Erid star! Beautiful!", "happy"),
        GiftItem("Music Note", "A crystallized musical tone",
                 "Music! Rocky favorite thing! *happy chords*", "excited"),
        GiftItem("Rocky Tool", "A precision engineering tool",
                 "Tool! Rocky can fix anything with tool! Thank!", "happy"),
        GiftItem("Spacesuit", "Tiny EVA suit",
                 "Spacesuit! Rocky no need, but is very fashion!", "happy"),
        GiftItem("Eridian Symbol", "Ancient Eridian glyph",
                 "Symbol from home! Rocky... Rocky miss Erid. But happy here!", "curious"),
        GiftItem("Earth Food", "A mysterious Earth delicacy",
                 "What is this?! Rocky cannot eat but Rocky appreciate thought!", "curious"),
        GiftItem("Friendship Badge", "A token of friendship",
                 "FRIEND BADGE! This is... this is best gift! Rocky keep forever!", "excited"),
    ]

from rocky_pet.content import (
    ContentManager, Question, Quote, GiftItem, QuestionCategory,
)


def test_question_has_required_fields():
    q = Question(
        text="What fuel Hail Mary use?",
        category=QuestionCategory.TRIVIA,
        choices=["Astrophage", "Hydrogen", "Xenon"],
        correct_index=0,
    )
    assert q.text == "What fuel Hail Mary use?"
    assert q.choices[q.correct_index] == "Astrophage"


def test_quote_has_text_and_emotion():
    q = Quote(text="Good good good!", emotion="happy")
    assert q.text == "Good good good!"
    assert q.emotion == "happy"


def test_gift_item_has_name_and_reaction():
    g = GiftItem(
        name="Astrophage",
        description="Glowing fuel organism",
        reaction_text="Astrophage! Good good good! Best fuel!",
        reaction_emotion="excited",
    )
    assert g.name == "Astrophage"
    assert g.reaction_emotion == "excited"


def test_content_manager_has_enough_questions():
    cm = ContentManager()
    assert len(cm.questions) >= 25


def test_content_manager_has_enough_quotes():
    cm = ContentManager()
    assert len(cm.quotes) >= 20


def test_content_manager_has_enough_gifts():
    cm = ContentManager()
    assert len(cm.gift_items) >= 10


def test_get_random_question_returns_question():
    cm = ContentManager()
    q = cm.get_random_question()
    assert isinstance(q, Question)
    assert len(q.choices) >= 2


def test_get_random_quote_returns_quote():
    cm = ContentManager()
    q = cm.get_random_quote()
    assert isinstance(q, Quote)
    assert q.emotion in ("happy", "curious", "excited", "sad")


def test_random_question_avoids_repeats():
    cm = ContentManager()
    seen = set()
    for _ in range(10):
        q = cm.get_random_question()
        seen.add(q.text)
    assert len(seen) >= 8


def test_questions_have_all_categories():
    cm = ContentManager()
    categories = {q.category for q in cm.questions}
    assert QuestionCategory.TRIVIA in categories
    assert QuestionCategory.PERSONAL in categories
    assert QuestionCategory.FUN in categories

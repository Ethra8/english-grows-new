from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from placement.models import PlacementQuestion, TEST_VERSION, TOTAL_QUESTIONS


# Original English Grows assessment items. Each row:
# (number, sentence, (A, B, C, D), correct answer, area, language point, estimated target level)
# Item CEFR labels describe the language targeted, not empirically measured item difficulty.
QUESTIONS = [
    (1, "The office ______ at eight every weekday.", ("open", "opening", "opens", "to open"), "C", "grammar", "Present simple: third-person singular", "A1"),
    (2, "Had I known about the road closure, I ______ a different route.", ("would have taken", "had taken", "would take", "will take"), "A", "grammar", "Inverted third conditional", "C1"),
    (3, "There isn't ______ information in the brochure.", ("many", "several", "a few", "much"), "D", "grammar", "Quantifiers with uncountable nouns", "A2"),
    (4, "I ______ this software since January.", ("used", "have used", "am using", "use"), "B", "grammar", "Present perfect with since", "B1"),
    (5, "The customer ______ a formal complaint with the regulator.", ("committed", "performed", "filed", "attended"), "C", "vocabulary", "Collocation: file a complaint", "B2"),
    (6, "We ______ the museum last Saturday and bought tickets at the entrance.", ("visited", "have visited", "visit", "visiting"), "A", "grammar", "Past simple with a finished time expression", "A1"),
    (7, "The missing files are believed ______ during the move.", ("to lose", "to have lost", "to have been losing", "to have been lost"), "D", "grammar", "Passive reporting with perfect passive infinitive", "C1"),
    (8, "______ your colleagues work remotely?", ("Are", "Do", "Does", "Have"), "B", "grammar", "Present simple questions with do", "A1"),
    (9, "If the train is delayed, we ______ a taxi.", ("will take", "took", "had taken", "would have taken"), "A", "grammar", "First conditional", "A2"),
    (10, "What surprised me most ______ how quickly the team adapted.", ("were", "it was", "was", "being"), "C", "grammar", "Pseudo-cleft sentences", "C1"),
    (11, "The instructions were so ______ that three people followed them in three different ways.", ("clear", "consistent", "explicit", "ambiguous"), "D", "vocabulary", "Advanced vocabulary: ambiguous", "C2"),
    (12, "This is Marta's jacket. It belongs to ______.", ("she", "her", "hers", "herself"), "B", "grammar", "Object pronouns after prepositions", "A1"),
    (13, "He told me he ______ the report the day before.", ("had finished", "has finished", "will finish", "is finishing"), "A", "grammar", "Reported speech: past perfect backshift", "B2"),
    (14, "Of the three routes, this one is ______.", ("shorter", "shortest", "the shortest", "as short"), "C", "grammar", "Superlative adjectives", "A2"),
    (15, "The new safety measures are intended to ______ the risk of accidents.", ("provoke", "mitigate", "duplicate", "disregard"), "B", "vocabulary", "Advanced vocabulary: mitigate risk", "C1"),
    (16, "She suggested ______ the meeting until Friday.", ("postpone", "to postpone", "postponed", "postponing"), "D", "grammar", "Verb patterns: suggest + -ing", "B1"),
    (17, "You're welcome to bring your own laptop, but you ______; we'll provide one if needed.", ("don't have to", "mustn't", "can't", "shouldn't"), "A", "grammar", "Modals: absence of obligation versus prohibition", "B1"),
    (18, "The consultant, ______ report we discussed, is joining us tomorrow.", ("which", "who", "whose", "whom"), "C", "grammar", "Possessive relative pronoun whose", "B2"),
    (19, "Only after the audit ______ the error.", ("we discovered", "did we discover", "we had discovered", "we did discover"), "B", "grammar", "Inversion after only + adverbial", "C1"),
    (20, "The seminar starts precisely ______ 10:30.", ("in", "on", "by", "at"), "D", "grammar", "Prepositions of clock time", "A1"),
    (21, "I ______ cycle to work, but now I take the tram.", ("used to", "am used to", "use to", "was used to"), "A", "grammar", "Past habits: used to", "B1"),
    (22, "The negotiations ______ when neither side would compromise.", ("broke into", "broke away", "broke down", "broke out"), "C", "vocabulary", "Phrasal verb: negotiations break down", "B2"),
    (23, "Could you explain the procedure ______? I still don't understand it.", ("most clearly", "more clearly", "more clear", "much clearly"), "B", "grammar", "Comparative adverbs", "A2"),
    (24, "The chair recommended that the proposal ______ revised before publication.", ("being", "been", "to be", "be"), "D", "grammar", "Mandative subjunctive", "C1"),
    (25, "They ______ the network since 9 a.m., and it still isn't working.", ("have repaired", "repaired", "have been repairing", "had repaired"), "C", "grammar", "Present perfect continuous for ongoing activity", "B2"),
    (26, "Please show your boarding pass at the ______ immediately before boarding the aircraft.", ("gate", "platform", "checkout", "baggage claim"), "A", "vocabulary", "Travel vocabulary: airport gate", "B1"),
    (27, "If we had checked the address, the parcel ______ to the wrong office.", ("wouldn't go", "wouldn't have gone", "won't go", "hadn't gone"), "B", "grammar", "Third conditional", "B2"),
    (28, "She takes ______ her grandfather; they even laugh the same way.", ("over", "up", "off", "after"), "D", "vocabulary", "Phrasal verb: take after", "B2"),
    (29, "No sooner had the presentation begun ______ the projector failed.", ("than", "when", "that", "then"), "A", "grammar", "Inversion: no sooner ... than", "C1"),
    (30, "How ______ chairs do we need?", ("much", "a little", "many", "any"), "C", "grammar", "Quantifiers with countable nouns", "A1"),
    (31, "We're having the air conditioning ______ next week.", ("repair", "repaired", "repairing", "to repair"), "B", "grammar", "Causative: have something done", "B2"),
    (32, "I ______ my dentist at four tomorrow; it's already booked.", ("saw", "have seen", "seeing", "am seeing"), "D", "grammar", "Present continuous for future arrangements", "A2"),
    (33, "The app ______ you recommended is very useful.", ("where", "whose", "that", "who"), "C", "grammar", "Defining relative clauses", "B1"),
    (34, "The investigation uncovered further safety failures, ______ the urgent need for stricter checks.", ("underscoring", "overlooking", "delaying", "concealing"), "A", "vocabulary", "Advanced vocabulary: underscore a need", "C1"),
    (35, "There ______ a few cookies left in the tin.", ("is", "are", "has", "be"), "B", "grammar", "There is/are: subject–verb agreement", "A1"),
    (36, "I wish I ______ more confident when speaking in public.", ("am", "will be", "have been", "were"), "D", "grammar", "Wish + past form for unreal present situations", "B2"),
    (37, "This isn't my notebook; ______ is blue.", ("mine", "my", "me", "myself"), "A", "grammar", "Possessive pronouns", "A1"),
    (38, "By the time we arrived, the film ______.", ("is starting", "has started", "had started", "will start"), "C", "grammar", "Past perfect: sequencing past events", "B1"),
    (39, "If I ______ your advice last year, I wouldn't be in this situation now.", ("took", "had taken", "would take", "have taken"), "B", "grammar", "Mixed conditional: past condition, present result", "B2"),
    (40, "The hotel refunded our payment because the room was ______.", ("bright", "comfortable", "spacious", "unavailable"), "D", "vocabulary", "Accommodation vocabulary: unavailable", "B2"),
    (41, "The director refused to ______ pressure from investors.", ("get over", "give in to", "put up", "break down"), "B", "vocabulary", "Phrasal verb: give in to pressure", "B1"),
    (42, "Each of the computers ______ a password.", ("requires", "require", "requiring", "have required"), "A", "grammar", "Subject–verb agreement with each", "A2"),
    (43, "The latest update allows users ______ their preferences.", ("customising", "customise", "to customise", "customised"), "C", "grammar", "Allow + object + to-infinitive", "B1"),
    (44, "She is unlikely ______ the offer unless conditions improve.", ("accept", "accepting", "accepted", "to accept"), "D", "grammar", "Adjective + to-infinitive", "B2"),
    (45, "Not only ______ the proposal, but she also secured funding.", ("did she draft", "she drafted", "she did draft", "drafted she"), "A", "grammar", "Inversion after not only", "C1"),
    (46, "The instructions are ______ complicated for beginners to follow.", ("such", "too", "enough", "many"), "B", "grammar", "Too + adjective + to-infinitive", "A2"),
    (47, "The documentary was so ______ that I watched it twice.", ("fascinate", "fascination", "fascinating", "fascinated"), "C", "vocabulary", "Participial adjectives: -ing versus -ed", "B2"),
    (48, "The evidence was not sufficient to ______ the claim.", ("estimate", "anticipate", "replicate", "substantiate"), "D", "vocabulary", "Advanced vocabulary: substantiate a claim", "C1"),
    (49, "We'd better ______ now if we want to catch the last bus.", ("leave", "to leave", "leaving", "left"), "A", "grammar", "Had better + bare infinitive", "B1"),
    (50, "It's high time the company ______ its outdated procedures.", ("reviews", "reviewed", "has reviewed", "reviewing"), "B", "grammar", "It's high time + past form", "C1"),
]


class Command(BaseCommand):
    help = "Safely seed the 50 original English Grows four-option placement questions."

    @transaction.atomic
    def handle(self, *args, **options):
        numbers = [row[0] for row in QUESTIONS]
        levels = Counter(row[6] for row in QUESTIONS)
        answers = Counter(row[3] for row in QUESTIONS)
        expected_levels = {"A1": 8, "A2": 7, "B1": 10, "B2": 13, "C1": 11, "C2": 1}
        if numbers != list(range(1, TOTAL_QUESTIONS + 1)) or levels != expected_levels:
            raise CommandError("Question numbers or CEFR target distribution are incorrect.")
        if set(answers) != set("ABCD") or min(answers.values()) < 10 or any(
            len(row[2]) != 4 or len(set(row[2])) != 4 or row[3] not in "ABCD" for row in QUESTIONS
        ):
            raise CommandError("The four-option answer key is invalid or unbalanced.")

        created = 0
        for number, text, choices, key, area, language_point, level in QUESTIONS:
            data = dict(text=text, option_a=choices[0], option_b=choices[1], option_c=choices[2],
                        option_d=choices[3], correct_answer=key, area=area, language_point=language_point,
                        target_level=level, is_active=True)
            question, was_created = PlacementQuestion.objects.get_or_create(
                version=TEST_VERSION, number=number, defaults=data
            )
            if not was_created and any(getattr(question, field) != value for field, value in data.items()):
                raise CommandError(f"Question {number} in version {TEST_VERSION} differs from the seed. "
                                   "Existing questions have NOT been overwritten.")
            created += int(was_created)

        count = PlacementQuestion.objects.filter(version=TEST_VERSION, is_active=True).count()
        if count != TOTAL_QUESTIONS:
            raise CommandError(f"Expected {TOTAL_QUESTIONS} active questions, found {count}.")
        self.stdout.write(self.style.SUCCESS(
            f"Placement v{TEST_VERSION}: {count} active questions; {created} created. "
            f"Target levels: {dict(levels)}. Answer key: {dict(answers)}."
        ))

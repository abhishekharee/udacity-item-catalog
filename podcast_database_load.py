# coding: utf-8

# Import relevant sqlalchemy packages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import database setup file
from podcast_database_setup import Podcast, Episode, Base

# Create the SQLite engine
engine = create_engine('sqlite:///podcastepisodes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
# Initialise a DBSession.
# Note: A DBSession() instance establishes all conversations with the database
# and represents a staging zone for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create podcast objects
podcast1 = Podcast(
    podcast_name="Freakonomics",
    podcast_description=(
        "Freakonomics Radio is an American public radio program which "
        "discusses socioeconomic issues for a general audience. The show "
        "is a spin-off of the 2005 book Freakonomics. Journalist Stephen "
        "Dubner hosts the show, with economist Steven Levitt as a regular "
        "guest."))
podcast2 = Podcast(
    podcast_name="TED Radio Hour",
    podcast_description=(
        "A journey through fascinating ideas, astonishing inventions, and new "
        "ways to think and create. Based on riveting TEDTalks from the "
        "world\'s most remarkable minds."))
podcast3 = Podcast(
    podcast_name="How I Built This",
    podcast_description=(
        "How I Built This is an American podcast about innovators, "
        "entrepreneurs, idealists, and the stories behind the movements they "
        "built, produced by NPR."))

# Add podcasts objects to Podcast database
session.add(podcast1)
session.add(podcast2)
session.add(podcast3)
session.commit()

# Create and add episode objects ...
episode1 = Episode(
    episode_name='Not Just Another Labor Force',
    episode_description=(
        'If you think talent and hard work give top athletes all the leverage '
        'to succeed,think again. As employees in the Sports-Industrial '
        'Complex, they\'ve got a tight earnings window, a high injury rate, '
        'little choice in where they work - and a very early forced '
        'retirement. (Ep. 6 of The Hidden Side of Sports series.)'),
    episode_date='2019-01-30',
    episode_listened='',
    podcast=podcast1)
session.add(episode1)
episode2 = Episode(
    episode_name='Extra: Domonique Foxworth Full Interview',
    episode_description=(
        'Stephen Dubner\'s conversation with the former N.F.L. player, union '
        'official, and all-around sports thinker, recorded for our Hidden '
        'Side of Sports. series.'),
    episode_date='2019-02-02',
    episode_listened='',
    podcast=podcast1)
session.add(episode2)
episode3 = Episode(
    episode_name=(
        'This Economist Predicted the Last Crisis. What\'s the Next One?'),
    episode_description=(
        'In 2005, Raghuram Rajan said the financial system was at risk of a '
        'catastrophic meltdown. After stints at the I.M.F. and India\'s '
        'central bank, he sees another potential crisis - and he offers a '
        'solution. Is it stronger governments? Freer markets? Rajan\'s '
        'answer: neither.'),
    episode_date='2019-02-06',
    episode_listened='Listened',
    podcast=podcast1)
session.add(episode3)
episode4 = Episode(
    episode_name='The Future of Meat',
    episode_description=(
        'Global demand for beef, chicken, and pork continues to rise. So do '
        'concerns about environmental and other costs. Will reconciling '
        'these two forces be possible - or, even better, Impossible?'),
    episode_date='2019-02-13',
    episode_listened='Listened',
    podcast=podcast1)
session.add(episode4)
episode5 = Episode(
    episode_name='Where Do Good Ideas Come From?',
    episode_description=(
        'Whether you\'re mapping the universe, hosting a late-night talk '
        'show, or running a meeting, there are a lot of ways to up your idea '
        'game. Plus: the truth about brainstorming. (Ep. 3 of the How to Be '
        'Creative series.)'),
    episode_date='2019-02-20',
    episode_listened='Listened',
    podcast=podcast1)
session.add(episode5)
episode6 = Episode(
    episode_name='A Good Idea Is Not Good Enough',
    episode_description=(
        'Whether you\'re building a business or a cathedral, execution is '
        'everything. We ask artists, scientists, and inventors how they '
        'turned ideas into reality. And we find out why it\'s so hard for a '
        'group to get things done - and what you can do about it. (Ep. 4 of '
        'the How to Be Creative series.)'),
    episode_date='2019-02-27',
    episode_listened='Listened',
    podcast=podcast1)
episode21 = Episode(
    episode_name='The Right To Speak',
    episode_description=(
        'Should all speech, even the most offensive, be allowed on college '
        'campuses? And is hearing from those we deeply disagree with ... '
        'worth it? This hour, TED speakers explore the debate over free '
        'speech.'),
    episode_date='2018-07-27',
    episode_listened='',
    podcast=podcast2)
session.add(episode21)
episode22 = Episode(
    episode_name='The Story Behind The Numbers',
    episode_description=(
        'Is life today better than ever before? Does the data bear that out? '
        'This hour, TED speakers explore the stories we tell with numbers - '
        'and whether those stories portray the full picture.'),
    episode_date='2018-08-17',
    episode_listened='Listened',
    podcast=podcast2)
session.add(episode22)
episode23 = Episode(
    episode_name='Dying Well',
    episode_description=(
        'Is there a way to talk about death candidly, without fear ... and '
        'even with humor? How can we best prepare for it with those we love? '
        'This hour, TED speakers explore the beauty of life ... and death.'),
    episode_date='2018-09-07',
    episode_listened='Listened',
    podcast=podcast2)
session.add(episode23)
episode24 = Episode(
    episode_name='Building Humane Cities',
    episode_description=(
        'Cities are symbols of hope and opportunity. But today, overcrowding '
        'and gentrification are hurting their most vulnerable residents. '
        'This hour, TED speakers explore how we can build more humane '
        'cities.'),
    episode_date='2018-09-28',
    episode_listened='',
    podcast=podcast2)
session.add(episode24)
episode25 = Episode(
    episode_name='Hacking The Law',
    episode_description=(
        'We have a vision of justice as blind, impartial, and fair - but in '
        'reality, the law often fails those who need it most. This hour, TED '
        'speakers explore radical ways to change the legal system.'),
    episode_date='2018-10-12',
    episode_listened='',
    podcast=podcast2)
session.add(episode25)
episode26 = Episode(
    episode_name='Unintended Consequences',
    episode_description=(
        'Human innovation has transformed the way we live, often for the '
        'better. But as our technologies grow more powerful, so do their '
        'consequences. This hour, TED speakers explore technology\'s dark '
        'side.'),
    episode_date='2018-11-02',
    episode_listened='Listened',
    podcast=podcast2)
session.add(episode26)
episode27 = Episode(
    episode_name='Where Joy Hides',
    episode_description=(
        'When we focus so much on achievement and success, it\'s easy to '
        'lose sight of joy. This hour, TED speakers search for joy in '
        'unexpected places, and explain why it\'s crucial to a fulfilling '
        'life.'),
    episode_date='2018-11-16',
    episode_listened='Listened',
    podcast=podcast2)
session.add(episode27)
episode40 = Episode(
    episode_name='Moving Forward',
    episode_description=(
        'When the life you\'ve built slips out of your grasp, you\'re often '
        'told it\'s best to move on. But is that true? Instead of forgetting '
        'the past, TED speakers describe how we can move forward with it.'),
    episode_date='2019-06-21',
    episode_listened='',
    podcast=podcast2)
session.add(episode40)
episode41 = Episode(
    episode_name='Live Episode! Dollar Shave Club: Michael Dubin',
    episode_description=(
        'At the end of 2010, Michael Dubin was working in marketing when he '
        'met a guy named Mark Levine at a holiday party. Mark was looking '
        'for ideas to get rid of a massive pile of razors he had sitting in '
        'a California warehouse. Michael\'s spontaneous idea for an internet '
        'razor subscription service grew into Dollar Shave Club, and his '
        'background in improv helped him make a viral video to generate buzz '
        'for the new brand. Just five years after launch, Unilever acquired '
        'Dollar Shave Club for a reported $1 billion. Recorded live in Los '
        'Angeles.'),
    episode_date='2018-12-17',
    episode_listened='Listened',
    podcast=podcast3)
session.add(episode41)
episode42 = Episode(
    episode_name='Lisa Price Of Carol\'s Daughter At The HIBT Summit',
    episode_description=(
        'It\'s our final episode in our series from this year\'s How I '
        'Built This Summit! Today, we\'re featuring Lisa Price of the '
        'beauty brand Carol\'s Daughter. When Lisa sat down with Guy Raz '
        'in October, she described how her business expanded well beyond '
        'her Brooklyn kitchen. As it grew, she decided not to sit at the '
        'head of the table, and deferred to the experts. She later came '
        'to regret that.'),
    episode_date='2018-12-20',
    episode_listened='Listened',
    podcast=podcast3)
session.add(episode42)
episode43 = Episode(
    episode_name='SoulCycle: Julie Rice & Elizabeth Cutler',
    episode_description=(
        'Before Elizabeth Cutler and Julie Rice met, they shared a common '
        'belief: New York City gyms didn\'t have the kind of exercise '
        'classes they craved, and each of them wanted to change that. A '
        'fitness instructor introduced them over lunch in 2005, and before '
        'the meal was done they were set on opening a stationary bike '
        'studio, with a chic and aspirational vibe. A few months later, the '
        'first SoulCycle opened in upper Manhattan. Today, SoulCycle has '
        'cultivated a near-tribal devotion among its clients, with studios '
        'across the United States and Canada. PLUS for our postscript How '
        'You Built That, how kid-preneur Gabrielle Goodwin and her mom '
        'Rozalynn invented a double-face double snap barrette that doesn\'t '
        'slip out of little girls\' hair, no matter how much they play '
        'around.'),
    episode_date='2019-01-07',
    episode_listened='Listened',
    podcast=podcast3)
session.add(episode43)
episode44 = Episode(
    episode_name='Bonobos: Andy Dunn',
    episode_description=(
        'When Andy Dunn was in business school, his housemate Brian Spaly '
        'created a new type of men\'s pants: stylish, tailored trousers that '
        'fit well in both the hips and thighs. Together, they started the '
        'men\'s clothing company Bonobos, which became an instant hit due to '
        'the pants\' signature flair and innovative e-commerce experience. '
        'But within a few years, Andy hit challenging roadblocks, including '
        'a struggle with depression and a falling-out with his co-founder '
        'and friend. Despite many moments of crisis, Andy steered Bonobos to '
        'massive success, and in 2017, it was acquired by Walmart for a '
        'reported $310 million. PLUS for our postscript How You Built That, '
        'how Amy and Brady King created an easy-to-assemble portable shelter '
        'meant to provide natural disaster relief and help house people '
        'experiencing homelessness.'),
    episode_date='2019-01-21',
    episode_listened='Listened',
    podcast=podcast3)
session.add(episode44)
episode45 = Episode(
    episode_name='Canva: Melanie Perkins',
    episode_description=(
        'When she was just 19 years old, Melanie Perkins dreamt of '
        'transforming the graphic design and publishing industries. But she '
        'started small, launching a site to make yearbook design simpler and '
        'more collaborative. Her success with that first venture - and an '
        'unexpected meeting with a VC investor - eventually landed her the '
        'backing to pursue her original idea, and the chance to take on '
        'software industry titans like Adobe and Microsoft. Today, '
        'Melanie\'s online design platform Canva is valued at over $1 '
        'billion, joining the list of Australia\'s unicorn companies. '
        'PLUS for our postscript How You Built That, how Tristan Corriveau '
        'collected used bars of soap from a hotel and recycled them into '
        'liquid soap with The One Gallon Soap Company.'),
    episode_date='2019-01-28',
    episode_listened='Listened',
    podcast=podcast3)
session.add(episode45)
# ... then commit those episodes to the database
session.commit()

# Check whether the load worked, by first storing the database contents in
# variables ...
podcasts = session.query(Podcast).all()
episodes = session.query(Episode).all()

# ... and printing the Podcast database ...
print "You have loaded the following Podcasts:"
for i in podcasts:
    print "  ", i.podcast_id, "|", i.podcast_name, "|", i.podcast_description
# ...followed by the Episode database.
print "You have loaded the following Episodes:"
for i in episodes:
    print (
        "  ", i.episode_id, "|", i.episode_name, "|", i.episode_description,
        "|", i.episode_date,  "|", i.episode_listened, "|", i.podcast_id)

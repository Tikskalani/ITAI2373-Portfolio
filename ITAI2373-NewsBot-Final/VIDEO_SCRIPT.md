# NewsBot 2.0 — Final Video Presentation Script (10 to 15 minutes)

Presenter: Trilok Kalani | Course: ITAI 2373 | Group: SOLO
Upload name: FP_VideoPresentation_TrilokKalani_SOLO_ITAI2373.mp4

Record at 720p or higher, zoom so code and charts are readable, and have the app
and notebooks already run so nothing is loading on camera. Speaking at about 140
words per minute lands this near 12 minutes. The [ON SCREEN] cues tell you what to
show. The slide deck FP_Presentation_TrilokKalani_SOLO_ITAI2373.pptx follows these
segments one to one, so you can present straight from it.

## Segment 1 — Intro (0:00 to 1:00)
[ON SCREEN: Slide 1, then the GitHub repo with the ITAI2373-NewsBot-Final folder open.]

"Hi, I am Trilok Kalani, and this is my ITAI 2373 final project, NewsBot Intelligence
System 2.0. I did this as an individual project. For the midterm I built an
end-to-end news analysis pipeline in a single notebook. For the final I rebuilt that
into a real, modular system and added four advanced capabilities on top: deeper
content analysis, language understanding and generation, multilingual analysis, and
a conversational interface. I also built a web app so you can use all of it in a
browser. Everything lives in the ITAI2373-NewsBot-Final folder in my portfolio repo."

## Segment 2 — From midterm to final (1:00 to 2:00)
[ON SCREEN: Slide 3. Show the src/ folder tree.]

"The biggest change is structure. The midterm was one long notebook. The final is a
Python package. Every capability is its own small class with one job, under src, so
I can test it alone and reuse it from the notebooks, the tests, and the web app. That
refactor is what made the four new modules possible, because once the parts had clean
inputs and outputs I could wire them together instead of copying code around."

## Segment 3 — Architecture (2:00 to 3:00)
[ON SCREEN: Slide 4, the architecture diagram.]

"Here is the architecture. Raw article text comes into a thin facade called NewsBot,
which handles classification, sentiment, and entities. On top of that sit the four
modules. The design rule is parse and vectorize once, then reuse. The classifier owns
the TF-IDF vectorizer for the five known categories, while search and topic modeling
keep their own vectorizers because they are tuned for different goals. On the very top
is the Flask web app, which is just a presentation layer over these same components."

## Segment 4 — Module A, Content Analysis (3:00 to 4:30)
[ON SCREEN: Slide 5, then run a classification in the app or notebook 02.]

"Module A is advanced content analysis. Classification returns the category, a
confidence score, the runner-up, and how many words it actually recognized. The most
important behavior is the uncertainty guard: if the input has almost no known words,
or the top probability is too low, it returns uncertain instead of guessing. In the
midterm short off-topic text was getting labeled sport, and this is the fix. It also
does sentiment with an emotion label, named entity recognition with a domain rule
layer, and topic modeling with both LDA and NMF."

## Segment 5 — Module B, Language Understanding and Generation (4:30 to 6:00)
[ON SCREEN: Slide 6, then show a summary and a semantic search result.]

"Module B is language understanding and generation. Summarization is extractive by
default: it scores each sentence by TF-IDF salience and returns the top ones, and
there is an optional transformer summarizer that only loads if you ask for it.
Semantic search ranks the whole corpus by cosine similarity to a query, so I can
search by meaning, not just keywords, and there is an optional dense embedding backend.
There is also content enhancement and WordNet query expansion. The theme here is a
light default that runs anywhere, with a heavier upgrade one flag away."

## Segment 6 — Module C, Multilingual (6:00 to 7:00)
[ON SCREEN: Slide 7, then run cross-lingual analyze on a Spanish or French sentence.]

"Module C is multilingual intelligence. It detects the language, translates the text
to English, and then runs the exact same pipeline I already trust. So a Spanish or
French article gets the same classification, sentiment, and entities as an English
one. I chose to translate into English rather than pretend my English-trained models
understand every language directly, which is the honest way to do it with these tools."

## Segment 7 — Module D, Conversational (7:00 to 8:15)
[ON SCREEN: Slide 8, then type a few questions in the Ask box.]

"Module D is the conversational interface, and it is the piece I am most proud of
because it ties everything together. An intent classifier reads a plain question like
what is the sentiment, or who is mentioned, and a query processor routes it to the
right component and formats the answer. This only works because each capability is a
clean class, so the router can just call the right one."

## Segment 8 — Web app demo (8:15 to 9:45)
[ON SCREEN: Slide 9, then the running web dashboard. Analyze an article, ask a
question, run a search.]

"Here is the web app, which is the bonus frontend. The dashboard has three panels.
I paste an article and get the category, confidence, sentiment, entities, and a
summary. I ask a question about that article in plain English and get an answer. And
I search for related coverage by meaning. This is the same code from the modules,
just exposed in a browser so a non-technical user can use it."

## Segment 9 — Results and technical depth (9:45 to 11:00)
[ON SCREEN: Slide 10 and 12, the demo table and the accuracy table.]

"On results: the classification foundation reaches about 97.5 percent test accuracy
on the five BBC categories, with Linear SVM best and all four models above 94 percent.
On four fresh June 2026 articles the system labels tech, business, sport, and politics
all correctly with high confidence, and it returns uncertain on short off-topic input.
The LDA topics also rediscover the five categories with no labels at all, which is a
nice check that the unsupervised side is finding real structure."

## Segment 10 — Business value (11:00 to 12:00)
[ON SCREEN: Slide 13.]

"In the real world this maps onto media intelligence. A communications team can point
NewsBot at a feed, automatically flag every article that mentions them, and get warned
when the tone turns negative. The entity extraction turns a pile of articles into a
searchable index of the people and companies in the news, and the conversational layer
means someone can just ask questions instead of learning a query language."

## Segment 11 — Limitations and future work (12:00 to 13:00)
[ON SCREEN: Slide 14 and 15.]

"I tried to be honest about the limits. The model is trained on older BBC news, so it
is weaker on messy present-day text, and the lexicon sentiment misreads financial
language and can score a profit warning as positive. I would not ship that piece
without replacing it with a finance-tuned model like FinBERT. After that I would
fine-tune the entity recognizer on recent news, add topic modeling over time, and
deploy the app to a public URL. Thanks for watching."

## Recording checklist
- Tool: OBS, Zoom recording, or your built-in recorder. Headset mic if you have one.
- Have the web app running and the notebooks already executed before you hit record.
- Keep it between 10 and 15 minutes.
- Upload to YouTube or Vimeo as Unlisted, or export MP4. Test the link privately.
- Name it FP_VideoPresentation_TrilokKalani_SOLO_ITAI2373 and put the link in the README.

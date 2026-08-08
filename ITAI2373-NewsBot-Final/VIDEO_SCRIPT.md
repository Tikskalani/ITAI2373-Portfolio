# NewsBot 2.0 — Final Video Presentation Script (record-ready)

Presenter: Trilok Kalani | Course: ITAI 2373 | Group: SOLO
Upload name: FP_VideoPresentation_TrilokKalani_SOLO_ITAI2373.mp4
Target length: 10 to 15 minutes (this reads to about 12 at a normal pace).

## Before you hit record (2 minute setup)
Open two things and nothing else:
1. The slide deck: reports/FP_Presentation_TrilokKalani_SOLO_ITAI2373.pptx (put it in Slide Show mode).
2. The live demo in a browser tab: https://tikskalani.github.io/ITAI2373-Portfolio/
Optional third tab: the GitHub repo https://github.com/Tikskalani/ITAI2373-Portfolio

Use any screen recorder (the deck's Slide Show > Record, or OBS, or Zoom). Share your
screen, use a headset mic if you have one, record at 720p or higher. Just read the lines
below in a normal voice. The [SHOW] cues tell you what to have on screen. You do not need
to run any code, the demo is the live website.

---

## 1. Intro  (about 0:00 to 1:00)
[SHOW: Slide 1, the title slide.]

"Hi, I am Trilok Kalani, and this is my ITAI 2373 final project, NewsBot Intelligence
System 2.0. I completed it as an individual project. For the midterm I built an
end-to-end news analysis pipeline in a single notebook. For the final I rebuilt that into
a real, modular system and added four advanced capabilities on top: deeper content
analysis, language understanding and generation, multilingual analysis, and a
conversational interface. I also built a web front end so you can use all of it in a
browser, which I will demo live in a minute."

## 2. From midterm to final  (about 1:00 to 2:00)
[SHOW: Slide 3.]

"The biggest change is structure. The midterm was one long notebook. The final is a Python
package where every capability is its own small class under a source folder, so I can test
each part on its own and reuse it from the notebooks, the tests, and the web app. That
refactor is what made the four new modules possible, because once the parts had clean
inputs and outputs I could wire them together instead of copying code around."

## 3. Architecture  (about 2:00 to 3:00)
[SHOW: Slide 4, the architecture diagram.]

"Here is the architecture. Raw article text comes into a thin facade called NewsBot, which
handles classification, sentiment, and entities. On top of that sit the four modules. The
design rule is parse and vectorize once, then reuse. The classifier owns the TF-IDF
vectorizer for the five known categories, while search and topic modeling keep their own
vectorizers, tuned for different goals. On top of all of it is the web app, which is just a
presentation layer over these same components."

## 4. The four modules  (about 3:00 to 5:30)
[SHOW: Slides 5, 6, 7, 8 in turn.]

"Module A is advanced content analysis. Classification returns the category, a confidence
score, the runner up, and how many words it actually recognized. The key behavior is the
uncertainty guard: if the input is empty or out of scope, it returns uncertain instead of
guessing. It also does sentiment with an emotion label, named entity recognition, and topic
modeling with both LDA and NMF.

Module B is language understanding and generation. Summarization is extractive by default
and ranks sentences by importance, with an optional transformer summarizer behind a flag.
Semantic search ranks the whole corpus by meaning, not just keywords. There is also content
enhancement and query expansion.

Module C is multilingual. It detects the language, translates the text to English, and then
runs the same pipeline I already trust, so a Spanish or French article gets the same
treatment as an English one.

Module D is the conversational interface, and it is the piece I am most proud of. An intent
classifier reads a plain question like what is the sentiment, and a query processor routes it
to the right module and formats the answer. It only works because each capability is a clean
class the router can call."

## 5. Live demo  (about 5:30 to 8:30)
[SHOW: switch to the browser tab, https://tikskalani.github.io/ITAI2373-Portfolio/ ]

"Now let me show it working. This is the live web app for NewsBot 2.0, and everything you
see here is the model's real output.

[Click the Technology sample, then Business, Sport, Politics as you talk.]
In the Analyze panel I pick a sample article and it returns the category with a confidence
score, the sentiment and dominant emotion, the entities it found, the key terms, and a
short summary. Technology comes back as tech, the markets story as business, the World Cup
story as sport at 96 percent, and the UK politics story as politics at 97 percent, all
correct.

[Type a question in the Ask box, for example: what is the sentiment?]
In the Ask panel I can ask a plain question about the selected article and it routes to the
right answer, here the sentiment and emotion.

[Click one of the search buttons, for example election government policy.]
In the Find similar panel I search the corpus by meaning and it returns the closest
articles ranked by similarity, and you can see they are all on topic.

[Scroll to the Topics section.]
And these are the topics the model discovered with LDA, with no labels at all. They line up
cleanly with the five news beats, which is a good sign the unsupervised side is finding real
structure."

## 6. Results and technical depth  (about 8:30 to 10:00)
[SHOW: Slides 10 and 12, the demo table and the accuracy table.]

"On results, the classification foundation reaches about 97.5 percent test accuracy on the
five BBC categories, with Linear SVM best and all four models above 94 percent. The only
real confusions are a few politics and business articles that share vocabulary like tax and
economy. And as I showed, on fresh articles it classifies correctly and returns uncertain on
short off-topic input instead of forcing a label."

## 7. Business value  (about 10:00 to 11:00)
[SHOW: Slide 13.]

"In the real world this maps onto media intelligence. A communications team can point
NewsBot at a feed, automatically flag every article that mentions them, and get warned when
the tone turns negative. The entity extraction turns a pile of articles into a searchable
index of the people and companies in the news, and the conversational layer means someone
can just ask questions instead of learning a query language."

## 8. Limitations and future work  (about 11:00 to 12:00)
[SHOW: Slides 14 and 15.]

"I tried to be honest about the limits. The model is trained on older BBC news, so it is
weaker on messy present-day text, and the lexicon sentiment misreads financial language and
can score a profit warning as positive. I would replace that with a finance-tuned model like
FinBERT. After that I would fine-tune the entity recognizer on recent news, add topic
modeling over time, and expand the deployment. Everything is on my GitHub and there is a live
demo link in the README. Thanks for watching."

---

## After recording
- Export as MP4, or upload to YouTube or Vimeo set to Unlisted.
- Name it FP_VideoPresentation_TrilokKalani_SOLO_ITAI2373.
- Put the link in the README next to the live demo link.
- Submit on Canvas with the GitHub link and the three PDFs.

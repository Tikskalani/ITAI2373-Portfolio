# NewsBot Intelligence System, Video Script (5 to 7 minutes)

**Presenter:** Trilok Kalani  |  **Course:** ITAI 2373  |  **Upload name:** MT_Video_Group_SOLO_Trilok_Kalani_ITAI2373

Read the lines in plain voice. The **[ON SCREEN]** cues tell you what to have visible. Speaking pace of about 140 words per minute lands this around 6 minutes.

---

## Segment 1 — Introduction and overview (about 0:00 to 1:00)
**[ON SCREEN: the GitHub repo page, then the ITAI2373-NewsBot-Midterm folder open showing the notebook, README, dataset, and visualizations.]**

"Hi, my name is Trilok Kalani, and this is my ITAI 2373 midterm project, the NewsBot Intelligence System. I completed this as an individual project.

NewsBot is an end-to-end natural language processing pipeline. You give it a news article, and it does five things at once: it predicts the article's category, it pulls out the named entities like people, organizations, and places, it scores the sentiment and emotional tone, and it surfaces the key terms and writing patterns that define each kind of news. It is the same kind of system that powers Google News categorization and the media-monitoring tools that PR and finance teams use.

Here is the repository. Everything lives in the folder named ITAI2373-NewsBot-Midterm: the Jupyter notebook with all eight modules, the README, the BBC dataset, and a visualizations folder with the result charts."

## Segment 2 — Live demonstration with new articles (about 1:00 to 3:00)
**[ON SCREEN: scroll to Section 11, the integration layer. Run the cell, or open the Gradio dashboard in Section 13.4.]**

"Now let me show it working on brand-new articles that are not in the training data. These are five real news stories from June 2026, one per category.

**[Point at each result as you read it.]**

The first is a technology story about an AI software launch. NewsBot classifies it as tech with 90 percent confidence, and you can see it pulled out the key terms and entities.

The second is a markets story about the Nasdaq and Apple. It returns business at 85 percent.

The third is about the World Cup and the Stanley Cup. It returns sport at 96 percent.

The fourth is a UK politics story about a prime minister resigning. It returns politics at 97 percent.

The fifth is an entertainment story about new film releases. It returns entertainment at 80 percent.

So all five new articles are classified correctly, and for each one it also gives the sentiment, the dominant emotion, and the entities it found.

**[Point at the last item.]**

The last input is deliberately tricky: a short, off-topic line. Instead of guessing, the system returns *uncertain*, because it only recognized a couple of words. I built that in on purpose, and I will come back to why in a moment."

## Segment 3 — Technical deep dive (about 3:00 to 5:00)
**[ON SCREEN: scroll to the classifier comparison table and confusion matrix in Section 9.]**

"On the technical side, I compared four classifiers with five-fold cross-validation and a held-out test set. Linear SVM was the best at 97.5 percent test accuracy, with Logistic Regression close behind, and all four models above 94 percent. The confusion matrix shows the only real mistakes are a few politics and business articles that share vocabulary like tax and economy.

**[ON SCREEN: scroll to the POS heatmap (Section 6) and the entity-type mix heatmap (Section 10).]**

Two findings stood out. First, the writing style itself signals the category: sport and entertainment are full of proper nouns because they are about named people and teams, while business and tech are the most noun-dense. Second, the entity mix is its own signal: business is dominated by organizations, while sport, politics, and entertainment are dominated by people.

**[ON SCREEN: scroll to the research extension, Section 13.3.]**

The most interesting result came from a bonus experiment I ran. I asked whether grammar and structure alone, with no vocabulary at all, could predict the category. The answer is yes: style features alone hit 56 percent accuracy, almost three times the 20 percent you would get by chance. That is real evidence that different news beats are written in measurably different styles.

**[ON SCREEN: open the Gradio dashboard, Section 13.4, and type or paste an article live.]**

For the advanced feature, here is an interactive dashboard. I can paste any article and get the full analysis instantly. And this is where that uncertainty guard matters: because the model is trained on 2004 to 2005 BBC news, if I paste something out of scope, it honestly says uncertain instead of forcing a wrong label. That is the behavior you want in a real tool."

## Segment 4 — Business value and conclusion (about 5:00 to 6:30)
**[ON SCREEN: back to the README or the insights section, Section 12.]**

"In the real world, this maps directly onto media-intelligence products. A communications team could point NewsBot at a news feed to automatically flag every article that mentions their company, score whether the coverage is positive or negative, and alert them to negative spikes within minutes. The entity extraction builds a searchable index of who and what is in the news.

Building this taught me how to make eight separate NLP techniques work together as one system, how to prevent data leakage by fitting the vectorizer only on training data, and how to evaluate honestly, including reporting the limitations like the sentiment model misreading financial language.

If I extended it, I would swap the lexicon sentiment for a transformer model like FinBERT to fix that financial-framing error, fine-tune the entity recognizer on modern news, and add multilingual support.

This project is going in my portfolio as a complete, defensible NLP system. Thank you for watching."

---

## Recording checklist
- Tool: OBS, Zoom recording, or your built-in screen recorder. Use a headset mic if you have one.
- Resolution: at least 720p, and zoom the notebook so code and charts are readable.
- Length: keep it under 7 minutes.
- Upload to YouTube as **Unlisted** (or Google Drive set to "anyone with the link"). Test the link in a private browser window.
- Put the link in your README and name the submission MT_Video_Group_SOLO_Trilok_Kalani_ITAI2373.
- Practice once; on the real take, have the notebook already run so the outputs are visible and you are not waiting on cells.

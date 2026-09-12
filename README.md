# Tamil Learning App

A full-stack web application that helps heritage Tamil speakers build literacy through structured lessons, quizzes, and eventually adaptive review.
Most existing resources rely on static charts or images, which get overwhelming fast: learners need to connect letters, sounds, letter combinations, pronunciation, and real world usage all at once. This app breaks that into a guided, trackable learning loop instead.

## Tech Stack

- **Backend:** Django, Django Rest Framework
- **Database:** PostgreSQL

## Core Learning Loop

```
Learn -> Quiz -> Score -> Save Results -> Identify Weak Letters -> Practice Again
```
As the adaptive features come online, this will evolve into:
```
Learn -> Quiz -> Analyze Performance -> Update Mastery -> Schedule Review -> Reassess
```

## Status: V1 (in progress)

Currently building out the MVP:
- Account creation, login/logout
- View Tamil letters with sound and explanation
- Example words for each letter in context
- Multiple choice quizzes on studied letters
- Scoring and saved quiz attempts
- Review of correct and incorrect answers per attempt

V1 starts with a smaller foundational letter set (12 Uyir letters) rather than the full 247 character Tamil script, with content manually curated and independently authored from trusted Tamil linguistic references.

## Roadmap

| Version | Focus |
| ------- | ----- |
| **V1** | Core Learning App: accounts, lessons, multiple choice quizzes, saved attempts, and result review |
| **V2** | Progress and Adaptive Review: per-letter progress tracking, mastery scoring, weak-letter detection, adaptive quiz selection, spaced repetition, and learner progress views |
| **V3** | Teacher Review System: teacher accounts, role-based permissions, content review dashboard, and draft/approved/published workflow |
| **V4** | AI Content Generation: use LLMs to generate lessons and quizzes based on trusted Tamil reference materials |
| **V5** | Generator-Critic Validation: use a second model to check generated content for accuracy and quality |
| **V6** | Human-in-the-Loop Pipeline: require generated content to pass automated checks and teacher review before it is published | 

The long-term architecture separates two systems:
- **learning engine:** tracks learner progress and determines what should be reviewed next
- **AI content pipeline:** generates and checks new learning content before sending it to a teacher for final review

## Notes

All educational content is independently authored using trusted Tamil linguistic resources, including:
- Tamil Virtual Academy
- Tamil Wiktionary

Additional sources and licensing information will be documented as new content is added.

No third-party instructional text, audio, or exercises are reproduced unless permitted by the applicable license or explicit permission has been obtained.
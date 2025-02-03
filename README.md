# Championship

## Init Brainstorm

### Goal
- Predict the upcoming Premier League champion

### Data
- Match outcomes (wins, losses, goals)
- Player related (injuries, transfers)
- Team dynamics (home vs away performance)
- Weather data on game day

### Data challenges
- API integration (football-data.org)
- Web scraping (transfermarkt)
- Handling inconsistencies 

### Approaches (models)
- Regression models (poisson regression)
- Ensemble methodes (Random Forest, XGBoost)
- Time-series models (LSTM)
- Bayesian networks (probabilistic outcomes)
- Deep Learning (enough data?)

### Deployment
- Simple dashboard
- Integration of live data (API setup)

### Psychology of football
- Problem: Games can be decided by a teams state of mind 
- Football outcomes are highly linked to emotional aspects
- How can this be linked to external statistics?
- Where are the corelations between game outcomes and a teams state of mind?

## Project planing

### Milestones
- Market analysis
  - How was this done before?
  - What can it be made better?
- MPV Development
  - Full ml pipeline
    - Data collection
    - EDA
    - Feature Engineering
    - Model selection/building/training
    - Evaluation (Metrics: Accuracy, Log loss, Brier score, comparision vs bookmaker models)
    - Deployment
  - Explaining model decision (XAI: SHAP, LIME)
- Reiteration
- Make it better
  - Updating model as new data comes in
  - Retraining pipeline
- Make it a product!
- Scale it!


Resources:

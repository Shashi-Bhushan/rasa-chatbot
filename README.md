RASA Chatbot
---------------
A task oriented chatbot in restaurant domain, implemented using Rasa NLU and Rasa Core.

## Dependencies
All the project dependencies has been mentioned in `Pipfile` and for a reproducible build, a `Pipfile.lock` has also been provided.

In order to install using pip
```
# download Spacy Model
pip install rasa[spacy]
python -m spacy download en_core_web_md
python -m spacy link en_core_web_md en

# Install Project dependencies
pip install
```

## Directory Tree
```
rasa-chatbot
├── actions.py # Have all the custom actions defined
├── App_nlu.py # Rasa NLU Httpserver 
├── data
│   ├── data.json # train data json format
│   ├── stories.md # Train data stories
│   └── cities.csv # csv for valid cities 
├── config.yml # Rasa NLU config file
├── restaurant_domain.yml # Rasa Core Config file
├── models # Pretrained models
│   ├── dialogue
│   └── nlu
├── README.md
├── nlu_model.py # Initial Train script of Rasa NLU
├── train_online.py # Train script with online training of Rasa NLU
└── train_init.py # Train script of Rasa NLU
```


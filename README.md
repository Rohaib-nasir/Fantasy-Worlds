# Fantasy Worlds ML Project

## Folder structure
```
fantasy-ml-project/
├── data/            # raw CSVs (LOTR, Harry Potter, Star Wars, GoT)
├── notebooks/        # one EDA+cleaning notebook per universe
│   ├── 01_lotr_eda_cleaning.ipynb
│   ├── 02_harrypotter_eda_cleaning.ipynb
│   ├── 03_starwars_eda_cleaning.ipynb
│   └── 04_got_eda_cleaning.ipynb
├── models/           # trained models get saved here (.pkl) later
└── app/              # final interactive app goes here later
```

## Workflow
Each notebook follows the same skeleton: load data → first look → missing
values → univariate exploration → cleaning → feature engineering →
candidate target columns. We fill these in one universe at a time,
starting with LOTR, before touching the app itself.

Open `notebooks/01_lotr_eda_cleaning.ipynb` in Jupyter Lab to start.

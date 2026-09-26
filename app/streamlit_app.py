from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
MODEL_DIR = PROJECT_DIR / "models"

WORLDS = {
    "lotr": {"name": "Lord of the Rings", "mark": "✧", "index": "01 / MIDDLE-EARTH", "color": "#3FA65B"},
    "hp": {"name": "Harry Potter", "mark": "✦", "index": "02 / WIZARDING WORLD", "color": "#C9A227"},
    "sw": {"name": "Star Wars", "mark": "◉", "index": "03 / GALAXY FAR AWAY", "color": "#3D7FE0"},
    "got": {"name": "Game of Thrones", "mark": "♜", "index": "04 / WESTEROS", "color": "#8E97A3"},
}
CLEAN_DATASETS = {
    "lotr": "lotr_characters_clean.csv",
    "hp": "hp_characters_clean.csv",
    "sw": "sw_characters_clean.csv",
    "got": "got_characters_clean.csv",
}
STATIC_TARGET_MODELS = {
    "hp": {
        "Gender": "hp_gender.pkl",
        "Species/Race": "hp_species_race.pkl",
        "Blood": "hp_blood.pkl",
        "hogwarts_house": "hp_hogwarts_house.pkl",
        "profession_group": "hp_profession_group.pkl",
        "is_hogwarts": "hp_is_hogwarts.pkl",
        "has_description": "hp_has_description.pkl",
    },
    "sw": {
        "species_group": "sw_species_group.pkl",
        "gender": "sw_gender.pkl",
        "sex": "sw_sex.pkl",
        "homeworld_group": "sw_homeworld_group.pkl",
        "height": "sw_height.pkl",
        "mass": "sw_mass.pkl",
        "birth_year": "sw_birth_year.pkl",
    },
}
EXTRA_LOTR_TARGET_MODELS = {
    "hair_group": "lotr_hair_group.pkl",
    "birth_age": "lotr_birth_age.pkl",
}
FIELD_LABELS = {
    "name": "Character name",
    "is_dead": "Known to have died",
    "has_spouse": "Has a known spouse",
    "is_hogwarts": "Hogwarts affiliated",
    "has_description": "Has a character description",
    "boolDeadRelations": "Has dead relations",
    "numDeadRelations": "Number of dead relations",
    "film_count": "Films appeared in",
    "has_vehicle": "Has a vehicle",
    "has_starship": "Has a starship",
    "birth_year": "Birth year",
    "isAlive": "Alive",
    "isNoble": "Noble",
    "isMarried": "Married",
    "isPopular": "Popular",
}

st.set_page_config(
    page_title="The Black Ledger | Fantasy Worlds",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def load_clean_data(world: str) -> pd.DataFrame:
    path = DATA_DIR / CLEAN_DATASETS[world]
    if not path.is_file():
        raise FileNotFoundError(f"Clean dataset is missing: {path.name}")
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_manifest(world: str) -> dict[str, Any]:
    path = MODEL_DIR / f"{world}_manifest.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_resource(show_spinner=False, max_entries=8)
def load_saved_model(model_path: str, modified_time_ns: int) -> Any:
    del modified_time_ns
    return joblib.load(model_path)


def target_catalog(world: str) -> dict[str, dict[str, Any]]:
    if world in {"lotr", "got"}:
        targets = dict(load_manifest(world).get("targets", {}))
        if world == "lotr":
            for target, filename in EXTRA_LOTR_TARGET_MODELS.items():
                if (MODEL_DIR / filename).is_file():
                    targets.setdefault(target, {"model_file": filename})
    else:
        targets = {
            target: {"model_file": filename}
            for target, filename in STATIC_TARGET_MODELS[world].items()
        }

    return {
        target: metadata
        for target, metadata in targets.items()
        if target.lower() != "name" and metadata.get("model_file")
    }


def resolve_model(
    world: str, target: str, metadata: dict[str, Any]
) -> tuple[Any, list[str], str]:
    model_path = MODEL_DIR / metadata["model_file"]
    if not model_path.is_file():
        raise FileNotFoundError(f"Saved model is missing: {model_path.name}")

    saved_model = load_saved_model(str(model_path), model_path.stat().st_mtime_ns)
    model = saved_model.get("pipeline") if isinstance(saved_model, dict) else saved_model
    feature_columns = (
        metadata.get("required_features")
        or metadata.get("feature_columns")
        or (saved_model.get("feature_columns") if isinstance(saved_model, dict) else None)
        or getattr(model, "feature_names_in_", None)
    )
    if feature_columns is None or len(feature_columns) == 0:
        raise ValueError(f"Could not determine input features for {world}/{target}.")

    task = metadata.get("task") or (
        saved_model.get("task") if isinstance(saved_model, dict) else None
    )
    estimator = model.steps[-1][1] if hasattr(model, "steps") else model
    if task is None:
        task = "classification" if getattr(estimator, "_estimator_type", None) == "classifier" else "regression"
    return model, list(feature_columns), task


def field_label(feature: str) -> str:
    return FIELD_LABELS.get(feature, feature.replace("_", " ").strip().title())


def render_feature(world: str, target: str, feature: str, data: pd.DataFrame) -> Any:
    label = field_label(feature)
    key = f"{world}-{target}-{feature}"

    if feature.lower() == "name":
        return st.text_input(label, key=key, placeholder="Enter a character name")
    if feature not in data.columns:
        return st.text_input(label, key=key)

    values = data[feature]
    if is_numeric_dtype(values):
        numeric_values = pd.to_numeric(values, errors="coerce").dropna()
        observed = set(numeric_values.unique().tolist())
        if observed and observed.issubset({0, 1}):
            return st.selectbox(
                label,
                options=[0, 1],
                format_func=lambda value: "Yes" if value else "No / not listed",
                key=key,
            )

        minimum = float(numeric_values.min()) if not numeric_values.empty else 0.0
        maximum = float(numeric_values.max()) if not numeric_values.empty else 100.0
        default = float(numeric_values.median()) if not numeric_values.empty else 0.0
        if not all(math.isfinite(number) for number in (minimum, maximum, default)):
            minimum, maximum, default = 0.0, 100.0, 0.0
        if minimum == maximum:
            minimum -= 1.0
            maximum += 1.0
        default = min(max(default, minimum), maximum)
        step = 1.0 if feature in {"numDeadRelations", "film_count"} else 0.1
        return st.number_input(
            label,
            min_value=minimum,
            max_value=maximum,
            value=default,
            step=step,
            key=key,
        )

    options = sorted(values.dropna().astype(str).unique().tolist(), key=str.casefold)
    if not options:
        options = ["Unknown"]
    return st.selectbox(label, options=options, key=key)


def format_prediction(value: Any) -> str:
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float):
        return f"{value:,.2f}"
    return str(value)


def render_home() -> None:
    st.markdown("<div class='ledger-kicker'>INDEX OF KNOWN REALMS</div>", unsafe_allow_html=True)
    st.title("The Black Ledger")
    st.caption("Four realms recorded. Countless lives within them. Choose an entry to consult the record.")

    columns = st.columns(4, gap="small")
    for column, (world, details) in zip(columns, WORLDS.items()):
        with column:
            st.caption(details["index"])
            if st.button(
                f"{details['mark']}  {details['name']}",
                key=f"choose-{world}",
                use_container_width=True,
            ):
                st.session_state.selected_world = world
                st.rerun()


def render_world(world: str) -> None:
    details = WORLDS[world]
    data = load_clean_data(world)
    targets = target_catalog(world)

    rail, content = st.columns([0.09, 0.91], gap="medium")
    with rail:
        if st.button("← INDEX", key="back-to-index"):
            st.session_state.selected_world = None
            st.rerun()
        st.markdown("<div class='rail-seal'>IV</div>", unsafe_allow_html=True)
        st.markdown("<div class='rail-caption'>THE<br>BLACK<br>LEDGER</div>", unsafe_allow_html=True)

    with content:
        st.markdown(
            f"<div class='ledger-kicker'>{details['mark']} &nbsp; {details['index']}</div>",
            unsafe_allow_html=True,
        )
        st.title(details["name"])
        if not targets:
            st.error("No trained prediction models are available for this world.")
            return

        target_labels = {field_label(target): target for target in targets}
        selected_label = st.selectbox(
            "Requested record",
            options=list(target_labels),
            key=f"target-{world}",
        )
        target = target_labels[selected_label]
        metadata = targets[target]
        try:
            model, feature_columns, task = resolve_model(world, target, metadata)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            st.error(f"Could not prepare this model: {exc}")
            return

        st.markdown("#### Record the known details")
        with st.form(f"predict-{world}-{target}"):
            form_columns = st.columns(2)
            input_features: dict[str, Any] = {}
            for index, feature in enumerate(feature_columns):
                with form_columns[index % 2]:
                    input_features[feature] = render_feature(world, target, feature, data)
            submitted = st.form_submit_button("Strike the record", use_container_width=True)

        if submitted:
            row = pd.DataFrame([input_features], columns=feature_columns)
            try:
                prediction = model.predict(row)[0]
            except (TypeError, ValueError) as exc:
                st.error(f"The model could not use those values: {exc}")
                return

            st.markdown("#### The record speaks")
            st.success(format_prediction(prediction))
            st.caption("Estimated numeric value" if task == "regression" else "Predicted category")


st.markdown(
    """
    <style>
    .stApp { background: #0B0B0D; color: #E7DDCD; }
    [data-testid="stHeader"] { background: rgba(11, 11, 13, .96); }
    .ledger-kicker { color: #D46A2B; font: .78rem monospace; letter-spacing: .14em; }
    .rail-seal { margin: 1rem auto; padding: .8rem .5rem; width: fit-content; border: 1px solid #D46A2B; color: #D46A2B; clip-path: polygon(50% 0, 100% 16%, 88% 82%, 50% 100%, 12% 82%, 0 16%); }
    .rail-caption { color: #929297; font: .65rem/1.8 monospace; letter-spacing: .13em; text-align: center; }
    div[data-testid="stForm"] { border: 1px solid #303034; border-left: 2px solid #D46A2B; border-radius: 0; background: #161618; }
    div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button { border-radius: 0; border-color: #D46A2B; }
    div[data-testid="stAlert"] { border-radius: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault("selected_world", None)
if st.session_state.selected_world not in WORLDS:
    render_home()
else:
    render_world(st.session_state.selected_world)

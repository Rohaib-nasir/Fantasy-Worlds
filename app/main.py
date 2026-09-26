from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_DIR / "models"

WORLDS = {
    "lotr": "Lord of the Rings",
    "hp": "Harry Potter",
    "sw": "Star Wars",
    "got": "Game of Thrones",
}

STATIC_TARGET_MODELS = {
    "hp": {
        "Gender": "hp_gender.pkl",
        "Species/Race": "hp_species_race.pkl",
        "Blood": "hp_blood.pkl",
        "hogwarts_house": "hp_hogwarts_house.pkl",
        "profession_group": "hp_profession_group.pkl",
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

EXTRA_TARGET_MODELS = {
    "lotr": {
        "hair_group": "lotr_hair_group.pkl",
        "birth_age": "lotr_birth_age.pkl",
    },
    "hp": {
        "is_hogwarts": "hp_is_hogwarts.pkl",
        "has_description": "hp_has_description.pkl",
    },
}


class PredictRequest(BaseModel):
    world: Literal["lotr", "hp", "sw", "got"]
    target: str
    input_features: dict[str, Any]


class PredictResponse(BaseModel):
    world: str
    target: str
    prediction: Any


app = FastAPI(title="Fantasy Worlds Model Tester")


@lru_cache(maxsize=2)
def load_manifest(world: str) -> dict[str, Any]:
    manifest_path = MODEL_DIR / f"{world}_manifest.json"
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail=f"Could not read the {world} model manifest") from exc


def get_target_metadata(world: str, target: str) -> dict[str, Any]:
    extra_targets = EXTRA_TARGET_MODELS.get(world, {})
    if target in extra_targets:
        return {"model_file": extra_targets[target]}

    if world in {"lotr", "got"}:
        targets = load_manifest(world).get("targets", {})
        if target not in targets:
            raise HTTPException(status_code=404, detail=f"Unknown target '{target}' for {world}")
        return targets[target]

    target_models = STATIC_TARGET_MODELS[world]
    if target not in target_models:
        raise HTTPException(status_code=404, detail=f"Unknown target '{target}' for {world}")
    return {"model_file": target_models[target]}


@lru_cache(maxsize=64)
def load_model(world: str, target: str) -> tuple[Any, tuple[str, ...]]:
    metadata = get_target_metadata(world, target)
    model_path = MODEL_DIR / metadata["model_file"]
    if not model_path.is_file():
        raise HTTPException(status_code=500, detail=f"Saved model is missing: {model_path.name}")

    try:
        saved_model = joblib.load(model_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not load model: {model_path.name}") from exc

    model = saved_model.get("pipeline") if isinstance(saved_model, dict) else saved_model
    features = metadata.get("required_features") or metadata.get("feature_columns")
    if not features and isinstance(saved_model, dict):
        features = saved_model.get("feature_columns")
    if not features:
        features = getattr(model, "feature_names_in_", None)
    if features is None or len(features) == 0:
        raise HTTPException(status_code=500, detail=f"Could not determine input features for {world}/{target}")

    return model, tuple(str(feature) for feature in features)


@app.get("/worlds")
def list_worlds() -> dict[str, list[dict[str, str]]]:
    return {"worlds": [{"id": key, "name": name} for key, name in WORLDS.items()]}


@app.get("/world/{world}/targets")
def list_targets(world: str) -> dict[str, Any]:
    if world not in WORLDS:
        raise HTTPException(status_code=404, detail=f"Unknown world '{world}'")

    if world in {"lotr", "got"}:
        targets = list(load_manifest(world).get("targets", {}).keys())
    else:
        targets = list(STATIC_TARGET_MODELS[world].keys())
    targets.extend(EXTRA_TARGET_MODELS.get(world, {}).keys())
    return {"world": world, "targets": targets}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    model, required_features = load_model(request.world, request.target)
    missing_features = [feature for feature in required_features if feature not in request.input_features]
    if missing_features:
        raise HTTPException(
            status_code=422,
            detail={"missing_input_features": missing_features},
        )

    row = pd.DataFrame(
        [{feature: request.input_features[feature] for feature in required_features}],
        columns=required_features,
    )
    try:
        prediction = model.predict(row)[0]
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=f"Invalid input feature value: {exc}") from exc

    if hasattr(prediction, "item"):
        prediction = prediction.item()
    return PredictResponse(world=request.world, target=request.target, prediction=prediction)

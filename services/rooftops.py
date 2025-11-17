from sqlalchemy.orm import Session
from models import Rooftop, Project
from schemas import RooftopCreate, ProjectRooftop, RooftopUpdate
from fastapi import HTTPException, status, responses
from utils import transform_pvcalc_data
import uuid
import requests


def get_projects_rooftops(project_id: uuid.UUID, db: Session) -> list[Rooftop]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't find project with id '{project_id}'.",
        )

    rooftops = db.query(Rooftop).filter((Rooftop.project_id) == project_id).all()
    return rooftops


def create_new_rooftop(
    rooftop: RooftopCreate, project_id: uuid.UUID, db: Session
) -> ProjectRooftop:
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't find project with id '{project_id}'.",
        )

    new_rooftop = Rooftop(**rooftop.model_dump(), project_id=project_id)
    db.add(new_rooftop)
    db.commit()
    db.refresh(new_rooftop)

    # extract lat, long from initial polygon
    try:
        first_point = new_rooftop.initial_polygon[0]
        lon, lat = first_point[0], first_point[1]

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid initial_polygon: cannot extract coordinates.",
        )

    try:
        pvcalc_result = fetch_pvcalc_data(
            lat=lat,
            lon=lon,
            angle=new_rooftop.angle,
            slope=new_rooftop.slope,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"PVCalc API error: {e}",
        )
    new_rooftop.solar_production = transform_pvcalc_data(pvcalc_result)
    db.commit()
    db.refresh(new_rooftop)

    return new_rooftop


def update_project_rooftop(
    rooftop_id: uuid.UUID, rooftop_data: RooftopUpdate, db: Session
) -> ProjectRooftop:
    rooftop = db.query(Rooftop).filter(Rooftop.id == rooftop_id).first()
    if not rooftop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find this rooftop.",
        )

    for key, value in rooftop_data.model_dump(exclude_unset=True).items():
        setattr(rooftop, key, value)

    db.commit()
    db.refresh(rooftop)
    return rooftop


def delete_project_rooftop(rooftop_id: uuid.UUID, db: Session):
    rooftop = db.query(Rooftop).filter(Rooftop.id == rooftop_id).first()
    if not rooftop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find this rooftop.",
        )

    db.delete(rooftop)
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)


def fetch_pvcalc_data(lat: float, lon: float, angle: float, slope: float) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "aspect": angle,
        "angle": slope,
        "peakpower": 1,
        "loss": 16,
        "outputformat": "json",
    }

    url = "https://re.jrc.ec.europa.eu/api/v5_2/pvcalc"

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"PVCalc returned {response.status_code}: {response.text}")

    return response.json()

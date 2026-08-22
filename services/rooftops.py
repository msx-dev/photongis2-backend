from sqlalchemy.orm import Session
from models import Rooftop, Project, Panel, User
from schemas import RooftopCreate, ProjectRooftop, RooftopUpdate,RooftopUpdateResponse
from fastapi import HTTPException, status, responses
from models import ElectricalString
from utils import transform_pvcalc_data
import uuid
import requests


def get_projects_rooftops(project_id: uuid.UUID, db: Session, current_user: User):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't find project with id '{project_id}'.",
        )

    rooftops = (
        db.query(Rooftop)
        .filter(Rooftop.project_id == project_id)
        .order_by(Rooftop.created_at.asc())
        .all()
    )

    response = []

    for rooftop in rooftops:
        panel = rooftop.panel

        # Convert ORM → dict
        r = rooftop.__dict__.copy()
        r.pop("_sa_instance_state", None)

        r["width"] = panel.width
        r["height"] = panel.height
        r["power"] = panel.power
        r["name"] = panel.name
        r["vmp"] = panel.vmp
        r["voc"] = panel.voc
        r["imp"] = panel.imp
        r["isc"] = panel.isc

        response.append(r)

    return response


def create_new_rooftop(
    rooftop: RooftopCreate, project_id: uuid.UUID, db: Session, current_user: User
) -> ProjectRooftop:
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_id == current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't find project with id '{project_id}'.",
        )

    new_rooftop = Rooftop(**rooftop.model_dump(), project_id=project_id)
    db.add(new_rooftop)
    db.commit()
    db.refresh(new_rooftop)

    # Fetch the associated panel
    panel = db.query(Panel).filter(Panel.id == new_rooftop.panel_id).first()
    if not panel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can't find panel with id '{new_rooftop.panel_id}'.",
        )

    # Extract lat, lon from initial polygon
    try:
        first_point = new_rooftop.initial_polygon[0]
        lon, lat = first_point[1], first_point[0]

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

    # Construct ProjectRooftop response with panel data
    return ProjectRooftop(
        id=new_rooftop.id,
        project_id=new_rooftop.project_id,
        additional_panels=new_rooftop.additional_panels,
        initial_polygon=new_rooftop.initial_polygon,
        transformed_additional_panels=new_rooftop.transformed_additional_panels,
        angle=new_rooftop.angle,
        slope=new_rooftop.slope,
        solar_production=new_rooftop.solar_production,
        spacing=new_rooftop.spacing,
        width=panel.width,
        height=panel.height,
        power=panel.power,
        name=panel.name,
        vmp=panel.vmp,
        voc=panel.voc,
        imp=panel.imp,
        isc=panel.isc,
    )


def update_project_rooftop(
    rooftop_id: uuid.UUID, rooftop_data: RooftopUpdate, db: Session, current_user: User
) -> RooftopUpdateResponse:
    rooftop = (
        db.query(Rooftop)
        .join(Project, Rooftop.project_id == Project.id)
        .filter(Rooftop.id == rooftop_id, Project.owner_id == current_user.id)
        .first()
    )
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


def delete_project_rooftop(rooftop_id: uuid.UUID, db: Session, current_user: User):
    rooftop = (
        db.query(Rooftop)
        .join(Project, Rooftop.project_id == Project.id)
        .filter(Rooftop.id == rooftop_id, Project.owner_id == current_user.id)
        .first()
    )
    if not rooftop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find this rooftop.",
        )

    rooftop_prefix = str(rooftop_id)

    # Manually remove electrical strings that reference this rooftop - TODO: Consider using a more efficient query to delete related strings in bulk.
    electrical_strings = db.query(ElectricalString).all()

    for electrical_string in electrical_strings:
        if any(
            polygon.startswith(rooftop_prefix)
            for polygon in electrical_string.connected_polygons
        ):

            db.delete(electrical_string)

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
    print(params)

    url = "https://re.jrc.ec.europa.eu/api/v5_2/pvcalc"

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"PVCalc returned {response.status_code}: {response.text}")

    return response.json()

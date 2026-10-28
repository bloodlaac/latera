from fastapi import APIRouter, status, HTTPException
from backend.api.schemas.tag import TagCreate, TagResponse
from backend.dependencies import SessionDep, StorageDep


router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@router.get("", response_model=list[TagResponse])
def get_tags(session: SessionDep, storage: StorageDep):
    return storage.get_tags(session)


@router.get("/{id}", response_model=TagResponse)
def get_tag(id: int, session: SessionDep, storage: StorageDep):
    tag = storage.get_tag(session, id)

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no tag with such id"
        )

    return tag


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, session: SessionDep, storage: StorageDep):
    try:
        new_tag = storage.post_tag(session, tag)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"tag '{e}' already exists"
        )

    return new_tag
        

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(id: int, session: SessionDep, storage: StorageDep):
    if not storage.delete_tag(session, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no tag with such id"
        )
    return

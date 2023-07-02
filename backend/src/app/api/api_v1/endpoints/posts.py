from typing import Any, List, Dict

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.media import upload_file, upload_multiple_files, get_all_medias, get_one_media
from app import schemas, services
from app.deps.base import get_db
from app.deps.post import get_post_service
from app.deps.user import get_current_user


router = APIRouter()

image_url_types = ['absolute', 'relative']

@router.post(
    '/add',
    response_model=schemas.Post,
    summary="Create new post"
    )
async def create_post(
    post_in: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    post_service: services.PostService = Depends(get_post_service),
    current_user = Depends(get_current_user)
    ):
    return await post_service.create(db=db, obj_in=post_in, current_user=current_user)


@router.get(
    '/get-all',
    response_model=List[schemas.PostDisplay],
    summary="Get all posts"
)
async def get_all_posts(
    *,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    post_service: services.PostService = Depends(get_post_service)
    ):
    
    return await post_service.get_all(db=db, skip=skip, limit=limit)

# ==============================================================================
# Image API
# ==============================================================================

@router.post(
    '/image',
    response_model=Dict[str, str]
    )
def upload_an_image(
    image: UploadFile = File(...),
    current_user: schemas.UserAuth = Depends(get_current_user)
    ):
    """
    Upload an image.
    """
    filename = upload_file(image)
    return {'filename': filename}

@router.post(
    '/multi-image',
    response_model=Dict[str, List[str]]
    )
def upload_multiple_images(
    images: List[UploadFile] = File(...),
    current_user: schemas.UserAuth = Depends(get_current_user)
    ):
    """
    Upload multiple images.
    """
    filenames = upload_multiple_files(images)
    return {'filenames': filenames}

@router.get(
    '/multi-image',
#    response_model=schemas.MultiMedia
    )
async def get_all_images():
    """
    Get all images.
    """
    all_medias = await get_all_medias()
    return JSONResponse(content=all_medias)

@router.get(
    '/image',
#    response_model=schemas.SingleMedia
    )
async def get_image(
    filename: str
):
    """
    Get An Image With provided name.
    """
    
    get_media = await get_one_media(filename)
    if not get_media:
        raise HTTPException(status_code=404, detail=f"Image not found with this name: {filename}")
    response = {"filename": get_media}
    return JSONResponse(content=response)


@router.get(
    "/get/{id}",
    response_model=schemas.Post,
    summary="Get a post by id"
)
async def get_post_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    post_service: services.PostService = Depends(get_post_service),
    ):
    """
    Get a specific post by id.
    """
    
    return await post_service.get(db=db, id=id)


@router.delete(
    '/delete/{id}',
    response_model=schemas.Post,
    summary="Delete a post by id"
    )
async def delete(    
    *,
    db: AsyncSession = Depends(get_db),
    post_service: services.PostService = Depends(get_post_service),
    current_user: schemas.UserAuth = Depends(get_current_user),
    id: int,
    ):
    """
    Delete a post.
    """
    
    return await post_service.remove_post_by_current_user(db=db, id=id, current_user=current_user)

@router.put(
    '/edit/{id}',
    response_model=schemas.PostUpdate,
    summary="Edit a post by id"
    )
async def update_post_by_id(    
    *,
    id: int,
    post_in: schemas.PostUpdate,
    db: AsyncSession = Depends(get_db),
    post_service: services.PostService = Depends(get_post_service),
    current_user: schemas.UserAuth = Depends(get_current_user),

    ):
    """
    Update a post.
    """
    
    return await post_service.update(db=db, id=id, obj_in=post_in)




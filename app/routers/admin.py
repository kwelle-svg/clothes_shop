from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.models.products_model import *
from app.settings import db_dependency, templates

router = APIRouter(
    tags=["Admins"],
    prefix="/admin")

# Make it only for admins
@router.get("/")
async def admin_page(request: Request, db: db_dependency):
    all_brands = db.query(Brand).all()
    all_categories = db.query(Category).all()
    all_products = db.query(Product).all()
    return templates.TemplateResponse(name="admin_dashboard.html", request=request, context={"brands": all_brands, "categories": all_categories, "products": all_products})

@router.post("/brands_postdata")
async def brands_postdata(db: db_dependency, name=Form()):
    try:
        new_brand = Brand(name=name)
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
    except:
        raise HTTPException(status_code=403)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/categories_postdata")
async def categories_postdata(db: db_dependency, name=Form()):
    try:
        new_category = Category(name=name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except:
        raise HTTPException(status_code=403)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/products_postdata")
async def products_postdata(db: db_dependency, name=Form(),
                            brand_id=Form(),
                            category_id=Form(),
                            price=Form()):
    try:
        new_product = Product(name=name, brand_id=brand_id, category_id=category_id, price=price)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except:
        raise HTTPException(status_code=403)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
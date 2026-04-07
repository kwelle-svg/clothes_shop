from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.cart import *
from app.models.users_model import User
from app.models.products_model import Cart, CartItem, Product
from app.auth.auth import get_current_user
from app.settings import get_db

router = APIRouter(
    tags=["Carts"],
    prefix="/cart")

def get_current_cart(db, current_user) -> Cart | None:
    cart = db.query(Cart).filter(Cart.user_id==current_user.id).first()
    
    if not cart:
        return None
    return cart

@router.post("/add")
async def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = get_current_cart(db, current_user)
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    product = db.query(Product).filter(Product.id==item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Didn't find product.")
    
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
    else:
        new_item = CartItem(cart_id=cart.id, **item_data.model_dump())
        db.add(new_item)
    db.commit()
    db.refresh(cart)
    return cart
    

@router.get("/all")
async def get_all_in_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = get_current_cart(db, current_user)
    if not cart:
        raise HTTPException(status_code=404, detail="Didn't find cart")
    return cart.items

@router.get("/price")
async def get_total_price(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = get_current_cart(db, current_user)
    if not cart:
        raise HTTPException(status_code=404, detail="Didn't find cart")

    total_price = 0
    if cart:
        for item in cart.items:
            quantity = item.quantity
            product_price = item.product.price

            total_price+=quantity*product_price
    return total_price

@router.put("/update")
async def update():
    pass

@router.patch("/delete")
async def delete_in_cart(
    item_data: CartItemOut,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = get_current_cart(db, current_user)
    if not cart:
        raise HTTPException(status_code=404, detail="Didn't find cart")

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item and existing_item.quantity>=item_data.quantity:
        existing_item.quantity -= item_data.quantity
        if existing_item.quantity <= 0:
            db.delete(existing_item)
    else:
        raise HTTPException(status_code=404, detail="Did't find product in cart.")
    db.commit()
    db.refresh(cart)
    return cart
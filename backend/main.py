from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models, database
from fastapi.middleware.cors import CORSMiddleware

# para ponerse las librerías, ejecutar pip install -r requirements.txt

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#ENDPOINTS 

@app.get("/")
def leer_root():
    return {"message": "Bienvenido a la API de la Tienda"}

@app.post("/productos/")
def create_producto(name: str, price: float, description: str, image_url: str = None, db: Session = Depends(get_db)):
    new_product = models.Product(name=name, price=price, description=description, image_url=image_url)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/productos/")
def read_producto(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/carrito/")
def add_to_carrito(product_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    carrito_item = models.CarritoItem(product_id=product_id, quantity=quantity)
    db.add(carrito_item)
    db.commit()
    return {"message": "Producto agregado al carrito"}

@app.get("/carrito/")
def get_carrito(db: Session = Depends(get_db)):
    return db.query(models.CarritoItem).all()

@app.get("/carrito/total")
def get_carrito_total(db: Session = Depends(get_db)):
    items = db.query(models.CarritoItem).all()
    
    total = 0.0
    for item in items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product:
            total += product.price * item.quantity
            
    return {"total_items": len(items), "total_price": total}

@app.delete("/productos/{product_id}")
def delete_producto(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(product)
    db.commit()
    
    return {"message": f"Producto {product_id} eliminado correctamente"}
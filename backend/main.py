from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models, database
from fastapi.middleware.cors import CORSMiddleware
from schemas import ProductCreate

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

@app.post("/productos/")
def create_producto(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product.name, 
        price=product.price, 
        description=product.description, 
        image_url=product.image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/productos")
def read_producto(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.delete("/productos/{product_id}")
def delete_producto(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(product)
    db.commit()
    
    return {"message": f"Producto {product_id} eliminado correctamente"}
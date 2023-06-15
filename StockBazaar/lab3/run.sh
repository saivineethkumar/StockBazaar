cd src/
cd backend/catalog/
python3 catalog-service.py &
cd ../order/
python3 order-service.py -id 3 &
python3 order-service.py -id 2 &
python3 order-service.py -id 1 &
cd ../../frontend
python3 frontend-service.py &
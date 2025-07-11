docker exec -it xtrader-app bash
# Then inside container:
source /opt/conda/etc/profile.d/conda.sh  # Initialize conda
conda activate xtrader-env
python manage.py shell

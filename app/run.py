import os

from apscheduler.schedulers.blocking import BlockingScheduler
from app.simplified_model_builder import FruitsLabelingService as PredictionService
from app.communication_controller import download_job, send_warming_up, send_result, send_error
from app.data_builder import prepare_dataframe
import logging
from time import sleep
from dotenv import load_dotenv


def predict_data():
    try:
        logging.info(f"Downloading job")
        job = download_job()
        job_id = job.get('id')
    except ConnectionError as err:
        logging.warning(err)
        return
    try:
        logging.info(f"Job {job_id}: Downloaded job")
        job = send_warming_up(job_id)
        logging.info(f"Job {job_id}: preparing data")
        df = prepare_dataframe(job.get('data'))
        logging.info(f"Job {job_id}: loading model")
        ps = PredictionService(file_name='fruit_data_with_colors.txt', model_name='fruits')
        ps.load_model()
        sleep(2)
        logging.info(f"Job {job_id}: predicting")
        result = ps.predict(df)
        sleep(2)
        logging.info(f"Job {job_id}: prediction result {result}")
        send_result(job_id, result)
    except ConnectionError as err:
        send_error(job_id)
        logging.warning(err)


def init_app():
    logging.basicConfig(level=logging.INFO)
    scheduler = BlockingScheduler()
    scheduler.add_jobstore('redis', jobs_key='fruit_labeling.jobs', run_times_key='fruit_labeling.run_times')
    task_interval = int(os.getenv('TASK_INTERVAL', 5))

    scheduler.add_job(predict_data, 'interval', minutes=task_interval)

    try:
        print('scheduler starting')
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        print('removing all jobs')
        scheduler.remove_all_jobs()
        print(len(scheduler.get_jobs()))


if __name__ == '__main__':
    # example data
    # {"mass": 160,"width": 4,"height": 5.1,"color_score": 0.6}
    load_dotenv()
    init_app()

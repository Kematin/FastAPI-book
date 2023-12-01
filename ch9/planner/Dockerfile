FROM python:3.10

# set workdir
WORKDIR /planner_app

# install requirements
COPY requirements.txt /planner_app
RUN pip install --upgrade pip && pip install -r /planner_app/requirements.txt

# Give open port
EXPOSE 8000

# add project to workdir
ADD ./ /planner_app

# run app
CMD ["python", "main.py"]

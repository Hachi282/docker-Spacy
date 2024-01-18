FROM public.ecr.aws/lambda/python:3.9

# COPY requirements.txt ./
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN python -m pip install -r requirements.txt

# RUN pip install -U spacy
RUN python -m spacy download zh_core_web_sm && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV SPACY_MODEL zh_core_web_sm

# WORKDIR /app

# COPY app.py ./
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.handler" ]

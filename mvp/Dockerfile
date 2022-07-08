from python

RUN pip install todoist-api-python
RUN pip install pyyaml google-api-python-client google-auth-oauthlib todoist-python
COPY basic.py basic.py
COPY token.secret token
ENV pom_limit=5
CMD python3 basic.py
